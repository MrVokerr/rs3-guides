# Requires: Python 3.10+, Node.js, npm, wrangler (logged in or CLOUDFLARE_API_TOKEN set)
# Schedule in Windows Task Scheduler: daily at 9:00 AM, trigger timezone Pacific.

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

Write-Host "==> Refreshing GE prices..."
python "$RepoRoot\scripts\update-money-making-prices.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Building site..."
npm run docs:build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Deploying to Cloudflare Pages..."
npx wrangler pages deploy .vitepress/dist --project-name=rs3-guides --branch=main
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Done."
