#!/bin/bash

xxd -r data.txt > filename
mkdir tempDir


function main(){

 fileType=$(file $1 | cut -d ' ' -f2)
 echo $fileType
 if [[ "$fileType" == "gzip" ]]; then
        # Rename the file
        mv filename file.gz
        gzip -d < file.gz > filename
        main filename
 elif [[ "$fileType" == "bzip2" ]]; then 
        mv filename file.bz2
        bzip2 -d < file.bz2 > filename
        main filename
 elif [[ "$fileType" == "POSIX" ]]; then
        tar -xf filename -C tempDir
        rm filename
        cd tempDir
        for file in *; do
                mv $file filename
                mv filename ..
                cd ..
        done
        main filename
 elif [[ "$fileType" == "ASCII" ]]; then
        cat filename
        exit
 else
        echo "Format incorrect"
 fi

}
main filename
