"""
Here is the pseudocode

* Read the blast file in line by line with a csv reader that delimits by tab
* for each line that is read
** Extract the qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore as seperate variables from the line by assigning the values in that respective order to the line read which is a list of values
** Create a variable called key which is a tuple of qseqid and sseqid
** create a variable called value which is a tuple of length and evalue
** If the key already exists in the dictionary
*** Append the value to the existing key
** Else
*** Insert the key and value into the dictionary

* Create a new dictionary called unique_alignments
* For each key, value pair in the alignments dictionary, 
** put the value into a python set which removes duplicates automatically
** In the unique alignments dictionary store the key and the set of values as a list

* Create a dictionary called best_alignments
* for each key and value set in unique_alignments
** sort the values first from highest alignment to lowest alignment (this will guarantee the largest alignment tuple is taken when evalues between alignments are the same in the next step)
** sort the result of the previous sort (previous step) lowest evalue to highest evalue
** take only the first tuple from the previous sort (previous step) as the best_value
** store the key and the best_value in the best_alignments dictionary

* use python's built-in sort for dictionary to sort using a lambda (function) that sorts by the items of the dictionary based on the (alignment, evalue) tuple alignment value and keep only the top 5 values
* The sort method takes the dictionary items and uses a lambda that considers the alignment value of each tuple. The sort is done in reverse order so that it gets the largest to the smallest alignments.

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
        value = (int(length), float(evalue))        
        if key in alignments:
            alignments[key].append(value)
        else:
            alignments[key] = [value]

unique_alignments = {}
for key, values in alignments.items() :
    unique_values = set(values)
    unique_alignments[key] = list(unique_values)

best_alignments = {}
for key, values in unique_alignments.items():
    sorted_alignment_values = sorted(values, key=lambda x:x[0], reverse=True)
    best_values = sorted(sorted_alignment_values, key=lambda x:x[1])
    best_value = best_values[0]
    best_alignments[key] = best_value


best_alignments_sorted = dict(sorted(best_alignments.items(), key=lambda x: x[1][0], reverse=True)[:5])

print ("Gene pairs in the five alignments with the largest overlap in the best alignments:")
for key, value in best_alignments_sorted.items():
    print ("Gene pair = ", key, " overlap = ", value[0])

