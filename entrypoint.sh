#!/bin/bash

if [ "$#" -eq 0 ]; then
    printf "Please provide a package filename as the only argument.\n"
    exit 1
fi

# Check that file exists
filename="${1}"
if [ ! -f "${filename}" ]; then
    printf "${filename} does not exist!\n"
    exit 1;
fi

# If it's not in the right directory
filedir=$(dirname $filename)
if [ "$filedir" != "specs" ]; then
    printf "$filedir is not in specs, skipping\n"
    exit 0
fi

# Ensure we have SPACKMON_USER/SPACKMON_TOKEN in environment
use_monitor="true"
if [[ -z "${SPACKMON_USER}" ]]; then
    printf "SPACKMON_USER not found in the environment, skipping monitor"
    use_monitor="false"
fi
if [[ -z "${SPACKMON_TOKEN}" ]]; then
    printf "SPACKMON_TOKEN not found in the environment, skipping monitor"
    use_monitor="false"
fi

# Setup spack
. /opt/spack/share/spack/setup-env.sh

# always build with debug!
export SPACK_ADD_DEBUG_FLAGS=true

# Just in case this was not run (but it should have been!)
spack compiler find

# Each filename can have one or more spec names
for spec in $(cat ${filename}); do
    for compiler in $(spack compiler list --flat); do
        if [[ "${use_monitor}" == "true" ]]; then
            printf "spack install --monitor --all --monitor-tag smeagle $spec ${compiler}\n"
            spack install --monitor --all --monitor-tag smeagle "$spec %$compiler"
            printf "spack analyze --monitor run --analyzer smeagle --recursive --all $spec $compiler\n"
            spack analyze --monitor run --analyzer smeagle --recursive --all "$spec %$compiler"
        else
            printf "spack install --all $spec $compiler\n"
            spack install --all "$spec %$compiler"
            printf "spack analyze run --analyzer smeagle --recursive --all $spec $compiler\n"
            spack analyze run --analyzer smeagle --recursive --all "$spec %$compiler"
        fi
    done
done
