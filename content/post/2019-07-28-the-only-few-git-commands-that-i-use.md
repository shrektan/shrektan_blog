---
title: The only few Git commands that I use
author: Xianying Tan
date: '2019-07-28'
slug: the-only-few-git-commands-that-i-use
categories:
  - en
tags:
  - git
  - programming
  - tech  
---

Git is great but quite complicated to fully master[^books]. Fortunately, being familiar with a few commands is usually enough. Here's basically all the git commands that I use.

(First of all, I need to claim that I prefer using a GUI. I either use RStudio's Git panel or Git's GUI.)

## Clone

1. `git clone {git-url} {local-folder}`: clone a remote repository to local

## Branch

1. `git checkout {branch-name}`: checkout to a branch
1. `git checkout -b {new-branch-name}`: create a new branch and checkout to it
1. `git branch -d {branch-name}`: delete a local branch (should use `-D` if the branch hasn't been merged)
1. `git merge {another-branch}`: merge the content of another branch to the current branch 

## Repository

1. `git remote -v`: display all the remote repository
1. `git remote add/rm {repo-alias} {git-url}`: add or remove a remote repository

## Local - Remote

1. `git fetch {repo-alias}`: fetch the content from the remote repository
1. `git push {repo-alias} {branch-name}`: push the local content to remote
1. `git push -u {repo-alias} {branch-name}`: push and set the remote branch as the upstream, which means you don't have to specify the remote repo and branch when using `git pull` and `git push` later
1. `git pull {repo-alias} {branch-name}`: equals to `git fetch` first then `git merge {repo-alias/branch-name}`

## Commit

1. `git commit -a -m "your message"`: commit all the code changes with a message.

## Clean up

```bash
git branch -d $(git branch --merged=master | grep -v master)
git fetch --prune
```

## Advanced

1. `git reset --hard HEAD~n`: discard the last n commits *hardly*. `--hard` means reverting to the previous status. Often used when you think your last n commits are nonsense.
1. `git reset --soft HEAD~n`: discard the last n commits *softly*. `--soft` means keeping the changes. Often used when you want to squash the commits or remove the just-unintentionally-included files.
1. `git merge --abort`: imagine you pull from the upstream and a CONFLICT happens. You can solve the conflict but you may also consider to abort the merge. This command allows to abort the current merge.
1. `git rebase --onto master B C`: (Well, frankly speaking, I'm writing this article because of this command) Often used when you made a commit, which should have been committed on another branch. So you need to *rebase* the commit.    
   Let's say you are working on the `D` branch, developping a cool new feature. You need to use an existing function but find a bug inside. The *correct* procedure is: `git checkout master`, modify the code, commit, `git checkout D` and `git merge master` to have the fix on `D`. 
   Remember that you are immersed in developping the new feature (good programmers do) so there's a chance you simply commit the fix on `D` and go. After a few more commits on `D`, you realize the previous commit should have been played on the branch `master`.  
   You have three options now. The first is to `git revert --soft` all the previous commits and re-commit the work except the fix. The good commit history may not be well preserved. Another option is to re-do the fix on the `master` branch but you may find conflicts when branch `D` gets merged. The last option (usually the best) is to `git rebase master B C`, where `B` and `C` stands for the SHA-1 strings[^sha] of last commit *before* the fix and *of* the fix.   
   You may find [`git rebase`'s documentation](https://git-scm.com/docs/git-rebase) useful (I admit I don't really know how to *interactively* play with `git rebase` and the above command is the only one I use).
1. `git clean -df && git checkout .` to discard all local file changes. This is useful when you add / edit lots of local files and want to completely discard all your wasted efforts.
   
## Misc

Well that's not *literally* all. I may use `git config` (first time set-up on the new computer), `git tag` (tag a version) and `git status` (when I have to [disable the Git function in RStudio for one project, due to the anti-virsus issue](https://github.com/rstudio/rstudio/issues/4368)).

[^books]: Two books I recommend on Git. The Git related chapter of Hadley's [R packages](http://r-pkgs.had.co.nz) is well-written and a great place to get your hands dirty. To get a deeper understanding of Git, [Pro Git book](https://git-scm.com/book) is the best choice.

[^sha]: You can think SHA-1 strings are the unique names of each commit. They're the "non-sense" strings displayed in RStudio's Git Panel (the last column with the name SHA). You can also see them by executing `git log`.

## References

- Florent Destremau, [A simple way to clean up your git project branches](https://medium.com/@FlorentDestrema/a-simple-way-to-clean-up-your-git-project-branches-283b87478fbc)
