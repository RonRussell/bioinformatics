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

* For the query fasta file
** read in each line
** if the line starts with '>' 
*** strip the '>' asn save in a variable called key
** else
*** store the key and the length of the current line in a dictionary dictionary
* return the dictionary after all lines have been read
* store length of query dictionary in query_count variable

* For the subject fasta file
** read in each line
** if the line starts with '>' 
*** strip the '>' asn save in a variable called key
** else
*** store the key and the length of the current line in a dictionary dictionary
* return the dictionary after all lines have been read
* store length of subject dictionary in subject_count variable

* create a query_match_count variable
* For every entry in the alignment dictionary
** for every line in the query file dictionary
*** if the single key of the query line matches the query part of the alignment key
**** increment the query_match_count variable

* create a subject_match_count variable
* For every entry in the alignment dictionary
** for every line in the subject file dictionary
*** if the single key of the subject line matches the subject part of the alignment key
**** increment the subject_match_count variable

print query_match_count / query_count * 100 to get the percent of query FASTA lines that had a match in the BLAST file
print subject_match_count / subject_count * 100 to get the percent of subject FASTA lines that had a match in the BLAST file

"""

import csv
import sys
import collections
import operator

if (len(sys.argv) != 3) :
    print("usage: puthon3 bat6-7.py <blast file name> <query file name> <subject file name>")
    exit(1)

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

query_records = read_fasta_with_length(fasta_query)
query_record_count = len(query_records)

subject_records = read_fasta_with_length(fasta_subject)
subject_record_count = len(subject_records)

query_record_alignments = 0
query_matches = {}
for keys, values in alignments.items():
    for query_id, query_length in query_records.items():
        if (query_id == keys[0]):
            query_record_alignments += 1

subject_record_alignments = 0
subject_matches = {}
for keys, values in alignments.items():
    for subject_id, subject_length in subject_records.items():
        if (subject_id == keys[1]):
            subject_record_alignments += 1

print("Percent of matches for the query file across all alignments : ", (query_record_alignments/query_record_count)*100)
print("Percent of matches for the subject file across all alignments : ", (subject_record_alignments/subject_record_count)*100)


