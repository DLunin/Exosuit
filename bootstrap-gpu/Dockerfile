FROM nvidia/cuda:10.2-devel-ubuntu18.04

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
	sudo

# Installing prerequisites for Python 3.8

# Enabling source repositories (for build-dep).
RUN sed -i '/deb-src/s/^# //' /etc/apt/sources.list && apt-get update
RUN apt-get update && apt-get build-dep -y python3.8 

# Installing Python 3.8 from source
RUN mkdir -p /opt/python3 && \
	git clone https://github.com/python/cpython.git /opt/python3 && \
	cd /opt/python3 && \
	git reset --hard fa919fdf2583bdfead1df00e842f24f30b2a34bf && \
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
	click==7.0
RUN ln -s $PROJECT_PATH /usr/local/lib/python3.8/site-packages/exosuit

