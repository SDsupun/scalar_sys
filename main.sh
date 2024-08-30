#!/bin/bash

SCALAR_WD="./"
export SCALAR_WD
libreoffice --invisible &
./
python main.py