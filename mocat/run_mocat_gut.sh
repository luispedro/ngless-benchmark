#!/usr/bin/env bash
# run_mocat_gut.sh -- created 2017-05-12 - Renato Alves

set -e

NCPU="$1"
SAMPLEFILE=gut
TIMING=timing-individual

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -rtf -config\
    &>> logs/rtf_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -s hg19 -r reads.processed -screened_files \
    &>> logs/screen-hg19_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -s 263MetaRef10MGv9.cal.v2.nr.padded -r hg19 -identity 97 -extracted_files \
    &>> logs/screen_motus_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -f 263MetaRef10MGv9.cal.v2.nr.padded -r hg19 -identity 97 -config filter_psort_buffer=2G -memory 5G \
    &>> logs/filter_motus_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -p 263MetaRef10MGv9.cal.v2.nr.padded -r hg19 -identity 97 -mode mOTU \
    -no_paste -no_horizontal -memory 3G \
    &>> logs/profile_motus_${SAMPLEFILE}.log
