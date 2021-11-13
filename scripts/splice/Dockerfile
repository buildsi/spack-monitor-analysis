FROM ghcr.io/buildsi/spack-ubuntu-20.04:latest

# docker build -t splice-test .

# We MUST have debug for allthings built.
ENV SPACK_ADD_DEBUG_FLAGS=true

# Install ipython and vim for editing stuff and interactive development
RUN apt-get update && apt-get install -y gfortran python3-ipython vim libtool && \
    
    # Add the splicing library - this is my branch that has Nate's fixes pulled
    cd /opt/spack && git fetch && git checkout vsoch/db-17-splice && \
    
    # Let's install libabigail with spack spack
    spack install libabigail

WORKDIR /code
COPY ./splice.py /code/splice.py
ENTRYPOINT ["/bin/bash"]
