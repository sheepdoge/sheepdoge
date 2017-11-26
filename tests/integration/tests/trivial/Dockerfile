FROM ubuntu:16.04

WORKDIR /test

RUN apt update
RUN apt install -y python3 python3-apt python3-pip
RUN pip3 install --upgrade pip
# Because installing ansible is so expensive, we do it before any elements of
# the Dockerfile which are likely to change. Docker will cache it.
RUN pip3 install "ansible>=2.0,<3.0"

ADD tmp_scratch /test
ADD run_sheepdoge.sh /test/run_sheepdoge.sh
ADD assert_e2e_state.sh /test/assert_e2e_state.sh

RUN python3 setup.py develop

RUN chmod u+x /test/*.sh
