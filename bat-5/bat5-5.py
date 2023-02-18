
# Here is the pseudocode:

# 1. For each line of the file, read the line with a CSV reader and do the following
# 	1. if the line starts with @
# 		1. if the value of the first column is @HD
# 			1. discard it
# 	2. if the value of the first column is @SQ
# 		1. get the value of second colum in the line
# 		2. strip the "SN:" from the start of the value
# 		3. store the remainder of the value as a key in a dictionary with a value of 0
# 	1. if the value of the first column is @PG
# 		2. discard it
# 	2. else (we have an alignment information line)
# 		1. Place the value from column 3 from the line we read into a variable called seq_name
# 		2. Place the value from column 8 from the line we read into a variable called mate_pos
# 		3. If (seq_name does not contain '*' AND does not contain '0") AND (mate_pos is between 1 and 81,000)
# 			1. Increment the dictionary entry whose value matches the variable from column 3 and increment its value (count) by 1
# 2. Print out the contents of the dictionary (by key and value) for any key that contains the string "Zea" to list the reference sequences and their number of reads with a position between 1 and 81,000

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
