#!/usr/bin/env bash
# run_mocat_gut.sh -- created 2017-05-12 - Renato Alves

set -e
set -o xtrace

NCPU="$1"
SAMPLEFILE=simulated_gut
TIMING=timing-individual

export PERL5LIB="$PERL5LIB:$(pwd)/MOCAT/src"
export PATH="$(pwd)/MOCAT/src:$(pwd)/MOCAT/bin:$PATH"

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -rtf -config\
    &>> logs/rtf_${SAMPLEFILE}.log


# Mapping to 10M gene catalog
/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -s IGC.1 IGC.2 \
    -r reads.processed -extracted_files \
    &>> logs/screen-IGC_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -f IGC.1 IGC.2 \
    -r reads.processed -config filter_psort_buffer=8G -memory 20G \
    &>> logs/filter-IGC_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -p IGC.1 IGC.2 \
    -r reads.processed -mode functional \
    -no_paste -no_horizontal -memory 3G \
    &>> logs/profile-IGC_${SAMPLEFILE}.log
