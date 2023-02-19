"""
To get the percentage of genes in each FASTA file that have an alignment in the BLAST file, you can use the following Python code:
"""

from Bio import SeqIO

# Parse the query FASTA file and store the gene IDs in a set
query_records = SeqIO.to_dict(SeqIO.parse('/scratch/mrmckain/Bioinformatics_Class/BATs/BAT_6_Combining_FASTA_and_BLAST/Gene_models_2.fasta', 'fasta'))
query_genes = set(query_records.keys())

# Parse the subject FASTA file and store the gene IDs in a set
subject_records = SeqIO.to_dict(SeqIO.parse('/scratch/mrmckain/Bioinformatics_Class/BATs/BAT_6_Combining_FASTA_and_BLAST/Gene_models_1.fasta', 'fasta'))
subject_genes = set(subject_records.keys())

# Parse the BLAST file and store the aligned gene IDs in a set
blast_genes = set()
with open('/scratch/mrmckain/Bioinformatics_Class/BATs/BAT_6_Combining_FASTA_and_BLAST/Gene_models_1v2.blastn') as blast_file:
    for line in blast_file:
        query_id, subject_id, percent_identity, alignment_length, mismatches, gap_opens, query_start, query_end, subject_start, subject_end, e_value, bit_score = line.split('\t')
        blast_genes.add(query_id)
        blast_genes.add(subject_id)

# Calculate the percentage of genes in each FASTA file that have an alignment in the BLAST file
query_percent = len(blast_genes & query_genes) / len(query_genes) * 100
subject_percent = len(blast_genes & subject_genes) / len(subject_genes) * 100

# Print the results
print(f'Query file alignment percentage: {query_percent:.2f}%')
print(f'Subject file alignment percentage: {subject_percent:.2f}%')

"""
This code first parses both FASTA files and stores the gene IDs in sets. It then parses the BLAST file and stores the aligned gene IDs in a set. Finally, it calculates the percentage of genes in each FASTA file that have an alignment in the BLAST file by finding the intersection of the aligned gene IDs set and the gene IDs set for each file, dividing by the total number of gene IDs in each set, and multiplying by 100. The code then prints the results, including the percentage alignment for each file rounded to two decimal places.

Note that this code assumes that the gene IDs in the BLAST file match the gene IDs in the FASTA files. You can modify this code to adjust the parsing or to perform additional analyses, depending on your needs.
"""