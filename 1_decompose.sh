## path to stringdecomposer
SD=$PWD/stringdecomposer
PARAM="-i 90 --ed_thr 18"
MONOMERS=$PWD/resources/Mon_ISMB2021.fa

## directory in which results will be written
RESDIR=$PWD/SD_results/

## list of "sample-name" and "encen_reads.fa"
( cat <<EOL
sample1 encen_sample1.fa
sample2 encen_sample2.fa
EOL
) | while read line; do
    set $line ; SAMPLE=$1 ; READS=$2
    mkdir -p $RESDIR/${SAMPLE}
    $SD/bin/stringdecomposer -t 4 ${PARAM} ${READS} ${MONOMERS} -o ${RESDIR}/${SAMPLE}
done
