#/usr/bin/env zsh

NCPU=8

for i in $(seq 3) ; do
    /usr/bin/time -ao timing \
        ngless -j $NCPU --trace --create-report gut.ngl 2>(tee -a log)
    echo >> log
    echo >> timing
done
