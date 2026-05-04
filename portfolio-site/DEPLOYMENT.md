# Portfolio Deployment Guide — AWS S3 + CloudFront

This walks you end-to-end from a folder of HTML files on your laptop to a live,
HTTPS-secured site at your own domain. Plan on ~45 minutes the first time.

**Architecture**

```
  your-domain.com
         │
         ▼
    CloudFront (CDN + HTTPS + caching)
         │
         ▼
       S3 bucket (stores index.html, styles.css, assets/)
```

S3 stores your files cheaply. CloudFront sits in front of S3 to give you HTTPS,
a global CDN for speed, and a single place to attach your domain and SSL cert.

---

## 0. What's in this folder

```
portfolio-site/
├── index.html     ← the page
├── styles.css     ← ALL design lives here, edit the :root block at the top
├── script.js      ← tiny interactive bits (mobile nav, year stamp)
├── assets/        ← images, resume.pdf, favicon, project screenshots
└── DEPLOYMENT.md  ← this file
```

### Quick local preview (Windows / Lenovo Yoga)

Just double-click `index.html`. For a better dev experience (so relative paths
and fetch() behave the way they will in production), run a tiny local server.

Open **PowerShell** in this folder (Shift-right-click the folder →
"Open in Terminal" or "Open PowerShell window here"):

```powershell
cd "C:\Users\00jgv\Personal Projects\portfolio-site"
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

   Paste your Access Key ID, Secret Access Key, default region (`us-east-1`
   is easiest), and default output format (`json`).
3. **Git for Windows** (optional but recommended if you want to version-control
   the site): https://git-scm.com/download/win — this also gives you Git Bash,
   a Unix-style shell if you ever want to run the bash-style commands in this
   guide verbatim.

Verify AWS CLI works:

```powershell
aws sts get-caller-identity
```

---

## 2. Create and configure the S3 bucket

S3 bucket names are globally unique. Pick something like `varley-portfolio` or
your domain name. Replace `YOUR-BUCKET` with whatever you chose in all commands
below.

PowerShell uses backtick `` ` `` for line continuation, not backslash. So:

```powershell
# Create the bucket (us-east-1 keeps life simplest — it's the only region
# where ACM certs work with CloudFront)
aws s3api create-bucket --bucket YOUR-BUCKET --region us-east-1

# Upload everything from the current folder
aws s3 sync . s3://YOUR-BUCKET/ `
  --exclude "DEPLOYMENT.md" `
  --exclude ".git/*"
```

We are NOT going to use S3's "static website hosting" feature. Instead, we'll
keep the bucket private and let CloudFront pull from it via an Origin Access
Control. This is the modern best practice — more secure and it supports HTTPS.

---

## 3. Request an SSL certificate (ACM)

Must be in **us-east-1** for CloudFront. In the AWS console:

1. Go to **Certificate Manager** → make sure region is `us-east-1`.
2. Request a public certificate.
3. Add both: `your-domain.com` and `www.your-domain.com`.
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
6. **Alternate domain names (CNAMEs)**: add `your-domain.com` and
   `www.your-domain.com`.
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

## 5. Point your domain at CloudFront

You said you already own a domain. Two paths depending on where DNS lives:

### If your DNS is in Route 53

1. Route 53 → Hosted zones → your domain.
2. Create record:
   - Record name: (leave blank for the apex, e.g. `your-domain.com`)
   - Type: `A`
   - Toggle **Alias** on
   - Route traffic to: "Alias to CloudFront distribution" → pick yours
3. Repeat for `www` subdomain: same as above but with `www` in Record name.

### If your DNS is at Namecheap / Cloudflare / GoDaddy

Most registrars don't support Alias records, so use CNAMEs:

- `www.your-domain.com` → CNAME → `dxxxxx.cloudfront.net` (your distribution)
- For the apex `your-domain.com`, you'll need either:
  - A registrar that supports "ANAME" or "flattened CNAME" (Cloudflare does), OR
  - Redirect the apex to `www` using your registrar's URL forwarding, OR
  - Move DNS to Route 53 (free to use with your own domain, charges ~$0.50/mo
    per hosted zone).

DNS propagation usually finishes in minutes but can take up to 48 hours.

---

## 6. Your update workflow (use every time you change the site)

Run these from inside the `portfolio-site` folder in PowerShell:

```powershell
aws s3 sync . s3://YOUR-BUCKET/ `
  --delete `
  --exclude "DEPLOYMENT.md" `
  --exclude ".git/*"

# Bust CloudFront's cache so changes appear immediately
aws cloudfront create-invalidation `
  --distribution-id YOUR-DISTRIBUTION-ID `
  --paths "/*"
```

You can find your distribution ID in the CloudFront console. Save both commands
in a `deploy.ps1` PowerShell script so it's one command going forward. A
`deploy.ps1` file is included in this folder — open it, fill in your bucket
name and distribution ID, then run:

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
| `AccessDenied` loading the site | Bucket policy from step 4 didn't get pasted |
| Old CSS showing up | CloudFront cache — run the invalidation command |
| `ERR_CERT_COMMON_NAME_INVALID` | Your cert doesn't cover that hostname, or you hit the cloudfront.net URL from a browser |
| Domain doesn't resolve | DNS hasn't propagated yet, or A/CNAME record points at wrong target |
| Images broken | Path in HTML doesn't match what's in S3 — check case sensitivity |

If you get stuck on any step, paste the error at me and I'll help debug.
