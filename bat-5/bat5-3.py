import csv
import sys
import re

filename = sys.argv[1]

ref_seq_dict = {}

with open (filename) as file:
	reader = csv.reader(file, delimiter='\t')

	for line in reader:
		if line[0] == "@HD" :
			continue

		if line[0] == "@PG" :
			continue

		if line[0] == "@SQ" :
			sequence = line[1]
			sequence.strip()
			sequence = re.sub(r"^[S][N][:]", "", sequence)
			ref_seq_dict[sequence]=0

		else:
			ref_seq = line[2]
			if (ref_seq != '*' and ref_seq != '0') :
				ref_seq_dict[ref_seq] += 1 

for seq in ref_seq_dict:
 	print (seq,':',ref_seq_dict[seq])
