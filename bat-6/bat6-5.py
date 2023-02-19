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

* For the query fasta file
** read in each line
** if the line starts with '>' 
*** strip the '>' asn save in a variable called key
** else
*** store the key and the length of the current line in a dictionary dictionary
* return the dictionary after all lines have been read
* sort the dictionary by values to get only the longest line from the query fasta file

* For the subject fasta file
** read in each line
** if the line starts with '>' 
*** strip the '>' asn save in a variable called key
** else
*** store the key and the length of the current line in a dictionary dictionary
* return the dictionary after all lines have been read
* sort the dictionary by values to get only the longest line from the subject fasta file

* create a result dictionary
* For every entry in the best_alignment dictionary
** if the single key of the longest query line matches
*** add a new entry to the results dictionary with a key of the query gene name and a value of the alignment, evalue tuple

* For every entry in the best_alignment dictionary
** if the single key of the longest subject line matches
*** add a new entry to the results dictionary with a key of the query gene name and a value of the alignment, evalue tuple

* Print out the contents of the result dictionary 
** print each key as the gene that matched
** print each value as the set of best matches

"""

import csv
import sys
import collections
import operator
from Bio import SeqIO


filename = sys.argv[1]
fasta_query = sys.argv[2]
fasta_subject = sys.argv[3]

linecount = 0

alignments = {}

def read_fasta_with_length(filename) :
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    file1.close
    
    fasta = {}
    key = ""

    for line in Lines:
        line = line.strip()
        if line.startswith('>') :
            key = line.replace(">", "")
        else :
            fasta[key] = len(line)
    return fasta


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

# Parse the query FASTA file and store the longest gene for each gene ID
query_records = read_fasta_with_length(fasta_query)
query_longest = {}
for gene_id, gene_length in query_records.items():
    for key, value in best_alignments.items():
        if gene_id == key[0]:
            if gene_id not in query_longest or gene_length > query_longest[gene_id]:
                query_longest[gene_id] = gene_length

sorted_query_longest = collections.OrderedDict(sorted(query_longest.items(), key=operator.itemgetter(1), reverse=True)[:1])
for gene_id, length in sorted_query_longest.items():
    print ("Query longest gene with match in blast file:", gene_id, " (length = ", length, ")")



# Parse the subject FASTA file and store the longest gene for each gene ID
subject_records = read_fasta_with_length(fasta_subject)
subject_longest = {}
for gene_id, gene_length in subject_records.items():
    for key, value in best_alignments.items():
        if gene_id == key[1]:
            if gene_id not in subject_longest or gene_length > subject_longest[gene_id]:
                subject_longest[gene_id] = gene_length

sorted_subject_longest = collections.OrderedDict(sorted(subject_longest.items(), key=operator.itemgetter(1), reverse=True)[:1])
for gene_id, length in sorted_subject_longest.items():
    print ("Subject longest gene with match in blast file:", gene_id, " (length = ", length, ")")


# Get the best matches for each longest gene
best_matches = {}
for keys, values in best_alignments.items():
    for query_id, query_length in sorted_query_longest.items():
        if (query_id == keys[0]):
            if (query_id not in best_matches) :
                best_matches[query_id] = []
                best_matches[query_id].append((keys, values))
            else :
                best_matches[query_id].append((keys, values))

for keys, values in best_alignments.items():
    for query_id, query_length in sorted_subject_longest.items():
        if (query_id == keys[1]):
            if (query_id not in best_matches) :
                best_matches[query_id] = []
                best_matches[query_id].append((keys, values))
            else :
                best_matches[query_id].append((keys, values))


for query_id, matches in best_matches.items():
    if matches:
        print("For gene ", query_id, " the best matches are:")
        for match in matches:
            print("   Match name : (", match[0][0], ",", match[0][1], "), alignment : ", match[1][0], ", evalue : ", match[1][1])

