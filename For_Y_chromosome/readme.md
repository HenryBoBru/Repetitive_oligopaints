# Repetitive Oligopaints for Y Chromosome

## Table of Contents  
- [Overview](#overview)  
- [Getting Started](#getting-started)  
- [Pipeline](#pipeline)  
- [Contact](#contact)  

---

## **Overview**  
This repository contains the scripts and pipeline developed for the manuscript:  
"Deciphering Chromosome Fusion in *D. miranda*'s Neo-Sex Chromosome through Single-Copy and Repetitive Oligo Probes" 

This project focuses on designing Single-copy and Repetitive Oligopaint probes for the Y chromosome by integrating the OligoY approach (https://github.com/isabela42/OligoY) to OligoMiner (https://github.com/beliveau-lab/OligoMiner).  
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
   You need three fasta and two fastq files to design oligopaints:
   - Male genome assembly (.fna)
   - Chromosome or region target to design oligos (.fna)
   - Male genome assembly without the target chromosome/region (.fna)
   - Female reads (*fastq.gz)
   - Male reads (*fastq.gz)

## **Pipeline**

1. **Identification of Y-linked scaffolds/contigs**
   
We used the Y-Genome Scan (YGS) approach (Carvalho & Clark, 2013) to identify Y-linked scaffolds and contigs. Detailed instructions are provided in the YGS section of the OligoY repository (https://github.com/isabela42/OligoY).
After identifying Y-linked scaffolds/contigs, one of them can be selected for oligo design.

2. **Oligos design**
   
Oligo design for a Y-linked regions follows a workflow similar to that described in *Repetitive Oligopaints for X/A Chromosome* manual (README.md).
Specifically, follow the 1-7 steps in **Pipeline** section of For_AX_chromosome directory

These steps include:
1. **Discover candidate oligos**  
2. **Mapping candidate oligos to genome**  
3. **Select single-copy oligos** 
4. **Select repetitive oligos**  
5. **Filtering using Kmer approach**  
6. **Filtering of secondary structure (StructureCheck)**
7. **Individual Density Reduction** or **CombinedDensityReduction**

## **Contact**  
Please contact Henry Bonilla if you have any enquires.
hnrb109@gmail.com
henry.bonilla@usp.br
