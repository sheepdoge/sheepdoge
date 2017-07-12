FROM python:2.7

ADD tmp_scratch /test
ADD run_sheepdog.sh /test/run_sheepdog.sh
ADD assert_e2e_state.sh /test/assert_e2e_state.sh

WORKDIR /test

RUN chmod u+x /test/*.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python setup.py develop
