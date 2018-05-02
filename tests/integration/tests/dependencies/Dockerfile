FROM ubuntu:18.04

WORKDIR /test

RUN apt update
RUN apt install -y python3 python3-apt python3-pip ansible

# Configure `update-alternatives` to use python3 by default.
RUN update-alternatives --install /usr/bin/python python /usr/bin/python2 0
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 0

ADD tmp_scratch /test
ADD run_sheepdoge.sh /test/run_sheepdoge.sh
ADD assert_e2e_state.sh /test/assert_e2e_state.sh

RUN chmod u+x /test/*.sh
