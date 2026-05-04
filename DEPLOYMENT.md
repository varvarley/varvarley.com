# Portfolio Deployment Guide — AWS S3 + CloudFront

This walks you end-to-end from a folder of HTML files on your laptop to a live,
HTTPS-secured site at your own domain. Plan on ~45 minutes the first time.

**Architecture**

```
  varvarley.com
         │
         ▼
    CloudFront (CDN + HTTPS + caching, global)
         │
         ▼
   S3 bucket: varvarley-com-191683921282 (us-west-1)
   stores index.html, styles.css, assets/
```

S3 stores your files cheaply. CloudFront sits in front of S3 to give you HTTPS,
a global CDN for speed, and a single place to attach your domain and SSL cert.

---

## 0. What's in this folder

```
varvarley.com/
├── index.html     ← the page
├── styles.css     ← ALL design lives here, edit the :root block at the top
├── script.js      ← tiny interactive bits (mobile nav, year stamp)
├── assets/        ← images, resume.pdf, favicon, project screenshots
├── deploy.ps1     ← one-command deploy script (fill in your bucket/dist ID)
└── DEPLOYMENT.md  ← this file
```

### Quick local preview (Windows / Lenovo Yoga)

Just double-click `index.html`. For a better dev experience (so relative paths
and fetch() behave the way they will in production), run a tiny local server.

Open **PowerShell** in this folder (Shift-right-click the folder →
"Open in Terminal" or "Open PowerShell window here"):

```powershell
cd "C:\Users\00jgv\varvarley.com"
python -m http.server 8000
# then open http://localhost:8000 in your browser
```

If `python` isn't recognized, install it from https://www.python.org/downloads/
(check "Add Python to PATH" during install), or install it from the Microsoft
Store (search for "Python 3"). Alternatively, install the **Live Server**
extension in VS Code — right-click `index.html` → "Open with Live Server".

Edit `styles.css` → save → refresh the browser. That's your dev loop.

---

## 1. Tools to install (one-time, Windows)

1. **AWS CLI for Windows** — download and run the MSI installer:
   https://awscli.amazonaws.com/AWSCLIV2.msi
   After install, close and reopen PowerShell.
2. **An IAM user with programmatic access** (don't use your root account).
   In the AWS console: IAM → Users → Create user → attach `AmazonS3FullAccess`,
   `CloudFrontFullAccess`, and `AmazonRoute53FullAccess`. Create an access key
   (choose "Command Line Interface"), then in PowerShell run:

   ```powershell
   aws configure
   ```

   Paste your Access Key ID, Secret Access Key, default region (you set
   this to `us-west-1` — that's fine, you can override per command when
   needed), and default output format (`json`).
3. **Git for Windows** (optional but recommended if you want to version-control
   the site): https://git-scm.com/download/win — this also gives you Git Bash,
   a Unix-style shell if you ever want to run bash-style commands verbatim.

Verify AWS CLI works:

```powershell
aws sts get-caller-identity
```

---

## 2. Create and configure the S3 bucket

S3 bucket names are globally unique. We're using **`varvarley-com-191683921282`**
(domain + AWS account ID), which guarantees uniqueness and reads cleanly.

> **Gotcha that bit us:** the AWS console may suggest a name ending in `-an`
> like `varvarley.com-191683921282-us-west-1-an`. That suffix tells AWS you
> want one of its newer "account-regional namespace" bucket types, which
> require a special header and aren't what we want for a static site. Stick
> to a normal general-purpose bucket name without that suffix.

PowerShell uses backtick `` ` `` for line continuation, not backslash:

```powershell
# Create the bucket in us-west-1.
# LocationConstraint is required for any region OTHER than us-east-1.
aws s3api create-bucket `
  --bucket varvarley-com-191683921282 `
  --region us-west-1 `
  --create-bucket-configuration LocationConstraint=us-west-1

# Upload everything from the current folder
aws s3 sync . s3://varvarley-com-191683921282/ `
  --exclude "DEPLOYMENT.md" `
  --exclude "deploy.ps1" `
  --exclude ".git/*"

# Sanity check
aws s3 ls s3://varvarley-com-191683921282/
```

The bucket region (us-west-1) is independent of CloudFront — CloudFront is
global, and your ACM cert in the next step lives in us-east-1 regardless of
where the bucket is.

We are NOT going to use S3's "static website hosting" feature. Instead, we'll
keep the bucket private and let CloudFront pull from it via an Origin Access
Control. This is the modern best practice — more secure and it supports HTTPS.

---

## 3. Request an SSL certificate (ACM)

The cert must be in **us-east-1** for CloudFront — this is a hard AWS rule, and
applies even though your bucket lives in us-west-1. In the AWS console:

1. Go to **Certificate Manager**, then **change the region selector in the
   top-right corner to N. Virginia (us-east-1)**. This is the most common
   stumble — easy to forget and the cert won't show up in CloudFront if you
   create it in the wrong region.
2. Request a public certificate.
3. Add both: `varvarley.com` and `www.varvarley.com`.
4. Choose **DNS validation**.
5. ACM will show you CNAME records. If your DNS is in Route 53, click
   "Create records in Route 53" and you're done. If your domain is at
   Namecheap / Cloudflare / GoDaddy, go there and create those CNAME records
   manually.
6. Wait until the certificate status becomes **Issued** (usually 2-10 minutes).

Copy the ARN of the certificate — you'll need it in the next step.

---

## 4. Create the CloudFront distribution

Console route (easier the first time):

1. CloudFront → Create distribution.
2. **Origin domain**: pick your S3 bucket from the dropdown (the
   `.s3.amazonaws.com` option, not the website-endpoint one).
3. **Origin access**: choose "Origin access control settings (recommended)"
   and click "Create control setting" with the defaults. This is what lets
   CloudFront read your private bucket.
4. **Viewer protocol policy**: "Redirect HTTP to HTTPS".
5. **Default root object**: `index.html`.
6. **Alternate domain names (CNAMEs)**: add `varvarley.com` and
   `www.varvarley.com`.
7. **Custom SSL certificate**: pick the cert you created in step 3.
8. Create distribution.

When it's created, CloudFront will show a banner with a bucket policy it wants
you to paste into S3. Copy that policy, go to S3 → your bucket → Permissions →
Bucket policy → paste it in and save. This is what actually grants CloudFront
read access.

Wait ~5 minutes for the distribution status to go from "Deploying" to
"Enabled". Test it by opening the `*.cloudfront.net` URL — your site should
load over HTTPS.

---

## 5. Point varvarley.com at CloudFront

Two paths depending on where your DNS lives:

### If your DNS is in Route 53

1. Route 53 → Hosted zones → `varvarley.com`.
2. Create record:
   - Record name: (leave blank for the apex, i.e. `varvarley.com` itself)
   - Type: `A`
   - Toggle **Alias** on
   - Route traffic to: "Alias to CloudFront distribution" → pick yours
3. Repeat for the `www` subdomain: same as above but with `www` in Record name.

### If your DNS is at Namecheap / Cloudflare / GoDaddy

Most registrars don't support Alias records, so use CNAMEs:

- `www.varvarley.com` → CNAME → `dxxxxx.cloudfront.net` (your distribution)
- For the apex `varvarley.com`, you'll need either:
  - A registrar that supports "ANAME" or "flattened CNAME" (Cloudflare does), OR
  - Redirect the apex to `www` using your registrar's URL forwarding, OR
  - Move DNS to Route 53 (free to use with your own domain, charges ~$0.50/mo
    per hosted zone).

DNS propagation usually finishes in minutes but can take up to 48 hours.

---

## 6. Your update workflow (use every time you change the site)

Run these from inside `C:\Users\00jgv\varvarley.com` in PowerShell:

```powershell
aws s3 sync . s3://varvarley-com-191683921282/ `
  --delete `
  --exclude "DEPLOYMENT.md" `
  --exclude "deploy.ps1" `
  --exclude ".git/*"

# Bust CloudFront's cache so changes appear immediately
aws cloudfront create-invalidation `
  --distribution-id YOUR-DISTRIBUTION-ID `
  --paths "/*"
```

You can find your distribution ID in the CloudFront console. A `deploy.ps1`
script is included in this folder — the bucket name is already filled in,
you just need to paste your CloudFront distribution ID at the top once,
then going forward you just run:

```powershell
.\deploy.ps1
```

(If PowerShell blocks the script the first time, run
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and confirm.)

---

## 7. How to edit the design (the fun part)

All the visual theming is controlled by CSS variables at the top of
`styles.css`. Open that file and look at the `:root { ... }` block — change the
hex codes and everything updates consistently.

The file also includes a light-theme palette commented out, ready to paste over
the dark one if you want to flip the whole look.

Structural changes:
- Add a new project → copy one of the `<article class="project">` blocks in
  `index.html` and edit.
- Change section order → reorder the `<section>` blocks in `index.html`.
- Change copy → edit the text directly in `index.html`.

---

## 8. Cost expectations

For a personal portfolio with low traffic:
- S3 storage: pennies (~$0.02/GB/month, your site is ≪1GB)
- CloudFront: 1 TB/month free tier, you will not exceed it
- Route 53: $0.50/month per hosted zone (if you use it)
- ACM certificate: free

Realistic total: **~$0.50 — $1.00 per month**.

---

## 9. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `MissingNamespaceHeader` on `create-bucket` | Your bucket name ends in `-an`. Drop the suffix — that's a separate bucket type we don't want. |
| `IllegalLocationConstraintException` | You used `--region us-west-1` but forgot `--create-bucket-configuration LocationConstraint=us-west-1`. Required for any non-`us-east-1` region. |
| ACM cert doesn't appear in CloudFront dropdown | Cert was created in the wrong region. Switch ACM to us-east-1 and re-request — the old cert in us-west-1 just sits unused (no charge). |
| `AccessDenied` loading the site | Bucket policy from step 4 didn't get pasted |
| Old CSS showing up | CloudFront cache — run the invalidation command |
| `ERR_CERT_COMMON_NAME_INVALID` | Your cert doesn't cover that hostname, or you hit the cloudfront.net URL from a browser |
| Domain doesn't resolve | DNS hasn't propagated yet, or A/CNAME record points at wrong target |
| Images broken | Path in HTML doesn't match what's in S3 — check case sensitivity |

If you get stuck on any step, paste the error at me and I'll help debug.
