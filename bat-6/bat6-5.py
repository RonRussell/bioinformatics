"""
To get the name of the longest gene in each FASTA file that has an alignment in the BLAST 
file, as well as the name(s) of its best match(es), you can use the following Python code:
"""

from Bio import SeqIO

# Parse the query FASTA file and store the longest gene for each gene ID
query_records = SeqIO.to_dict(SeqIO.parse('/scratch/mrmckain/Bioinformatics_Class/BATs/BAT_6_Combining_FASTA_and_BLAST/Gene_models_2.fasta', 'fasta'))
query_longest = {}
for gene_id, record in query_records.items():
    if gene_id in unique_alignments:
        if gene_id not in query_longest or len(record) > len(query_longest[gene_id]):
            query_longest[gene_id] = record

# Parse the subject FASTA file and store the longest gene for each gene ID
subject_records = SeqIO.to_dict(SeqIO.parse('/scratch/mrmckain/Bioinformatics_Class/BATs/BAT_6_Combining_FASTA_and_BLAST/Gene_models_1.fasta', 'fasta'))
subject_longest = {}
for gene_id, record in subject_records.items():
    if gene_id in unique_alignments:
        if gene_id not in subject_longest or len(record) > len(subject_longest[gene_id]):
            subject_longest[gene_id] = record

# Get the best matches for each longest gene
best_matches = {}
for query_id, query_record in query_longest.items():
    for subject_id, subject_record in subject_longest.items():
        if (query_id, subject_id) in unique_alignments:
            alignment_length, e_value = unique_alignments[(query_id, subject_id)][0]
            if query_record.seq == query_longest[query_id].seq and subject_record.seq == subject_longest[subject_id].seq:
                if query_id not in best_matches:
                    best_matches[query_id] = []
                if not best_matches[query_id] or e_value == best_matches[query_id][0][1]:
                    best_matches[query_id].append((subject_id, e_value))
                elif e_value < best_matches[query_id][0][1]:
                    best_matches[query_id] = [(subject_id, e_value)]

# Print the results
for query_id, matches in best_matches.items():
    if matches:
        print(f'Query gene: {query_id}')
        for match in matches:
            print(f'Best match: {match[0]}, E-value: {match[1]}')


"""
This code first parses both FASTA files and stores the longest gene for each gene ID 
that has an alignment in the BLAST file. 

It then gets the best matches for each longest gene by iterating over all pairs of 
longest genes and filtering the BLAST results by the longest gene sequences. If more 
than one gene is a best match, all best matches are included. 

Finally, the code prints the results, including the name of the query gene and the 
name(s) of its best match(es) with their corresponding E-value(s).

Note that this code assumes that you have already parsed and stored the BLAST results in the unique_alignments dictionary, as described in the previous answers. You can modify this code to adjust the filtering thresholds or to perform additional analyses, depending on your needs.
"""