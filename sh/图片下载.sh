#!/bin/bash
for line in $(cat /Users/liuxulu/Downloads/运营商.txt)
do
  wget $line
done