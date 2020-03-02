#!/bin/bash

mkdir -p workspace
cd workspace
conda activate model-env
jupyter notebook --port=8888 --ip=0.0.0.0 --NotebookApp.token=