"""
Here is the pseudocode

* Read the blast file in line by line with a csv reader that delimits by tab
* for each line that is read
** Increment a line counter
** Extract the qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore as seperate variables from the line by assigning the values in that respective order to the line read which is a list of values
** Create a variable called key which is a tuple of qseqid and sseqid
** create a variable called value which is a tuple of lenght and evalue
** If the key already exists in the dictionary
*** Append the value to the existing key
** Else
*** Insert the key and value into the dictionary

* Create a new dictionary call unique_alignments
* For each key, value pair in the alignments dictionary, 
** put the value into a python set which removes duplicated
** In the unique alignments dictionary store the key and the set of values as a list

* Create a variable called unique_alignment_count
* For each key, value pair in the unique_alignments dictionary, 
** increment unique_alignment_count by the number of values for that key in the dictionary


* print out the total number of lines
* print out the number of keys in unique_alignments
* print out the number of unique alignment values in unique_alignments

"""

import csv
import sys

filename = sys.argv[1]

linecount = 0

alignments = {}

with open (filename) as file:
    reader = csv.reader(file, delimiter='\t')

    for line in reader:
        linecount += 1
        qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore = line
        key = (qseqid, sseqid)
        value = (length, evalue)        
        if key in alignments:
            alignments[key].append(value)
        else:
            alignments[key] = [value]

unique_alignments = {}
for key, values in alignments.items() :
    unique_values = set(values)
    unique_alignments[key] = list(unique_values)

unique_alignment_count = 0
for key, values in unique_alignments.items() :
    unique_alignment_count += len (unique_alignments[key])


print ("Total lines in blast file: ", linecount)
print ("Total number of unique alignment qsequid, ssequid pairs: ", len(unique_alignments.keys()))
print ("Total number of unique alignment values for all qsequid, ssequid pairs: ", unique_alignment_count)

