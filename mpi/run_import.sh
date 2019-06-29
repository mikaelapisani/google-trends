#!/bin/bash

. $HOME/conda/etc/profile.d/conda.sh
conda activate
python $HOME/google-trends/main.py -c $HOME/google-trends/config.properties --import=true