FROM ubuntu:18.04

RUN apt-get update && TERM=xterm DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

RUN apt-get update && apt-get install -y \
	bash \
	build-essential \
	software-properties-common \
	make \
	git \
	g++ \
	sed \
	curl \
	sudo \
	vim \
	jupyter \
	tmux

# Enabling source repositories (for build-dep).
RUN sed -i '/deb-src/s/^# //' /etc/apt/sources.list && apt-get update
RUN apt-get update && apt-get build-dep -y python3.7

# Installing Python 3.7 from source
RUN mkdir -p /opt/python3 && \
	git clone https://github.com/python/cpython.git /opt/python3 && \
	cd /opt/python3 && \
	git reset --hard 43364a7ae01fbe4288ef42622259a0038ce1edcc && \
	./configure && \
	make && \
	make install && \
	cd /

RUN pip3 install --upgrade pip

# Installing Docker
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
RUN apt-get update && apt-get install -y \
	docker-ce \
	docker-ce-cli \
	containerd.io

ARG PROJECT_PATH

# Installing Python libraries
RUN pip3 install  \
	colorama==0.4.3 \
	sh==1.12.14 \
	pystache==0.5.4 \
	pyyaml==5.3 \
	docker==4.1.0 \
	click==7.0 \
	wheel==0.33.6 \
	ninja==1.9.0.post1 \
	mkl==2019.0 \
	astor==0.8.1 \
	uncompyle6==3.6.0 \
	anytree==2.7.3 \
	antlr4-python3-runtime==4.7.2 \
	networkx==2.4 \
	pytest==5.3.2 \
	numpy==1.17.4 \
	scipy==1.3.3 \
	matplotlib==3.1.1 \
	pandas==0.25.3 \
	scons==3.1.2 \
	setuptools==42.0.2 \
	pytorch==1.0.2 \
	torchvision==0.5.0 \
	tensorflow==2.1.0 \
	ipython==7.11.1

