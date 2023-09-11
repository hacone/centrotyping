#!/bin/bash

export MM2=minimap2.24
export SAMTOOLS=samtools1.16
export SEQKIT=seqkit

export CEN_HOR=$PWD/resources/Hum3HOR.fa

function en_centromere() {
  READS=$1
  BN=$( basename $READS )
  BN=${BN%%.fa.gz} ; BN=${BN%%.fq.gz}
  BN=${BN%%.fa} ; BN=${BN%%.fq}

  cd $( dirname $READS )
  echo "Collect reads for centromere: $READS"

  PARAMS="-Hk12 -t4 -a --sam-hit-only"
  $MM2 ${PARAMS} ${CEN_HOR} ${READS} | $SAMTOOLS view -b -T ${CEN_HOR} > ${BN}_cen.bam
  $SAMTOOLS fasta ${BN}_cen.bam | $SEQKIT seq -w 120 > encen_${BN}.fa
}; export -f en_centromere;

## full paths to the directory
READS_DIR=/path/to/reads_dir
ls $READS_DIR/*.fastq.gz | xargs -P6 -I% -n1 /bin/bash -c "en_centromere %"

## Or, specify the read file.
READS=/path/to/reads.fastq.gz
en_centromere $READS
