#!/usr/bin/env bash
# run_mocat_tara.sh -- created 2017-05-12 - Renato Alves

set -e
set -o xtrace

NCPU="$1"
SAMPLEFILE=tara
TIMING=timing-individual

export PERL5LIB="$PERL5LIB:$(pwd)/MOCAT/src"
export PATH="$(pwd)/MOCAT/src:$(pwd)/MOCAT/bin:$PATH"

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -rtf -config\
    &>> logs/rtf_${SAMPLEFILE}.log

# Mapping to ocean catalog
/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -s OM-RGC.1 OM-RGC.2 OM-RGC.3 OM-RGC.4 OM-RGC.5 OM-RGC.6 OM-RGC.7 OM-RGC.8 \
    -r reads.processed -extracted_files -memory 60G \
    &>> logs/screen-OM-RGC_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -f OM-RGC.1 OM-RGC.2 OM-RGC.3 OM-RGC.4 OM-RGC.5 OM-RGC.6 OM-RGC.7 OM-RGC.8 \
    -r reads.processed -config filter_psort_buffer=8G -memory 60G \
    &>> logs/filter-OM-RGC_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -p OM-RGC.1 OM-RGC.2 OM-RGC.3 OM-RGC.4 OM-RGC.5 OM-RGC.6 OM-RGC.7 OM-RGC.8 \
    -r reads.processed -mode functional \
    -no_paste -no_horizontal -memory 200G \
    &>> logs/profile-OM-RGC_${SAMPLEFILE}.log

# Check MOCAT.cfg for which categories to do with functional profiling
# KEGG (kegg exists as ko, pathway, modules in the functional.map file) - doing ko only

# Below SpecI
/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -s RefMG.v1.padded -r reads.processed -extracted_files \
    -no_paste -no_horizontal -memory 3G \
    &>> logs/screen-refmg_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -f RefMG.v1.padded -r reads.processed -config filter_psort_buffer=8G -memory 20G \
    &>> logs/filter-refmg_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -p RefMG.v1.padded -r reads.processed -mode gene \
    -no_paste -no_horizontal -memory 3G \
    &>> logs/profile-refmg_${SAMPLEFILE}.log
