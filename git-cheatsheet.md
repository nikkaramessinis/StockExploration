# Git Cheatsheet

### clone a repo
```git clone <repo_url>```

### Check the status of files/dirs
```git status```

### create a new branch
```git checkout -b <branch_name>```

### switch to a branch
```git checkout <branch_name>```

### switch to a remote branch
```git checkout -t origin/<branch_name>```

OR 

```git checkout -b <branch_name> <remote_name>/<branch_name>```

### fetch all remote branches
```git fetch```

### add files to commit
- This will add all the files in the current directory:

```git add -A```

- To add a single file

```git add <path/to/file>```

### commit changes

```git commit -m "message"```

### push changes
```git push origin master```

OR

```git push```

### pull changes from a branch
```git pull origin <branch_name>```

### See what you have changed
```git diff```

- if you have added the files using `git add` command then

```git diff --cached```

### See all the commits
```git log```

### pull changes from a remote branch
```git pull <remote_name> <branch_name>```

### merge two branches
```git merge <branch_name>```

### See all the branches
```git branch -vva```

### stash changes
```git stash```

### unstash changes
```git stash apply```

### reset changes
```git reset```

### remove all local changes (new dirs, files, etc)
```git clean -f -d```