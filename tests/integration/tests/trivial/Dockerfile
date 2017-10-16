FROM python:2.7

WORKDIR /test

RUN pip install --upgrade pip
# Because installing ansible is so expensive, we do it before any elements of
# the Dockerfile which are likely to change. Docker will cache it.
RUN pip install "ansible>=2.0,<3.0"

ADD tmp_scratch /test
ADD run_sheepdoge.sh /test/run_sheepdoge.sh
ADD assert_e2e_state.sh /test/assert_e2e_state.sh

RUN python setup.py develop

RUN chmod u+x /test/*.sh
