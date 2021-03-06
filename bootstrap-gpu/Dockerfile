FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04

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

RUN curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
RUN curl -s -L https://nvidia.github.io/nvidia-docker/$(. /etc/os-release;echo $ID$VERSION_ID)/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
RUN apt-get update && apt-get install -y nvidia-container-toolkit

ARG PROJECT_PATH

# Installing Python libraries
RUN pip3 install colorama==0.4.3
RUN pip3 install sh==1.12.14
RUN pip3 install pystache==0.5.4
RUN pip3 install pyyaml==5.3
RUN pip3 install docker==4.1.0
RUN pip3 install click==7.0
RUN pip3 install torch==1.4.0
RUN pip3 install tensorflow==2.1.0

