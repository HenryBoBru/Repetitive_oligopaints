# Repetitive Oligopaints for X/A Chromosome

## Table of Contents  
- [Overview](#overview)  
- [Getting Started](#getting-started)  
- [Pipeline](#pipeline)  
- [Contact](#contact)  

---

## **Overview**  
This repository contains the scripts and pipeline developed for the manuscript:  
"Deciphering Chromosome Fusion in *D. miranda*'s Neo-Sex Chromosome through Single-Copy and Repetitive Oligo Probes" 

This project focuses on designing Repetitive Oligopaint probes for autosomes or X chromosomes by enhancing the conventional OligoMiner (https://github.com/beliveau-lab/OligoMiner) and OligoY (https://github.com/isabela42/OligoY) pipelines.  
We successfully validated the specificity of our oligo libraries through fluorescence in situ hybridization (FISH). 

---

## **Getting Started**  

1. **Install miniconda**
   https://www.anaconda.com/docs/getting-started/miniconda/install#macos-linux-installation
2. **Clone the OligoMiner repository**  
   ```bash
   git clone https://github.com/beliveau-lab/OligoMiner.git
   cd OligoMiner
   conda create --name OligoMiner numpy scipy biopython==1.76 scikit-learn python=2.7 bowtie2=2.3.5.1 jellyfish=2.2.10
   conda activate OligoMiner 
   ```  
   **Note:** OligoMiner requires specific software versions to work correctly.
   
3. **Install Nupack**  
   The filter of the Secondary structure uses Nupack, this program is not compatible with biopython=1.76 in the OligoMiner environment, then create another environment for running this program.  
   You can get it from Isabela’s github (former student of Prof. María Vibranovski)
      ```bash
   git clone https://github.com/isabela42/OligoY.git 
   ```
   **Add the directory to PATH in ~/.bashrc:**  
   PATH=$PATH:/path/to/OligoY/scripts/Beliveau2018/nupack3.0.6/bin  
   NUPACKHOME=/path/to/OligoY/scripts/Beliveau2018/nupack3.0.6/  

   **Create a conda environment for Nupack (StructureCheck program)**
   ```bash
   conda create --name Nupack numpy scipy biopython==1.77 scikit-learn python=3.6 # Nupack works with biopython1.77
   conda activate Nupack
   ```
4. **Dowload your genomic data:**  
   You need three fasta files to design oligopaints:
   - Male genome assembly (.fasta)
   - Chromosome or region target to design oligos (.fasta)
   - Male genome assembly without the target chromosome/region (.fasta) 

## **Pipeline**
For demostration purposes, we will show the scripts to desing oligos for chr4 of D. melanogaster.

1. **Discover candidate oligos**  
   ```bash
   conda activate OligoMiner
   python /change/path/to/OligoMiner/blockParse.py -O -l 40 -L 46 -t 47 -T 52 -f /change/path/to/chr4.fasta -o /change/path/to/Dmel_oligos/Dmel_chr4_string_lap # See OligoMiner article for details (paramethers, etc)
   ```
2. **Mapping candidate oligos to genome**  
Align to complete male genome (for single-copy oligos) and to male genome without the target chromosome (to get single copy and repetitive oligos)

   - For single-copy oligos
   ```bash
   #Index the genome
   bowtie2-build /change/path/to/Dmel/GCF_000001215.4_Release_6_plus_ISO1_MT_genomic.fna /change/path/to/Dmel/Dmel_complete # index the genome to map oligos
   #Mapping     
   bowtie2 -x /change/path/to/Dmel/Dmel_complete  -U /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.fastq --very-sensitive-local -k 2 --no-hd -t -p 4 -S /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.sam
   ```
   - For single copy + repetitive oligos
   ```bash
   You can use: sed -e '/NC_004353.4/,+1d' /change/path/to/Dmel/GCF_000001215.4_Release_6_plus_ISO1_MT_genomic.fna > /change/path/to/Dmel/GCF_000001215.4_Release_6_plus_ISO1_MT_genomic_NoChr4.fna # to remove the target chromosome of the male genome assembly
   ```
   ```bash
   #Index the genome without target chromosome
   bowtie2-build /change/path/to/Dmel/GCF_000001215.4_Release_6_plus_ISO1_MT_genomic_NoChr4.fna /change/path/to/Dmel/Dmel_NoChr4 # index the genome to map oligos
   #Mapping        
   bowtie2 -x /change/path/to/Dmel/Dmel_NoChr4 -U /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.fastq --very-sensitive-local -k 2 --no-hd -t -p 4 -S /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.All.sam
   ```

3. **Select single-copy oligos** 
   ```bash
   conda activate OligoMiner
   python /change/path/to/OligoMiner/outputClean.py -u -f /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.sam -o /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.Sc
   ```
   
4. **Select repetitive oligos**  
<sup> Note: The complete set of oligos are firstly obtained. The complete set of oligos are made up of single-copy and repetitive oligos. Therefore, we have to subtract single-copy oligos (step 3 output) from the complete set of oligos. </sup>
   
   - Obtain all oligos
   ```bash
   python /change/path/to/OligoMiner/outputClean.py -0 -f /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.All.sam -o /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.All
   ```
   - Obtain repetitive oligos
   ```bash
   awk 'FILENAME != ARGV[2] { m[$1,$2, $3] = 1; next}; !(($1,$2, $3) in m)' \
   /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.Sc.bed \
   /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.All.bed \
   > /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.R.bed 
   ```
5. **Filtering using Kmer approach**  
  
   - For Single-copy oligos  
   ```bash
   conda activate OligoMiner
   #Create kmer dictionary
   jellyfish count /change/path/to/Dmel/GCF_000001215.4_Release_6_plus_ISO1_MT_genomic.fna -C -m 18 -s 10G -t 10 -o /change/path/to/Dmel/GCF_000001215.4_18m10G.jelly # Create a 18-Kmer dictionary for D.mel genome. The size of the dictionary depends on the genome size. 
   
   #Kmer filter
   python2.7 /change/path/to/OligoMiner/kmerFilter.py -f /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.Sc.bed -m 18 -j  /change/path/to/Dmel/GCF_000001215.4_18m10G.jelly -k 5 -o /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.Sc.m18 # Run 18-Kmer filter using a threshold 5 (-k). See OligoMiner article for details.
   ```  
   - For Repetitive oligos  
<sup> Note: Use the male genome without the target chromosome to generate the kmer dictionary. </sup>  
   ```bash  
   #Create kmer dictionary
   jellyfish count /change/path/to/Dmel/GCF_000001215.4_Release_6_plus_ISO1_MT_genomic_NoChr4.fna -C -m 18 -s 10G -t 10 -o /change/path/to/Dmel/GCF_000001215.4_18m10G_NoChr4.jelly # Use the same file used in step2
   
   #Kmer filter
   python2.7 /change/path/to/OligoMiner/kmerFilter.py -f /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.R.bed -m 18 -j  /change/path/to/Dmel/GCF_000001215.4_18m10G_NoChr4.jelly -k 5 -o /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.R.m18 # Run 18-Kmer filter using a threshold 5 (-k). See OligoMiner article for details.
   ```

6. **Filtering of secondary structure (StructureCheck)**

   ```bash
   #Activate the Nupack environment
   conda activate Nupack
   ```
   - For Single-copy oligos
   ```bash
    python3.6 /change/path/to/OligoY/scripts/Beliveau2018/structureCheckpy3v2.py -f /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.Sc.m18.bed -T 37 -t 0.1 -o /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.Sc.m18.SC  # See OligoMiner article for details (paramethers, etc)
   ```
   - For Repetitive oligos
   ```bash
   python3.6 /change/path/to/OligoY/scripts/Beliveau2018/structureCheckpy3v2.py -f /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.R.m18.bed -T 37 -t 0.1 -o /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.R.m18.SC  # See OligoMiner article for details (paramethers, etc)
   ```

7. **Step 7, Option A: Individual Density Reduction**  
<sup> Note: This step remove overlapping oligos by selecting a spacing between consecutive oligos.  
Use our densityReduction.py script 

   - Single-copy oligos
   ```bash
   python /change/path/to/densityReduction.py -n 0 -f /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.Sc.m18.SC.bed -o /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.Sc.m18.SC.n0.bed # -n is the spacing between consecutive oligos
   ```
   - Repetitive oligos
   ```bash
   python /change/path/to/densityReduction.py -n 0 -f /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.R.m18.SC.bed -o /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.R.m18.SC.n0.bed # -n is the spacing between consecutive oligos
   ```

7. **Step 7, Option B: CombinedDensityReduction**  
<sup> The CombinedDensityReduction script uses both lists of oligos to select single-copy oligos spaced by a desired distance (nt) and incorporates repetitive-oligos in positions where single-copy oligos are absent, while also considering a specific spacing with the preceding oligo. 
Test different nucleotide distances between oligos to reach a density of 1 oligo/Kb. If this value of density could not be reached, run with “-nU 0 -nR 0” to retrieve all possible oligos without any overlap.  
CombinedDensityReduction script provides two files: a file showing all the hits, and a non-redundant list of oligos (.BED). The Hit file is used for statistical analysis of oligos along the target scaffold using R software, whereas the non-redundant list of oligos is used for probe construction. 

   ```bash
      python /change/path/to/CombinedDensityReduction.py -fU /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.Sc.m18.SC.bed \  
   -fR /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.R.m18.SC.bed \  
   -nU 0 -nR 0 \  
   -o /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.m18.SC_nU0_nR0.bed \  
   -outHits /change/path/to/Dmel_oligos/Dmel_chr4_string_lap.VS.m18.SC_nU0_nR0.Hits
   ```
                                                         ========================
                                                                   #END!
                                                         ========================

Go to R to plot the density of Oligos along the chromosome target.

## **Contact**  
Please contact Henry Bonilla if you have any enquires.
hnrb109@gmail.com
henry.bonilla@usp.br
