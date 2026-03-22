# Git Good

_Tips and tricks for using [Git](https://git-scm.com/)._

# Splitting a commit in two

## Problem

Have:

```
  a2c
a --> c
      ^
 YOU ARE HERE
```

Want:

```
  a2b   a2c
a --> b --> c
```

## Solution

1. Commit `c2b`:

   ```
     a2c   c2b
   a --> c --> b
               ^
        YOU ARE NOW HERE
   ```

   Record its hash using `C2B_HASH=$(git rev-parse HEAD)`.

2. Squash `c2b` into `a2c`:

   ```sh
   git reset --soft HEAD~2
   git commit -m "a2b"
   ```

   This can also be achieved using an interactive rebase (`git rebase -i HEAD~2`).

3. Create new commit `b2c`:

   ```sh
   git revert --no-commit $C2B_HASH
   git commit -m "b2c"
   ```
