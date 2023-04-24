#!/bin/bash

MAX_SIZE=10000000
find . -type f -size +${MAX_SIZE}c -print >> .gitignore