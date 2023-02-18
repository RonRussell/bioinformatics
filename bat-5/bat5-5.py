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
			seq_name = line[2]
			mate_pos = line[7]
			if ((seq_name != '*' and seq_name != '0') and (1 <= int(mate_pos) <= 81000)):
				ref_seq_dict[seq_name] += 1 

for seq in ref_seq_dict:
	if (seq.lower().find('zea') >= 0) :
 		print (seq,':',ref_seq_dict[seq])
