#!/bin/bash

if [ -z $WIDTH ]; then echo WIDTH not defined; exit 1; fi;
if [ -z $HEIGHT ]; then echo HEIGHT not defined; exit 1; fi;
if [ -z $INPUT ]; then echo INPUT not defined; exit 1; fi;
if [ -z $OUTPUT ]; then echo OUTPUT not defined; exit 1; fi;

cmd="convert -gravity Center -crop ${WIDTH}x${HEIGHT}+0+0 ${INPUT} ${OUTPUT}"

echo Running $cmd
$cmd

