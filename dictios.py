from collections import defaultdict
dictios = dict()
alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

## TODO: need dictionary for HOR orientation and pivots ??

if False: # template
  dictios["C"] = defaultdict(lambda: "%")
  dictios["C"].update({ f: t for f, t in zip(alphabets, alphabets) })
  dictios["C"].update({ "AlphaSat": "#", ".": "." })

## Chromosome (1, 5, 19), (13, 21), and (14, 22) are mixing centromeres
## Chromosome 2 and 20 are confusing.


## Chromosome 3
dictios["3"] = defaultdict(lambda: "%")
dictios["3"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["3"].update({ "AlphaSat": "#", ".": "." })

## Chromosome 4
dictios["4"] = defaultdict(lambda: "%")
dictios["4"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["4"].update({ "AlphaSat": "#", ".": "." })
dictios["4"].update({ "H4/9": "H", "H9/": "Q", "A4/9": "A", "X4(E/L)": "x" })

## Chromosome 6
dictios["6"] = defaultdict(lambda: "%")
dictios["6"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["6"].update({ "AlphaSat": "#", ".": "." })
dictios["6"].update({ "T6(M+P)": "t" })

## Chromosome 7
dictios["7"] = defaultdict(lambda: "%")
dictios["7"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["7"].update({ "AlphaSat": "#", ".": "." })
dictios["7"].update({ "G7(E/A)": "g" })

## Chromosome 8
dictios["8"] = defaultdict(lambda: "%")
dictios["8"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["8"].update({ "AlphaSat": "#", ".": "." })
dictios["8"].update({ "L8(D+G)": "l" })

## Chromosome 9
dictios["9"] = defaultdict(lambda: "%")
dictios["9"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["9"].update({
  "H4/": "H", "A4/": "A", "H9/4": "h",
  "N9(D/G)": "N", "S9(C/B)": "S", "U9(G/C)": "U",
  "AlphaSat": "#", ".": "." })

## Chromosome 10
dictios["10"] = defaultdict(lambda: "%")
dictios["10"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["10"].update({ "AlphaSat": "#", ".": "." })
dictios["10"].update({
  'AA': "a", 'AE': "e", 'AG': "g",
  'AB': "b", 'AD': "d", 'AI': "i"})
dictios["10"].update({
  'Y10(F/B)': "y", 'Z10(F/H)': "z",
  'AF10(B/F)': "f", 'AK10(A/G)': "k",
  'AH10(H/B)': "h", 'AJ10(G/E)': "j"})

## Chromosome 11
dictios["11"] = defaultdict(lambda: "%")
dictios["11"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["11"].update({ "AlphaSat": "#", ".": "." })
dictios["11"].update({ "F11(C/D)": "f" })

## Chromosome 12
dictios["12"] = defaultdict(lambda: "%")
dictios["12"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["12"].update({ "AlphaSat": "#", ".": "." })
dictios["12"].update({
  "T12(G/E)":"t", "O12(C/A)":"o", "N12(A/G)":"n",
  "U12(D/H)":"u", "K12(C/A)":"k" })

## Chromosome 15
dictios["15"] = defaultdict(lambda: "%")
dictios["15"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["15"].update({ "AlphaSat": "#", ".": "." })

## Chromosome 16
dictios["16"] = defaultdict(lambda: "%")
dictios["16"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["16"].update({ "AlphaSat": "#", ".": "." })
dictios["16"].update({ "D5/16/19(D1/5/16/19/G/1/5/19)": "d",
  "F16/19": "f", "F1/5/16/19": "g", "A1/5/16/19": "a" })

## Chromosome 17
# 173 mono-reads
# 234,078 monomers in total (~40,027,338 bases)
dictios["17"] = defaultdict(lambda: "%")
dictios["17"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["17"].update({ "AlphaSat": "#", ".": "." })
dictios["17"].update({ f: t for f, t in 
  zip(['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ',
       'AK', 'AL', 'AM', 'AN', 'AO', 'AP17(E/G)', 'AR17(H/J)', 'AS'],
       "abcdefghij" + "klmnoprs")}) 

## Chromosome 18
dictios["18"] = defaultdict(lambda: "%")
dictios["18"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["18"].update({ "AlphaSat": "#", ".": "." })
dictios["18"].update({ "A18/20": "A", "V18(C/A)": "v", "R18(F/H)": "r" })

## Chromosome 20
dictios["20"] = defaultdict(lambda: "%")
dictios["20"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["20"].update({ "AlphaSat": "#", ".": "." })
dictios["20"].update({ "B2/": "b", "A18/": "a", "C2/": "c", "A14/": "d" })

## Chromosome X
dictios["X"] = defaultdict(lambda: "%")
dictios["X"].update({ f: t for f, t in zip(alphabets, alphabets) })
dictios["X"].update({ "AlphaSat": "#", ".": "." })
dictios["X"].update({ "MX(J/H)": "M" })
