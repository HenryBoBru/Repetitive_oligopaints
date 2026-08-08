## This readme contains the steps for adding the priming regions to the oligopaints probes.
## These priming regions allow the selection, amplification, and labeling of the oligopaints during th wetlab.

The final oligopaint probes contained three components:  
i) a central targeting sequence for in situ hybridization to the target scaffold/chromosome, it means the oligos designed,  
ii) a flanking priming region for reverse transcription (RT) and,  
iii) two index flanking priming regions (forward and reverse) to allow selection/amplification of a subset of oligos required for a specific experiment  

Final Probe template:  
                                      IndexPrimingForward--RTpriming--oligo--IndexPrimingReverse


# Step1 - Double-check IndexPrimings do not align among them. Use word_size 11
# Remove IndexPrimers that show some similarity.
blastn -query IndexPrimers.fasta -subject IndexPrimers.fasta -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore' -word_size 11 > IndexPrimers.blastOut.txt


# Step2 - Aling IndexPrimers with T7 3' terminal region (the last 5 nucleotides)
# T7 sequence: 		5’ TAATACGACTCACTATAGGG 3’
blastn -query IndexPrimers.fasta -subject T7promoter3end.fasta -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore' -word_size 5 > IndexPrimersVsT7.blastOut.txt

# Step3 - Aling RTprimers among them. Use word_size 20
# Remove RTprimers that show some similarity.
blastn -query rtPrimers.fasta -subject rtPrimers.fasta -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore' -word_size 20 > rtPrimers.blastOut.txt

#Step4 - Aling RTprimers with T7 3' terminal region (the last 5 nucleotides)
blastn -query rtPrimers.fasta -subject T7promoter3end.fasta -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore' -word_size 5 > rtPrimersVsT7.blastOut.txt

#Step5 - Alinhar primers da sonda de PCR contra TARGET word_size 12
