# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# spack python splice.py specA specB

import os
import sys

import spack.binary_distribution as bindist
import spack.rewiring
from spack.spec import Spec

# Plan of action
# discover spack package already in container (e.g., here we have curl)
# based on that version, run splices and symbolator predictions (maybe libabigail too?)
# save it somewhere, compare predictions to actual MATRIX!


def splice_all_versions(specA_name, specB_name, transitive=True):
    """
    Perform a splice with a SpecA (a specific spec with a binary),
    and SpecB (the high level spec that is a dependency that we can test
    across versions).

    spack python splice.py curl@7.56.0 zlib
    """
    print("Concretizing %s" % specA_name)
    specA = Spec(specA_name).concretized()
    specA.package.do_install(force=True)

    # Return list of spliced specs!
    splices = []

    # The second library we can try splicing all versions
    specB = Spec(specB_name)
    for version in specB.package.versions:
        splice_name = "%s@%s" % (specB_name, version)
        print("Testing splicing in %s" % splice_name)
        dep = Spec(splice_name).concretized()
        dep.package.do_install(force=True)
        spliced_spec = specA.splice(dep, transitive=transitive)

        # Exit early and tell the user if there was a splice issue
        # This would probably need a bug report
        if specA is spliced_spec or specA.dag_hash() == spliced_spec.dag_hash():
            sys.exit("There was an issue with splicing!")
        spack.rewiring.rewire(spliced_spec)

        # check that the prefix exists
        if not os.path.exists(spliced_spec.prefix):
            sys.exit(
                "%s does not exist, so there was a rewiring issue!"
                % spliced_spec.prefix
            )
        splices.append(spliced_spec)

    return splices


def run_symbolator(splices, spliced_lib):
    """
    Run symbolator python to generate corpora and predictions
    """
    for splice in splices:
        # Explicitly get the binaries
        manifest = bindist.get_buildfile_manifest(splice.build_spec)

        # Set of things to run symbolator on
        binaries = set()
        for contender in manifest.get("binary_to_relocate"):
            if contender.startswith("bin"):
                binaries.add(contender)

        for dep in splice.dependencies():
            if dep.name == spliced_lib:
                # TODO: this seems to be a bug - there is no libz.so in the manifest!
                # and indeed it doesn't exist on the system, and ldd doesn't find it
                manifest = bindist.get_buildfile_manifest(dep.build_spec)
                print("\nSplice: %s" % dep)
                print(manifest)

    print()
    import IPython

    IPython.embed()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage:\nspack python splice.py curl@7.56.0 zlib")
    splices = splice_all_versions(sys.argv[1], sys.argv[2])

    # For splices, run symbolator!
    run_symbolator(splices, sys.argv[2])
