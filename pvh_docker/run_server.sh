#!/bin/bash

source /opt/conda/bin/activate
conda activate baobab
cd $HOME/baobablims
bin/instance start

sleep 1000000
