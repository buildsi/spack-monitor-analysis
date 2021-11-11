FROM ghcr.io/buildsi/pkg-curl-7.54.0-centos-8-gcc-8.4.1:2021-11-11

# docker build -t splice-test .

# Install ipython and vim for editing stuff and interactive development
RUN yum install -y python3-ipython vim && \

    # Add the splicing library - this is my branch that has Nate's fixes pulled
    cd /opt/spack && git fetch && git checkout vsoch/db-17-splice
WORKDIR /code
COPY ./splice.py /code/splice.py
ENTRYPOINT ["/bin/bash"]
