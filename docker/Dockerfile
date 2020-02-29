ARG cuda_version=10.0
ARG cudnn_version=7

FROM nvidia/cuda:10.0-base-ubuntu16.04

COPY environment.yml /.

RUN apt-get update && apt-get install -y \
	wget \
	vim \
	bzip2

# Install Miniconda
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda.sh && \
	/bin/bash Miniconda.sh -b -p /opt/conda && \
	rm Miniconda.sh

ENV PATH /opt/conda/bin:$PATH

#Install ANACONDA Environment
RUN conda env create -n model-env --file=environment.yml

## Jupyter
#EXPOSE 8888
## Tensorboard
#EXPOSE 6006
#
#ENV PATH "/home/app/.local/bin:$PATH"
#CMD jupyter notebook --port=8888 --ip=0.0.0.0

