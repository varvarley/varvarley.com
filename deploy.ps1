# deploy.ps1 — one-command deploy to S3 + CloudFront
# Usage:  .\deploy.ps1
#
# First time only: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

$ErrorActionPreference = "Stop"

# ---- EDIT THESE TWO LINES ----
$Bucket = "varvarley-com-191683921282"
$DistId = "E30R11JNXG15JP"
# ------------------------------

Write-Host "Syncing files to s3://$Bucket ..." -ForegroundColor Cyan
aws s3 sync . "s3://$Bucket/" `
  --delete `
  --exclude "DEPLOYMENT.md" `
  --exclude "deploy.ps1" `
  --exclude "CLAUDE.md" `
  --exclude "DESIGN_PROMPT.md" `
  --exclude "CHANGES_PROMPT.md" `
  --exclude "workpoem.md" `
  --exclude "README.md" `
  --exclude ".git/*" `
  --exclude "InspoPics/*" `
  --exclude "portfolio-site/*"

Write-Host "Invalidating CloudFront cache ..." -ForegroundColor Cyan
aws cloudfront create-invalidation `
  --distribution-id $DistId `
  --paths "/*" | Out-Null

Write-Host "Deployed." -ForegroundColor Green
