# Spack Monitor Analysis

This repository will host docker base images for interacting with the development
spack monitor, and for building and deploying:

 - across packages
 - across versions
 - across operating systems
 
It's also setup to handle architectures, but we need to host runners to do that.
I'm not sure if this will all work, but it sounded fun to try.

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
