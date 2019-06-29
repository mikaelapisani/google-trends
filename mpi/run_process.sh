#!/bin/bash

. $HOME/conda/etc/profile.d/conda.sh
conda activate
if [[ $# -eq 1 ]]; then
   category=$1
   python $HOME/google-trends/main.py -c $HOME/google-trends/config.properties --process=true --num_category=$1
else
   echo "You need to input the category number to be processed"
fi

