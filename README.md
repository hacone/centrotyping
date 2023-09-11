
## Prerequisite

- Long read datasets of at least dozens of samples, each with >8x.
- StringDecomposer (and its dependencies)
- python3, datamash, etc

## Workflow

The entire process of centrotyping from long reads to vHOR frequency tables can be broken down into the smaller steps as follows. You can run each script/program one by one, with some appropriate modifications.

### Gather centromeric reads
Please refer to `0_enrich_centromeres.sh`.

### Generation of monoreads
This is delegated to `stringdecomposer` (URL).
Please refer to `1_decompose.sh`.

### Further processing of monoreads
From the decompositions in TSV file, this step gives you python representation of monoreads, and chromosome-specific monoreads in pickle format (serialized python objects).

```bash
python3 2_pickling.py pickle-one SAMPLE.final_decomposition.tsv SAMPLE.pickle
python3 2_pickling.py sort-one SAMPLE.pickle
```

### Extracting vHORs
This is done by running `3_pickle2count.sh`.
Since our definition of vHORs depends on the selection of the pivot monomer,
this script generates a comprehensive vHORs counting for each pivot selection.

### Generating vHORs frequency table
Up to this point, all the process can be done sample by sample, but now we are going to aggregate the data into table format with `4_count_to_csv.sh`.
From the resulted table, centrotypes can be identified via z-normalization & k-mean clustering.

### Centrotyping example code
(TODO)

### Mean vHOR frequencies for centrotype found in Japanese.
(TODO)
