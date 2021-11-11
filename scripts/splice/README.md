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

Note this is a centos image with spack

```bash
$ whereis spack
spack: /opt/spack/bin/spack
```

This is where the spack install is located if you want to try tweaking things and then re-running.
But first run the splice script for curl (already installed)
and zlib (across all versions):

```bash
$ spack python /code/splice.py curl@7.56.0 zlib
```

This is going to concretize this version of curl, and then perform the splices (see [splice.py](splice.py) for how that works
and then prepare to run symbolator -- so first you'll wait for it to install things, and then see installs for each splice. 
The splices are returned successfully, and then we call another function (that I was intending to find associated binaries/libs for)
but oups in the process we find that a spec is missing its install files (zlib should have a libz.so). What I've done is added an IPython embed here
so you can quickly jump into an interactive terminal to look around:

```bash
Splice: zlib@1.2.11%gcc@8.4.1+optimize+pic+shared arch=linux-centos8-skylake
{'text_to_relocate': ['lib/pkgconfig/zlib.pc', 'include/zconf.h', 'include/zlib.h'], 'binary_to_relocate': ['lib/libz.so.1.2.11'], 'link_to_relocate': [], 'other': ['/opt/spack/opt/spack/linux-centos8-skylake/gcc-8.4.1/zlib-1.2.11-msg2n3v2tcijwjo6zwqna3xuxtdvufwt/lib/libz.so', '/opt/spack/opt/spack/linux-centos8-skylake/gcc-8.4.1/zlib-1.2.11-msg2n3v2tcijwjo6zwqna3xuxtdvufwt/lib/libz.a', '/opt/spack/opt/spack/linux-centos8-skylake/gcc-8.4.1/zlib-1.2.11-msg2n3v2tcijwjo6zwqna3xuxtdvufwt/lib/libz.so.1'], 'binary_to_relocate_fullpath': ['/opt/spack/opt/spack/linux-centos8-skylake/gcc-8.4.1/zlib-1.2.11-msg2n3v2tcijwjo6zwqna3xuxtdvufwt/lib/libz.so.1.2.11']}

Splice: zlib@1.2.8%gcc@8.4.1+optimize+pic+shared arch=linux-centos8-skylake
{'text_to_relocate': ['lib/pkgconfig/zlib.pc', 'include/zconf.h', 'include/zlib.h'], 'binary_to_relocate': ['lib/libz.so.1.2.8'], 'link_to_relocate': [], 'other': ['/opt/spack/opt/spack/linux-centos8-skylake/gcc-8.4.1/zlib-1.2.8-sjaltkt5c427kmdn2xvhvoosxrkpumnn/lib/libz.so', '/opt/spack/opt/spack/linux-centos8-skylake/gcc-8.4.1/zlib-1.2.8-sjaltkt5c427kmdn2xvhvoosxrkpumnn/lib/libz.a', '/opt/spack/opt/spack/linux-centos8-skylake/gcc-8.4.1/zlib-1.2.8-sjaltkt5c427kmdn2xvhvoosxrkpumnn/lib/libz.so.1'], 'binary_to_relocate_fullpath': ['/opt/spack/opt/spack/linux-centos8-skylake/gcc-8.4.1/zlib-1.2.8-sjaltkt5c427kmdn2xvhvoosxrkpumnn/lib/libz.so.1.2.8']}

Splice: zlib@1.2.3%gcc@8.4.1+optimize+pic+shared arch=linux-centos8-skylake
{'text_to_relocate': ['include/zconf.h', 'include/zlib.h'], 'binary_to_relocate': [], 'link_to_relocate': [], 'other': ['/opt/spack/opt/spack/linux-centos8-skylake/gcc-8.4.1/zlib-1.2.3-g2h2afoljm6qulxfnyglsupdciqjk6fs/lib/libz.a'], 'binary_to_relocate_fullpath': []}
```

And then you can see the last splice doesn't have libz.so. It will open up an interactive terminal, and `splices` should have all the splices (specs)
and their dependencies (splice.dependencies()) that we loop through above. Look at the script for details!
