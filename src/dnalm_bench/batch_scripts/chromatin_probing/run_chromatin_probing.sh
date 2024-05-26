#!/bin/sh

model=$1
celltype=$2

source /oak/stanford/groups/akundaje/patelas/sherlock_venv/chrombench-new/bin/activate

python -m dnalm_bench.single.experiments.cell_lines.train.$model $celltype