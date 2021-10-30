ARG gcc_version
FROM ghcr.io/vsoch/gosmeagle as gobase
FROM gcc:${gcc_version}

COPY --from=gobase /usr/local/go/ /usr/local/go/
COPY --from=gobase /src/ /src/
ENV PATH /usr/local/go/bin:/src/:${PATH}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles

RUN apt update -y \
  && apt install -y \
      autoconf \
      automake \
      bzip2 \
      cpio \
      curl \
      file \
      findutils \
      g++ \
      gcc \
      gettext \
      gfortran \ 
      git \
      gpg \
      iputils-ping \
      jq \
      libffi-dev \
      libssl-dev \
      libxml2-dev \
      locales \
      locate \
      m4 \
      make \
      mercurial \
      ncurses-dev \
      patch \
      patchelf \
      pciutils \
      python3 \
      python3-dev \
      python3-pip \
      rsync \
      unzip \
      wget \
      zlib1g-dev \
      clang \
  && locale-gen en_US.UTF-8 \
  && apt autoremove --purge \
  && apt clean \
  && ln -s /usr/bin/gpg /usr/bin/gpg2 || echo "No gpg" \
  && rm -rf /usr/bin/python \
  && ln -s `which python3` /usr/bin/python || echo "No python 3"

RUN python3 -m pip install --upgrade pip setuptools wheel \
 && python3 -m pip install gnureadline boto3 pyyaml pytz minio requests \
 && python3 -m pip install clingo || apt-get install -y gringo \
 && rm -rf ~/.cache

ENV SPACK_ROOT=/opt/spack
    
# This might be too slow to run
RUN git clone -b vsoch/db https://github.com/vsoch/spack /opt/spack && \
    cd /opt/spack && \
    . share/spack/setup-env.sh && \
    spack compiler find

CMD ["/bin/bash"]

ENV PATH=/opt/spack/bin:$PATH \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    LANGUAGE=en_US:en \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8
