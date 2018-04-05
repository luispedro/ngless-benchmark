#!/usr/bin/env bash
# run_mocat_gut.sh -- created 2017-05-12 - Renato Alves

set -e
set -o xtrace

NCPU="$1"
SAMPLEFILE=gut
TIMING=timing-individual

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -rtf -config\
    &>> logs/rtf_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -s hg19 -r reads.processed -screened_files \
    &>> logs/screen-hg19_${SAMPLEFILE}.log


# Mapping to 10M gene catalog
/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -s IGC.1 IGC.2 -r reads.processed -extracted_files \
    &>> logs/screen-IGC_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -f IGC.1 IGC.2 -r reads.processed -config filter_psort_buffer=8G -memory 20G \
    &>> logs/screen-IGC_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -p IGC.1 IGC.2 -r reads.processed -mode functional \
    -no_paste -no_horizontal -memory 3G \
    &>> logs/screen-IGC_${SAMPLEFILE}.log


# Below SpecI
/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -s mOTU.v1.padded -r hg19 -identity 97 -extracted_files \
    &>> logs/screen_motus_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -f mOTU.v1.padded -r hg19 -identity 97 -config filter_psort_buffer=2G -memory 5G \
    &>> logs/filter_motus_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -p mOTU.v1.padded -r hg19 -identity 97 -mode mOTU \
    -no_paste -no_horizontal -memory 3G \
    &>> logs/profile_motus_${SAMPLEFILE}.log
