#/usr/bin/env zsh

NCPU=8
NREPLICATES=3

set -e

function remove_data_dirs {
    rm -rf SAMEA*
}

function create_data_dirs {
    for folder in ../data/$1/SAMEA* ; do
        echo $folder
        mkdir $(basename $folder)
        for file in $folder/* ; do
            ln -s ../$file $(basename $folder)/$(basename $file | sed 's/\(.*\)_\([0-9]\)\.fastq\.gz/\1.\2.fq.gz/')
        done
    done
}

mkdir -p logs

for repl in $(seq $NREPLICATES) ; do
    for samplefile in gut tara; do
        echo Doing ./run_mocat_${samplefile}.sh $NCPU replica $repl
        # Create the data folders
        create_data_dirs $samplefile

        echo $samplefile $repl >> log
        echo $samplefile $repl >> timing
        /usr/bin/time --verbose -ao timing \
            ./run_mocat_${samplefile}.sh $NCPU | tee -a log
        echo >> log
        echo >> timing

        remove_data_dirs
    done
done
