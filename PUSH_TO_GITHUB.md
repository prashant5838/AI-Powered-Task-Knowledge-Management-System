Pushing this project to GitHub

This document describes how to push the current workspace to the remote repository:

Repository: https://github.com/prashant5838/AI-Powered-Task-Knowledge-Management-System

Choose one of these flows depending on your auth method.

1) Recommended: SSH (if you have SSH keys configured)

Open PowerShell in the workspace root and run:

```powershell
# initialize repo (if not already a git repo)
git init
git add .
git commit -m "Initial commit: AI Task & Knowledge Management MVP"
# add SSH remote (replace if necessary)
git remote add origin git@github.com:prashant5838/AI-Powered-Task-Knowledge-Management-System.git
# push to main (create branch if needed)
git branch -M main
git push -u origin main
```

2) HTTPS with GitHub CLI (recommended if you haven't set SSH keys)

```powershell
# authenticate with gh (one-time)
gh auth login
# then run the same git commands
git init
git add .
git commit -m "Initial commit: AI Task & Knowledge Management MVP"
git remote add origin https://github.com/prashant5838/AI-Powered-Task-Knowledge-Management-System.git
git branch -M main
git push -u origin main
```

3) HTTPS with Personal Access Token (NOT recommended to embed token)

If you must use a PAT, create a remote like:

```powershell
# DO NOT paste tokens into scripts you share
git remote add origin https://<USERNAME>:<PERSONAL_ACCESS_TOKEN>@github.com/prashant5838/AI-Powered-Task-Knowledge-Management-System.git
git push -u origin main
```

Notes
- If the repo already exists with commits, you may need to `git pull --rebase origin main` first and resolve conflicts.
- If you want me to prepare a minimal `.gitignore` or adjust the top-level commit message, tell me and I'll add it.

If you want, run the provided PowerShell helper script: `scripts\push_repo.ps1` (below) which runs the SSH flow.
