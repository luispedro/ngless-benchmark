#!/usr/bin/env bash
# run_mocat_tara.sh -- created 2017-05-12 - Renato Alves

NCPU="$1"
SAMPLEFILE=tara
TIMING=timing-individual

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -rtf -config\
    &>> logs/rtf_${SAMPLEFILE}.log

# Mapping to ocean catalog
/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -s GORGeCat.95.padded -r reads.processed -extracted_files \
    &>> logs/screen-GORGeCat_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -f GORGeCat.95.padded -r reads.processed -config filter_psort_buffer=8G -memory 20G \
    &>> logs/screen-GORGeCat_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -p GORGeCat.95.padded -r reads.processed -mode functional \
    -no_paste -no_horizontal -memory 3G \
    &>> logs/screen-GORGeCat_${SAMPLEFILE}.log

# Check MOCAT.cfg for which categories to do with functional profiling
# KEGG (kegg exists as ko, pathway, modules in the functional.map file) - doing ko only
# TODO how to do eggnog functional profiling? (eggnog isn't in the functional.map file)?

# Below SpecI
/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -s Ref10MGv9.padded -r reads.processed -extracted_files \
    -no_paste -no_horizontal -memory 3G \
    &>> logs/screen-refmg_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -f Ref10MGv9.padded -r reads.processed -config filter_psort_buffer=8G -memory 20G \
    &>> logs/filter-refmg_${SAMPLEFILE}.log

/usr/bin/time --verbose -ao $TIMING MOCAT.pl -cfg MOCAT.cfg -sf $SAMPLEFILE -cpus "$NCPU" \
    -p Ref10MGv9.padded -r reads.processed -mode gene \
    -no_paste -no_horizontal -memory 3G \
    &>> logs/profile-refmg_${SAMPLEFILE}.log
