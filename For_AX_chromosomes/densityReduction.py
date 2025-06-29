#!/usr/bin/python
# coding=utf-8

'''
         This script was developed by Isabela Almeida and modified
         by Henry Bonilla. This script filters probes from a .bed file to 
         ensure a minimum spacing (-n) between adjacent oligos. It removes 
probes that overlap or start too close (within -n bases) to the previous 
probe, effectively reducing probe density when a larger -n is provided.
 
 This program was created while we were MSc Bioinformatics student at  
 the Universidade de São Paulo (USP/Brazil) under supervision  
 of USP PhD Prof. Maria Vibranovski (2021).       
 ~~~~~~~~~~~~~~~~~~~~~~(pandemic vibes)~~~~~~~~~~~~~~~~~~~~~~~ 

 <Envinroment: Sublime Text>                                   
 <OS: Linux (Ubuntu)>                                          
'''

import argparse
import sys

def main():
    # Get command-line args
    parser = argparse.ArgumentParser(description="Takes a probes .bed file containing "
                                    "ending position in the third column and "
                                    "removes the probes that overlap for/start up to "
                                    "n positions to the previous one.")
    parser.add_argument("-f", "--input", help="a probes.bed file",
                        default=sys.stdin,
                        type=argparse.FileType('r'))
    parser.add_argument("-o", "--output", help="output file name",
                        default=None)
    parser.add_argument("-n", "--noOverlap", help="spacing between oligos "
                        "When reducing density, n value must satisfy"
                        "the final desired oligos/kb density.",
                        type=int, default=0)

    args = parser.parse_args()
    
    # Read input data
    data = args.input.readlines()
        
    # Determine output filename
    if args.output:
        output_file = args.output
        if not output_file.endswith('.bed'):
            output_file += '.bed'
    else:
        if args.input != sys.stdin:
            base_name = os.path.splitext(args.input.name)[0]
            output_file = f"{base_name}_spaced.bed"
        else:
            output_file = "spaced_probes.bed"
    
    # Process the data
    with open(output_file, "w") as output:
        if not data:
            return
        
        output.write(data[0])
        first_probe = data[0].split("\t")
        previous = int(first_probe[2])
        nO_probes = 1

        for probe in range(1, len(data)):
            line = data[probe].split("\t")
            starts = int(line[1])
            ends = int(line[2])
            
            for i in range(0, args.noOverlap + 1):
                if (previous + i) >= (starts):
                    break

            if (previous + i) < (starts):
                previous = ends
                output.write(data[probe])
                nO_probes += 1

    # Print info about the results to terminal.
    print('densityReduction identified {0} of {1} / {2:.4f}% probes that do not overlap for up to {3} positions'.format(
        nO_probes, len(data), float(nO_probes) / float(len(data)) * 100, args.noOverlap))

if __name__ == "__main__":
    main()
