from collections import Counter, defaultdict
import datetime
from itertools import groupby
import json
import math
import numpy as np
import pandas as pd
import pickle
import re
import sys
import seaborn as sns
import argparse
import dictios

print_log = lambda s: print(f"[{datetime.datetime.now()}]\t{s}", flush = True)

def parse_tab(tabfile):
  tab = pd.read_table(tabfile, header = None)
  return { readname : [q[1] for q in qq] for readname, qq in groupby(
    ((r[1], # readname
      (r[2], # monomer name
       int(r[3]), # rb
       int(r[4]), # re
       float(r[5]), # ident.
       "-" if r[2][-1] == "'" else "+")) # ori
    for r in tab.itertuples()),
    lambda x: x[0] )}

## load chromosome-specificity of monomers
with open("spec-monomers.txt", "r") as f:
  _specs = { m : c for m, s, c in
    [ tuple(l.strip().split('\t')) for l in f.readlines() ]}

def assign_chrom(mrs):
  result = {}
  for rn, monos in mrs.items():
    count = Counter( _specs[n[0].strip("'")] for n in monos )
    total = len(monos)
    total_spec = total - count["NA"]
    if total_spec > 0:
      if count.most_common()[0][0] == "NA":
        most_freq, mfc = count.most_common()[1]
      else:
        most_freq, mfc = count.most_common()[0]
      result[rn] = most_freq
  return result

def counter_entropy(c):
  """ per item entropy """
  n_items  = sum(c.values())
  fs = [ v / n_items for v in c.values() ]
  return sum( -f * np.log2(f) for f in fs )

if __name__ == "__main__":

  ## depths, bases and karyotypes of each sample
  with open("./depth.300-pub.g.txt") as f:
    parsed = [ tuple(l.strip().split(" ")) for l in f ][1:] 
    bases  = { s: int("".join(b.split(","))) for s, d, b, g, k in parsed }
    karyos = { s: "XY" if k == "M" else "XX" for s, d, b, g, k in parsed }
    depths = { s: bases[s] / (3.1*(10**9)) for s in bases }

  parser = argparse.ArgumentParser()
  parser.add_argument("action", choices = ["pickle-one", "show", "sort-one",  "count", "classify"],
    help="sub-command to perform")

  sys.argv.pop(0)
  args = parser.parse_args(sys.argv[:1])
  sys.argv.pop(0)

# configure inputs here.
# `fofn` must be a "file of filename" of "final_decomposition.tsv" generated by stringdecomposer
# `samples` must be a list of samples corresponding to each line of the fofn

  outdir = f"/home/hacone/centromeres/results_sd_0520"
  fofn = "0524-tsv.fofn"
  with open(fofn) as f:
    samples = [ re.sub(".final_.*tsv", "", re.sub(".*0520/", "", l.strip())) for l in f ]
  with open(fofn) as f:
    files = [ l.strip() for l in f ]

  for s in samples:
    assert s in depths, f"depth not available for {s}"
  print_log(f"Processing {len(samples)} samples")

  if args.action == "pickle-one":
    in_tsv = sys.argv[0]
    out_pickle = sys.argv[1]
    monoreads = parse_tab(in_tsv)
    print_log(f"Parsed {in_tsv}")
    pickle.dump(monoreads, open(out_pickle, "wb"), protocol = 3)
    print_log(f"Written {out_pickle}")

  elif args.action == "show":
    assert len(sys.argv), "need pickle path"
    pklfile = sys.argv[0]
    monoreads = pickle.load(open(pklfile, "rb"))
    for rd in monoreads:
      print("\n".join( f"{rd}\t{mon}\t{rb}\t{re}\t{idt:.3f}\t{ori}"
        for mon, rb, re, idt, ori in monoreads[rd] ))
      print("-----", flush = True)

  elif args.action == "sort-one":
    in_pickle = sys.argv[0]
    out_pickle = re.sub(".pkl", "",
                 re.sub(".pickle", "", in_pickle))
    monoreads = pickle.load(open(in_pickle, "rb"))
    print_log(f"Loaded {in_pickle}")
    chrom_assign = assign_chrom(monoreads)
    for chrom in set(chrom_assign.values()):
      selected = { rn: monos for rn, monos in monoreads.items()
       if rn in chrom_assign and chrom_assign[rn] == chrom }
      print_log(f"{len(selected)} reads for chr {chrom}")
      pickle.dump(selected, open(f"{out_pickle}.chr{chrom}.pickle", "wb"))

  elif args.action == "sort":
    for sample, tf in zip(samples, files):
      pklfile = f"{outdir}/{sample}/{sample}.pkl"
      monoreads = pickle.load(open(pklfile, "rb"))
      print_log(f"Loaded {sample}")

      ## TODO: abstract
      chrom_assign = assign_chrom(monoreads)
      print_log(f"\nFound chroms with specific reads in {sample}: { set(chrom_assign.values()) }")
      for chrom in set(chrom_assign.values()):
        selected = { rn: monos for rn, monos in monoreads.items() if rn in chrom_assign and chrom_assign[rn] == chrom }
        print_log(f"{len(selected)} reads for chr {chrom}")
        pickle.dump(selected, open(f"monoreads-pickles/{sample}/{sample}.chr{chrom}.pickle", "wb"))

  elif args.action == "count":

    assert len(sys.argv), "need pickle path"
    pklfile = sys.argv[0]
    chrom = sys.argv[1]
    sample = sys.argv[2]
    monoreads = pickle.load(open(pklfile, "rb"))
    dictio = dictios.dictios[chrom]
    forward_ori = defaultdict(lambda: "+")
    forward_ori.update({"4" :"-", "6":"-", "7":"-", "8":"-"})
    forward_ori.update({"10":"-", "11":"-", "17":"-"})
    forward_ori.update({"16" :"-", "18":"-", "20":"-"})

    get_ori = lambda read: Counter(ori for m, b, e, pct, ori in read).most_common()[0][0]
    gaps = lambda ps: [ ps[i+1][1] - ps[i][2] for i in range(len(ps)-1) ] # gaps from a list of pairs

    cct = Counter()
    chars_list = []
    for rd, ms in monoreads.items():
      cct.update([ m[0].strip("'") for m in ms ])
      gs = [ "-" if g > 10 else "" for g in gaps(ms) ] + [""] # sentinel
      chars = "".join(dictio[m[0].strip("'").strip(chrom)] + gs[i] for i, m in enumerate(ms))
      if get_ori(ms) == forward_ori[chrom]:
        chars = "".join(reversed(chars))
      chars_list += [ chars ] 

    ct = Counter( c for chars in chars_list for c in chars )
    bit_per_mon = counter_entropy(ct)
    n_mons = sum(ct.values())
    b_tot_mon = bit_per_mon * n_mons
    depth = depths[sample]

    print( "               \tSample\tbpm\tn_mons\tTOT")
    print(f"Monomer-Entropy\t{sample}\t{bit_per_mon:.3f}\t{n_mons}\t{bit_per_mon*n_mons:.3f}")

    ## array size estimation
    print(f"Depth\t{sample}\t{depth:.2f}\tchr{chrom}\t", end = "")
    print(f"{n_mons/depth:.2f}\tmonomers =\t{171*n_mons/((1000*1000)*depth):.3f}\tMbp")

    # depth normalize value too!
    print(f"\nRaw Monomers in {chrom} - {sample}")
    print(f"RM#\tSAMPLE\tRank\tn\tn_n\tfq\tCn\tCn_n\tCfq\tMon\tChara")
    s, rc = sum(cct.values()), 0
    for i, (m, c) in enumerate(cct.most_common()):
      rc += c
      print(f"RM\t{sample}\t{i+1}\t", end = "")
      print(f"{c}\t{c/depth:.2f}\t{100*c/s:.3f}\t", end = "")
      print(f"{rc}\t{rc/depth:.2f}\t{100*rc/s:.3f}\t{m}\t{dictio[m.strip(chrom)]}")
    print("-----\n")

    print(f"Interpreted Monomers in {chrom} - {sample}")
    print(f"IM#\tSAMPLE\tRank\tn\tn_n\tfq\tCn\tCn_n\tCfq\tChara")
    s, rc = sum(ct.values()), 0
    for i, (m, c) in enumerate(ct.most_common()):
      rc += c
      # print(f"IM\t{sample}\t{i+1}\t{c}\t{100*c/s:.3f}\t{rc}\t{100*rc/s:.3f}\t{m}")
      print(f"IM\t{sample}\t{i+1}\t", end = "")
      print(f"{c}\t{c/depth:.2f}\t{100*c/s:.3f}\t", end = "")
      print(f"{rc}\t{rc/depth:.2f}\t{100*rc/s:.3f}\t{m}")
    print("-----\n")

    ## TODO: to select good pivot, i'd check spacing of them
    s = sum(ct.values()), 0
    for _pc in ct.most_common(n=20):
      if _pc[1] / sum(ct.values()) < 0.04:
        break # ignore <4% monomers
      pc = _pc[0]
      if pc in "-%#":
        continue # not a monomer...

      hor, n_single, n_none = Counter(), 0, 0
      for chars in chars_list:
        sp = chars.split(pc)
        if len(sp) > 2:
          hor.update( s for s in sp[1:-1] if "-" not in s )
        elif len(sp) == 2: # only one pivot in the read
          n_single += 1
        else: # len(sp) == 1, no pivot in the read
          n_none += 1

      n_encoded = sum((len(k)+1) * v for k, v in hor.items())
      n_units = sum(hor.values())
      n_remain = n_mons - n_encoded
      print(f"Pivot-Test\t{sample}\tchr{chrom}\t{pc}\t", end = "")
      print(f"{n_encoded}\t({100*n_encoded/n_mons:.2f}%)\tmons-in\t{n_units}\t", end = "")
      print(f"{n_encoded/depth:.2f}\t=>\t{n_units/depth:.2f}\t(in depth-normalized)")

      b_remain = n_remain * bit_per_mon
      b_head = sum(len(k)+1 for k in hor) * bit_per_mon
      bit_per_unit = counter_entropy(hor)
      b_hor = n_units * bit_per_unit
      b_tot_hor = b_head + b_hor + b_remain

      print(f"Pivot-Test-E\t{sample}\tchr{chrom}\t{pc}\t", end = "")
      print(f"{b_head:.2f}\thead-bits+\t{bit_per_unit:.2f}\tbpu+\t{b_remain:.2f}\tremaining-bits=>\t", end = "")
      print(f"{b_tot_hor:.2f}\tbits-in-total\t{100 * b_tot_hor / b_tot_mon:.2f}\t% after compression")

      print(f"\nHORs (pivot = {pc}) in {chrom} - {sample}, ", end = "")
      print(f"(any : single : none) = ", end = "")
      print(f"{len(chars_list)-n_single-n_none:,} : {n_single:,} : {n_none:,}")

      s, rc = sum(hor.values()), 0
      print(f"\nHOR-{pc}#\tSAMPLE\tRank\tn\tn_n\tfq\tCn\tCn_n\tCfq\tSize\tHOR")
      for i, (h, c) in enumerate(hor.most_common()):
        rc += c
        print(f"HOR-{pc}\t{sample}\t{i+1}\t", end = "")
        print(f"{c}\t{c/depth:.2f}\t{100*c/s:.3f}\t", end = "")
        print(f"{rc}\t{rc/depth:.2f}\t{100*rc/s:.3f}\t{1+len(h)}\t{pc+h}")

      print("-----\n")
