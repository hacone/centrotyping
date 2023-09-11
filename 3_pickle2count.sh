## counting monomers/HORs from sorted pickles

# StringDeomposer -> pickle -> sort -> (THIS SCRIPT) -> CSV

RESULT_DIR=./counts_dir/
mkdir -p ${RESULT_DIR}

## 14 chromosomes
for C in 3 4 6 7 8 9 10 11 12 15 16 17 18 X; do

  ## this is an example
  for S in sampleA sampleB sampleC ; do

    ## NOTE: please specify the path to pickles
    PKL=/path/to/$S/$S.chr${C}.pickle

    echo "processing $C for $S "`date`
    python3 pickling.py count ${PKL} ${C} ${S} > ${RESULT_DIR}/chr${C}.${S}.txt

  done # sample loop
done # chrom loop
