# Testing Splicing

This is a testing ground for splicing! Currently it reproduces a bug Nate and I
are working on. Instructions to reproduce are the following:

## Build the container

Name it whatever you like.

```bash
$ docker build -t splice-test .
```

Now shell into the container (the entrypoint is bash)

```bash
$ docker run -it splice-test
```

If you want to bind the script to change/update and run again:

```bash
$ docker run -it -v $PWD:/code splice-test
```

```bash
$ which spack
/opt/spack/bin/spack
```

This is where the spack install is located if you want to try tweaking things and then re-running.
Let's rum the splice script for curl and zlib (across all versions):

```bash
                         # binary  # splice # command
$ spack python splice.py curl@7.56.0 zlib spliced.json curl --head https://linuxize.com/
```

This is going to concretize this version of curl, and then perform the splices (see [splice.py](splice.py) for how that works
and then prepare to generate predictions:

1. symbolator: will make predictions based on symbol sets
2. libabigail: makes predictions based on corpora diffs (and an internal representation)

And then the actual "does it work" is determined from running the original executable.

