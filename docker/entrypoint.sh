#!/bin/bash

mkdir -p workspace
cd workspace
conda run -n model-env jupyter notebook --port=8888 --ip=0.0.0.0 --NotebookApp.token= --allow-root
