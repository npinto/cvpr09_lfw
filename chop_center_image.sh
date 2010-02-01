#!/bin/bash

if [ -z $WIDTH ]; then echo WIDTH not defined; exit 1; fi;
if [ -z $HEIGHT ]; then echo HEIGHT not defined; exit 1; fi;
if [ -z $INPUT ]; then echo INPUT not defined; exit 1; fi;
if [ -z $OUTPUT ]; then echo OUTPUT not defined; exit 1; fi;

shape=($(identify -format "%[fx:w] %[fx:h]" ${INPUT}))

iw=${shape[0]} 
ih=${shape[1]}
xo=$((iw/2-$WIDTH/2))
yo=$((ih/2-$HEIGHT/2))

echo "Running convert $INPUT -draw 'translate $xo,$yo rectangle 0,0 $WIDTH,$HEIGHT' $OUTPUT"

convert $INPUT -draw "translate $xo,$yo rectangle 0,0 $WIDTH,$HEIGHT" $OUTPUT







