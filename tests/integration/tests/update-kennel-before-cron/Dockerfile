FROM python:2.7

RUN apt-get update && apt-get install -y git

ADD tmp_scratch/requirements.txt /test/requirements.txt

WORKDIR /test

RUN pip install --upgrade pip
# Because installing ansible is so expensive, we do it before any elements of
# the Dockerfile which are likely to change. Docker will cache it.
RUN pip install "ansible>=2.0,<3.0"
RUN pip install -r requirements.txt

ADD tmp_scratch /test
ADD run_sheepdog.sh /test/run_sheepdog.sh
ADD assert_e2e_state.sh /test/assert_e2e_state.sh

RUN python setup.py develop

RUN chmod u+x /test/*.sh

# Add the setting which prefers the newly installed python to our system
# to our `.bashrc` file, which we will then source before running the
# sheepdog command.
RUN echo "export PATH=/usr/local/bin:$PATH" > ~/.bashrc

# Create an executable symlink to `sheepdog_runner.py` from `/usr/bin/sheepdog`.
RUN ln -s /test/sheepdog_runner.py /usr/bin/sheepdog
RUN chmod u+x /usr/bin/sheepdog

RUN mkdir /test/kennels

# Pull the most recent version of sheepdog from git
RUN git clone https://github.com/mattjmcnaughton/kennel-update-kennel-before-cron.git /test/kennels/kennel-update-kennel-before-cron-sample
