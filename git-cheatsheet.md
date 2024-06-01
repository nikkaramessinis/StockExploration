# Git Cheatsheet

### Repository Setup

```bash
# Clone a remote repository
git clone <repo_url>
```
### Working with Branches

```bash
# List all branches (local and remote)
git branch -a

# Create a new branch
git checkout -b <branch_name>

# Switch to a branch
git checkout <branch_name>

# Switch to a remote branch
git checkout -t origin/<branch_name>
# OR
git checkout -b <branch_name> <remote_name>/<branch_name>

# Fetch all remote branches
git fetch
```

### Managing Files

```bash
# Check the status of files/directories
git status

# Add all files to the staging area
git add -A

# Add a single file to the staging area
git add <path/to/file>

# Remove file from the staging area
git reset <path/to/file>

# See changes in the working directory
git diff

# See changes in the staging area
git diff --cached
```

### Committing Changes  

```bash
# Commit changes with a message
git commit -m "message"
```

### Pushing Changes

```bash
# Push changes to the remote repository
git push origin <branch_name>
# OR
git push

# Pull changes from a remote branch
git pull origin <branch_name>

# Pull changes from a remote branch (alternative)
git pull <remote_name> <branch_name>
```

### Viewing History

```bash
# See all commits
git log

# See commits with file changes
git log --stat
```

### Merging

```bash
# Merge another branch into the current branch
git merge <branch_name>
```

### Stashing Changes
```bash
# Stash uncommitted changes
git stash

# Apply the latest stashed changes
git stash apply

# List all stashed changes
git stash list
```

### Resetting and Cleaning

```bash
# Reset committed changes (soft: keep changes, mixed: keep staged, hard: discard everything)
git reset --soft <git commit hash>
git reset --mixed <git commit hash>
git reset --hard <git commit hash>

# Remove all untracked files and directories
git clean -f -d
```