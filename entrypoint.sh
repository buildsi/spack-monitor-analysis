#!/bin/bash

if [ "$#" -eq 0 ]; then
    printf "Please provide a package filename and (optionally) an analyzer as arguments.\n"
    exit 1
fi

pkg="${1}"
analyzer="${2:-symbolator}"

# Ensure we have SPACKMON_USER/SPACKMON_TOKEN in environment
use_monitor="true"
if [[ -z "${SPACKMON_USER}" ]]; then
    printf "SPACKMON_USER not found in the environment, skipping monitor\n"
    use_monitor="false"
fi
if [[ -z "${SPACKMON_TOKEN}" ]]; then
    printf "SPACKMON_TOKEN not found in the environment, skipping monitor\n"
    use_monitor="false"
fi

# Setup spack
. /opt/spack/share/spack/setup-env.sh

# always build with debug!
export SPACK_ADD_DEBUG_FLAGS=true

# Just in case this was not run (but it should have been!)
spack compiler find

# Run a build for each pkg spec, all versions
for compiler in $(spack compiler list --flat); do
    if [[ "${use_monitor}" == "true" ]]; then
        printf "spack install --monitor --all --monitor-tag ${analyzer} $pkg ${compiler}\n"
        spack install --monitor --all --monitor-tag "${analyzer}" "$pkg %$compiler"
        printf "spack analyze --monitor run --analyzer ${analyzer} --recursive --all $pkg $compiler\n"
        spack analyze --monitor run --analyzer "${analyzer}" --recursive --all "$pkg %$compiler"
    else
        printf "spack install --all $pkg $compiler\n"
        spack install --all "$pkg %$compiler"
        printf "spack analyze run --analyzer ${analyzer} --recursive --all $pkg $compiler\n"
        spack analyze run --analyzer "${analyzer}" --recursive --all "$pkg %$compiler"
    fi
done
