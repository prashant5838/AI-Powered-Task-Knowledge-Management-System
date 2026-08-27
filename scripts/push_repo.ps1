# PowerShell script to initialize a git repo and push to the provided SSH remote
# Use only if you have your SSH key configured with GitHub

param(
  [string]$remote = 'git@github.com:prashant5838/AI-Powered-Task-Knowledge-Management-System.git',
  [string]$branch = 'main'
)

Write-Host "Initializing git repository in $(Get-Location)"
if(-not (Test-Path .git)){
  git init
} else {
  Write-Host ".git already exists"
}

git add .

# Allow empty commit prevention; only commit if there are staged changes
$staged = git diff --cached --name-only
if([string]::IsNullOrEmpty($staged)){
  Write-Host "No changes staged for commit. Skipping commit."
} else {
  git commit -m "Initial commit: AI Task & Knowledge Management MVP"
}

# set remote if not present
$existing = git remote get-url origin 2>$null
if($LASTEXITCODE -ne 0){
  git remote add origin $remote
} else {
  Write-Host "Origin already set to: $existing"
}

git branch -M $branch
Write-Host "Pushing to origin/$branch..."
git push -u origin $branch

Write-Host "Done. If push failed authenticate via 'gh auth login' or configure your SSH keys."