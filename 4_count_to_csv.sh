
( cat <<EOL
3 A
4 A
6 A
7 A
8 A
9 A
10 A
11 E
12 A
15 A
16 A
17 G
18 A
X A
EOL
) | while read line; do
  set $line; C=$1 ; PIV=$2
  cat res230614/chr${C}.*.txt | grep HOR-${PIV} | grep -v "#" \
  | datamash crosstab 11, 2 sum 5 | sed -e "s,N/A,0,g;s/^\t/HOR\t/;s/\t/,/g" > CHM13.vHORs.chr${C}-${PIV}.csv
