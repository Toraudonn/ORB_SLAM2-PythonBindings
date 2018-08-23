# How to make patch/diff from git repo and apply it to another different git repo:

Create unidfied diff suitable for `git apply` by `git diff`:

```
git diff tag1..tag2 > mypatch.patch
```

Then you can apply the patch with:

```
git apply mypatch.patch
or
patch -p1 < mypatch.patch
```


### For this project:

[Reference](https://linuxacademy.com/blog/linux/introduction-using-diff-and-patch/)

Without using `git`:

```
diff -u [original directory] [updated directory] > something.diff
```

the `-u` is for unified format (which is more compact).


Applying patches to multiple files:

```
patch -p1 something.diff
```
