#!/bin/bash
raspivid -vf -n -w 320 -h 240 -o - -t 0 -b 2000000 | nc 10.0.0.4 5000
