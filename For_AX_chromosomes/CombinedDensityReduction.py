#!/usr/bin/python
# coding=utf-8

'''
         This script was developed by Isabela Almeida          
 in order to remove the probes that overlap for up to n
 positions to the previous one, given a .bed file input. It is
 also usefull for reducing probes density when provided a 
 bigger n value.       
 
 This was created while I was a MSc Bioinformatics student at  
 the Universidade de São Paulo (USP/Brazil) under supervision  
 of USP PhD Prof. Maria Vibranovski and under co-supervion of  
 UFRJ PhD Prof. Bernardo de Carvalho in the year of 2021       
 ~~~~~~~~~~~~~~~~~~~~~~(pandemic vibes)~~~~~~~~~~~~~~~~~~~~~~~ 

 <Envinroment: Sublime Text>                                   
 <OS: Linux (Ubuntu)>                                          
'''

import argparse
import sys
import pandas as pd
from pandas import DataFrame
import numpy as np
import csv

## Get command-line args
userInput = argparse.ArgumentParser(description=\
	"Takes two probes .bed files: one with unique probes and another with repetitive probes. "
	"It uses difference distance values to select unique (nU) and repetitive (nR) probes. "
	"Returns one file with all the kept probe hits and another with just the first appeareance of each hit. "
	"This was developed by Isabela Almeida (mb.isabela42@gmail.com) in 2021.")
requiredNamed = userInput.add_argument_group('required arguments')
requiredNamed.add_argument('-fU', '--Uniquefile', action='store', 
                          required=True, type=argparse.FileType('r'),
                          help='The BED file containg UNIQUE probes'
                          'in 3rd column')
requiredNamed.add_argument('-fR', '--Repetitivefile', action='store',        
                          required=True, type=argparse.FileType('r'),
                          help='The BED file containg REPTITIVE probes in 3rd column')
requiredNamed.add_argument('-o', '--output', action='store', 
                           required=True,
                           type=str, help='Specify the stem of the '
                                          'trimmed output filename')
requiredNamed.add_argument('-outHits', '--outputHits', action='store', 
                           required=True,
                           type=str, help='Specify the stem of the '
                                          'output filename which will have all probe hits')
userInput.add_argument('-nU', '--nUnique', action='store', 
                      default=20, type=int,
                      help='number of positions that must be '
                           'considered for unique probe selection; '
                           'it also removes overlaping probes')
userInput.add_argument('-nR', '--nRepetitive', action='store', 
                      default=20, type=int,
                      help='number of positions that must be '
                           'considered for repetitive probe '
                           'selection; '
                           'it also removes overlaping probes')

## Import user-specified command line values.
args = userInput.parse_args()
UFile = args.Uniquefile
RFile = args.Repetitivefile
outNameVal = args.output
outHits = args.outputHits
trimmU = args.nUnique
trimmR = args.nRepetitive
# args = parser.parse_args()

## Open and save data files
dataU = UFile.readlines()
dataR = RFile.readlines()
UFile.close()
RFile.close()

## Create output files
# main output with trimmed probes (first appearence of each probe/one copy per probe)
outputfile = outNameVal
out = open(outputfile, "w+" )

# output hits with all hits from the trimmed probes (all appearences of each probe/ all copies of each probe organized per position)
outputhits = outHits
outH = open(outputhits, "w+" )

## Create list and add Flags and count 1 for args.Uniquefile
mainUniq = []
for probe in range (0, len(dataU)):
    mainUniq_line = []
    mainUniq_line = dataU[probe].split("\t")
    mainUniq_line.append("U")
    mainUniq_line.append(1)
    mainUniq.append(mainUniq_line)

## Create df and add Flags and repetitions for args.Repetitivefile
## counting repetitions (probes copies)
mainRep = []
firstRep = []
firstRep=dataR[0].split("\t")
firstRep.append("R")
firstRep.append(1)
mainRep.append(firstRep)
for probe in range (1, len(dataR)):
	thisLine = dataR[probe].split("\t")    
	thisProbe = thisLine[3]
	hits = 1
	for eachProbe in range (0,len(mainRep)):
		otherProbe = mainRep[eachProbe][3]
		if thisProbe == otherProbe:
			hits = mainRep[eachProbe][6] + 1
			mainRep[eachProbe][6] = hits
	mainRep_line = []
	mainRep_line = dataR[probe].split("\t")
	mainRep_line.append("R")
	mainRep_line.append(hits)
	mainRep.append(mainRep_line)

## Transform mainUniq and mainRep into DataFrames
dfFinalU = DataFrame(mainUniq,columns=['Tag','Start','End', 'Probe', 'Temp', 'Flag', 'Copies'])
dfFinalR = DataFrame(mainRep,columns=['Tag','Start','End', 'Probe', 'Temp', 'Flag', 'Copies'])

## Get final dataframe
# Concatenate the two dataframes
dfFinal = pd.concat([dfFinalU, dfFinalR], sort=False, axis=0)
# Convert values to int
dfFinal.Start = dfFinal.Start.astype(int)
dfFinal.End = dfFinal.End.astype(int)
dfFinal.Temp = dfFinal.Temp.astype(float)
# sort values by column start
dfFinal = dfFinal.sort_values('Start')
# remove \n char from txt inicial file
dfFinal = dfFinal.replace('\n','', regex=True)
# reset index to new combined and sorted df
dfFinal = dfFinal.reset_index(drop=True)
# transform to list
# dfFinal = dfFinal.values.tolist()

## Get max value of the most frequent repetition range
# maxCopies = dfFinalR.Copies.max()
# maxFreqRange = 0
# for r in range(1,maxCopies,5): # Range starts at r
# 	rangeCount = 0
# 	for i in range(0,len(mainRep)):
# 		# if copies == r or (copies < r+5 and copies > r)
# 		if mainRep[i][6] == r or (mainRep[i][6] < (r+5) and mainRep[i][6] > r):
# 			rangeCount += 1
# 	if rangeCount >= maxFreqRange:
# 		maxFreqRange = rangeCount
# 		repeatRich = r+4 # min value to be repeatRich
# 		if r > maxCopies: repeatRich = maxCopies

## Select final probes (Write to outputfile)
## by selecting probes that do not overlap with the following ones for up to n positions

# create list in which selected probe hits are appended to
# should have the same probes as outH
dataH = []

# write the very first probe (erlier start position) to outputHits file (outH)
dfFinal.loc[[0]].to_csv(outH, sep='\t', index=False, header=False)
st = dfFinal.loc[0].values.tolist()
dataH.append(st)

# set the first probe end position as the last one
lastEnd=int(dfFinal.loc[0][2])

# register the firt info about probe
if str(dfFinal.loc[0][5]) == "U":
	lastFlagU = lastEnd
	savedU = 1  # no. of unique probes that were written to output file
	savedRhits = 0  # no. of repetitive probes that were written to output file
else: 
	lastFlagU = lastEnd # slight misconception, but overall prevents overlap
	savedRhits = 1  # no. of repetitive probes that were written to output file
	savedU = 0  # no. of unique probes that were written to output file

savedHits = 1 # overall no. of probes that were written to output file
for probe in range (1, len(dfFinal)):
	startPos = int(dfFinal.loc[probe][1])
	endPos = int(dfFinal.loc[probe][2])
	flag = str(dfFinal.loc[probe][5])
	copies = int(dfFinal.loc[probe][6])
	
	# Unique probes selection
	if flag == "U":
		for i in range (0,trimmU+1):
			if (lastFlagU+i) >= (startPos):
				break
			else: continue

		if (lastFlagU+i) < (startPos):
			lastFlagU = endPos
			lastEnd = endPos
			dfFinal.loc[[probe]].to_csv(outH, sep='\t', index=False, header=False)
			dataH.append(dfFinal.loc[probe].values.tolist())
			savedHits += 1
			savedU += 1
	
	# Repetitive probes selection
	elif flag == "R":
		for i in range (0,trimmR+1):
			if (lastEnd+i) >= (startPos): # and copies >= repeatRich:
				break
			else: continue

		if (lastEnd+i) < (startPos): # and copies >= repeatRich:
			lastEnd = endPos
			dfFinal.loc[[probe]].to_csv(outH, sep='\t', index=False, header=False)
			dataH.append(dfFinal.loc[probe].values.tolist())
			savedHits += 1
			savedRhits += 1
outH.close()

## Keep just first copy of each probe in dataH
## saving to args.output
keep = []
keep.append(dataH[0])

# Filter probes
trimmedOut = []
trimmedOut.append(dataH[0])
savedProbes = 1
if dataH[0][5] == 'R': savedR = 1
else: savedR = 0
for probe in range (1, len(dataH)):
	thisProbe = dataH[probe][3]
	first = True
	for eachProbe in range (0,len(trimmedOut)):
		otherProbe = trimmedOut[eachProbe][3]
		if thisProbe == otherProbe:
			first = False
			break
	if first == True:
		trimmedOut.append(dataH[probe])
		savedProbes += 1
		keep.append(dataH[probe])
		if dataH[probe][5] == 'R': savedR += 1

# save first copy of each probe to output main file (args.output)
wr = csv.writer(out,delimiter="\t")
wr.writerows(keep)

## Print info about the results to terminal.
print('CombinedDensityReduction identified {0} of {1} / {2:.4f}% and these final copies correspond to a total of {3} hits'.format(savedProbes, len(dfFinal), float (savedProbes) / float(len(dfFinal)) * 100, savedHits))
print('{0} single-copy probes were kept ({1}%). They presented a distance of at least {2} positions to the previously selected single-copy probe.'.format(savedU, float (savedU) / float(len(dfFinal)) * 100, trimmU))
print('{0} repetitive probes were kept ({1}%) with a total of {2} hits. They presented a distance of at least {3} positions to the previously selected probe, regardless of its nature.'.format(savedR, float (savedRhits) / float(len(dfFinal)) * 100, savedRhits, trimmR))
# print('Repetitive probes that were close to another probe were only kept when presenting at least {0} copies and, if the probe it was close to was also repetitive, they were only kept when also presenting more copies than the last one.'.format(repeatRich))
