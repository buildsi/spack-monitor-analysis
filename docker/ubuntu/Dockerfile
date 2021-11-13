ARG gcc_version
FROM ghcr.io/vsoch/gosmeagle as gobase
FROM gcc:${gcc_version}

COPY --from=gobase /usr/local/go/ /usr/local/go/
COPY --from=gobase /src/ /src/
ENV PATH /usr/local/go/bin:/src/:${PATH}

ARG anaconda_url
ENV anaconda_url=${anaconda_url}
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles

RUN apt update -y \
  && apt install -y \
      autoconf \
      automake \
      bzip2 \
      clang \
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
      libtool \
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
      python3-dev \
      rsync \
      unzip \
      wget \
      xz-utils \
      zlib1g-dev \
  && locale-gen en_US.UTF-8 \
  && apt autoremove --purge \
  && apt clean \
  && ln -s /usr/bin/gpg /usr/bin/gpg2 || echo "No gpg" \
  && rm -rf /usr/bin/python \
  && ln -s `which python3` /usr/bin/python || echo "No python 3"


RUN wget https://repo.anaconda.com/archive/${anaconda_url} && \
    bash ${anaconda_url} -p /opt/anaconda3 -b && \
    export PATH=/opt/anaconda3/bin:$PATH && \
    python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install gnureadline boto3 pyyaml pytz minio requests clingo 

ENV PATH=/opt/anaconda3/bin:$PATH
ENV SPACK_ROOT=/opt/spack
    
RUN git clone -b vsoch/db-17 https://github.com/vsoch/spack /opt/spack && \
    cd /opt/spack && \
    . share/spack/setup-env.sh && \
    spack compiler find && \
    spack install libabigail

RUN git clone https://github.com/buildsi/symbolator && \
    cd symbolator && \
    export PATH=/opt/anaconda3/bin:$PATH && \
    python -m pip install .

CMD ["/bin/bash"]

ENV PATH=/opt/anaconda3/bin:/opt/spack/bin:$PATH \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    LANGUAGE=en_US:en \
    LANG=en_US.UTF-8
