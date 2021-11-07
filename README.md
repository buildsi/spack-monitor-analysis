# Spack Monitor Analysis

This repository will host docker base images for interacting with the development
spack monitor, and for building and deploying:

 - across packages
 - across versions
 - across operating systems
 
It's also setup to handle architectures, but we need to host runners to do that.
I'm not sure if this will all work, but it sounded fun to try.

## Instructions

### Building base containers

The base containers are built with the following GitHub workflows:

 - [.github/workflows/gcc-matrices.yaml](.github/workflows/gcc-matrices.yaml): builds gcc base images with spack, smeagle, and symbolator, across gcc versions
 - [.github/workflows/build-deploy.yaml](.github/workflows/build-deploy.yaml): builds the same across ubuntu, centos, and a fedora container, each with a few compilers.
 
To run any of these updates, simply push to a branch, navigate to the "Actions" tab, and then select either of the two workflows:

 - GCC Build Matrices
 - Build Containers
 

And click "Run workflow" and select the branch to trigger. The finished containers will then be pushed to GitHub packages and ready
for use by the analysis pipeline.

### Updating base containers

To do any analysis, we split jobs into operating system (containers) by compilers (also in containers). To get the maximum out of each 6 hour run, we generate a matrix of container and compiler combinations by way of a simple Python script. For example, a base container should be built with a label of:

```bash
compiler_labels=gcc@7.5.0,gcc@9.5.0
```

And then we can programatically discover this set of labels via the image config from the packages registry, and run a script
to parse these labels!

```bash
$ python scripts/generate-matrix.py 
::set-output name=containers::[["ghcr.io/buildsi/spack-ubuntu-18.04", "all"], ["ghcr.io/buildsi/spack-ubuntu-20.04", "all"], ["ghcr.io/buildsi/spack-centos-7", "all"], ["ghcr.io/buildsi/spack-centos-8", "all"], ["ghcr.io/buildsi/spack-fedora", "all"], ["ghcr.io/buildsi/ubuntu:gcc-8.1.0", "all"], ["ghcr.io/buildsi/ubuntu:gcc-7.3.0", "all"], ["ghcr.io/buildsi/ubuntu:gcc-9.4.0", "all"], ["ghcr.io/buildsi/ubuntu:gcc-11.2.0", "all"], ["ghcr.io/buildsi/ubuntu:gcc-4.9.4", "all"], ["ghcr.io/buildsi/ubuntu:gcc-10.3.0", "all"]]
```

So if you need to add a new container base, add the name in the script [scripts/generate-matrix.py](scripts/generate-matrix.py).
If a container does not have compiler labels, then the label "all" is used, and the compilers are programatically discovered in the container.
This can work okay for smaller packages, but for long package builds across versions and compilers, we typically go over the 6 hour limit.


### Running an Analysis

The install and analysis for a package across versions with some set of compilers is done with:

 - [.github/workflows/analysis.yaml](.github/workflows/analysis.yaml) 

The trigger is also a dispatch event, except you need to also enter the package name and analyzer to run.

![img/analysis.png](img/analysis.png)

Analyses are uploaded to spack monitor.

## Analysis Plan

This is what I'm planning to do for a "base level" analysis. The goal is to understand the build space (what builds and what doesn't across packages and compilers, limited by spack) and then to simulate splices, and predict working / not working for each. Then when Nate's splicing
is working, we can validate our predictions.

The container bases here are mostly done, and will be launchable with a dispatch event,
meaning you will just need to enter the package name (from spack) into a UI and press a button.
This will work by way of using each base (an operating system with a few compilers, a customized
version of spack, and analyzers installed) to do the following steps.

### Step 1. Analysis to happen in GitHub Actions:

After a dispatch event for package P:

```
For operating systems in ubuntu-18.04, ubuntu-20.04, centos-7, centos-8, fedora:
    for compiler C in a handful of gcc versions and clang in each:
         build package P
         for each of P
              install P with C, send result to monitor
              run spack analyze with symbolator, send result to monitor
```

The above will send a bunch of builds across these variables, and symbolator results
to spack monitor, where they can be interacted with via the UI and API.
We can then do this a bunch of times for some set of packages, and then do analysis.

Analysis enabled by spack monitor database:

```
For a package query, P
    Find all species associated with package, specs (can have varying compilers, etc.)
        Pin a spec A, specA
        For all dependents of A (not limited to built with) choose a specB
        Run symbolator splice with specA to get undefined symbols USA
        Run symbolator splice with specB spliced into SpecB to get another set of undefined symbols USB
        Take diff between USA and USB, if any undefined not previously there, the splice will not work. Otherwise, yes.
```

This second part, doing a splice, will also be a UI view to do interactively.
This data should also be download-able via the API, so the analysis can be done programmatically.
When Nate splicing is available we can hopefully validate some of our splicing predictions. Then
at least we have a base set - making predictions about ABI compatibility based on the lowest, simplest
level of attribute that we have, the symbol. Further work should improve upon that. Or if it's already
very good, we don't have any more to do! :P
