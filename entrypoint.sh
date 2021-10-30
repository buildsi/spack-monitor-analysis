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

spack compiler find
for spec in $(cat ${filename}); do
    if [[ "${use_monitor}" == "true" ]]; then
        printf "spack install --monitor --all --monitor-tag smeagle $spec\n"
        spack install --monitor --all --monitor-tag smeagle "$spec"
        spack analyze --monitor run --analyzer smeagle --recursive --all "$spec"
        printf "spack analyze --monitor run --analyzer smeagle --recursive --all $spec\n"
    else
        printf "spack install --all $spec\n"
        spack install --all "$spec"
        printf "spack analyze run --analyzer smeagle --recursive --all $spec\n"
        spack analyze run --analyzer smeagle --recursive --all "$spec"
    fi
done
