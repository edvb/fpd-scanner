#!/bin/sh

rm -r workdir
yadage-run workdir workflows/madgraph_simple.yml inputs/input.yml -d initdir=$PWD/inputs &> /dev/null
