FROM ubuntu:16.04

RUN apt update
RUN apt install -y python3 python3-apt python3-pip git

WORKDIR /test

RUN pip3 install --upgrade pip
# Because installing ansible is so expensive, we do it before any elements of
# the Dockerfile which are likely to change. Docker will cache it.
RUN pip3 install "ansible>=2.0,<3.0"

ADD tmp_scratch /test
ADD run_sheepdoge.sh /test/run_sheepdoge.sh
ADD assert_e2e_state.sh /test/assert_e2e_state.sh

RUN python3 setup.py develop

RUN chmod u+x /test/*.sh

# Add the setting which prefers the newly installed python to our system
# to our `.bashrc` file, which we will then source before running the
# sheepdoge command.
RUN echo "export PATH=/usr/local/bin:$PATH" > ~/.bashrc

# Create an executable symlink to `sheepdoge_runner.py` from `/usr/bin/sheepdoge`.
RUN ln -s /test/sheepdoge_runner.py /usr/bin/sheepdoge
RUN chmod u+x /usr/bin/sheepdoge

RUN mkdir /test/kennels

# Pull the most recent version of sheepdoge from git
RUN git clone https://github.com/mattjmcnaughton/kennel-update-kennel-before-cron.git /test/kennels/kennel-update-kennel-before-cron-sample
