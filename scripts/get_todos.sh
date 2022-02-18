#!/bin/bash

. ./scripts/clean_repo.sh

for filename in $(find -type f ! -path "./.*/*" | grep -E "(\.py|\.md$)")
do
    
    todos=$(cat $filename | grep -ai "TODO:")
    if [ -n "$todos" ]
    then
        printf "\n$filename\n"
        printf "$todos\n\n"
    fi
    
done
