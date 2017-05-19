#/usr/bin/env zsh

NCPU=8
NREPLICATES=3

set -e

for script in gut.ngl ocean.ngl; do
    for repl in $(seq $NREPLICATES) ; do
        echo $script $repl >> log
        for i in $(seq 3) ; do
            echo $script $repl $i >> log
            echo $script $repl $i >> timing
            /usr/bin/time --verbose -ao timing \
                ngless -j $NCPU --trace --create-report $script | tee -a log
            echo >> log
            echo >> timing
        done
        rm -rf ngless-locks ngless-partials ngless-stats
    done
done
