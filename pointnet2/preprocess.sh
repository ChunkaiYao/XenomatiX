#!/bin/sh

cd xenomatix_utils/meta
python generate_meta.py 
cd ..
python collect_data.py
