# Created by Joseph Ammer 02/07/2018 for meu bem
# js.ammer@gmail.com

# This file and the .csv must be in the same folder
# The file converted is named output.csv
# Input and output names can be changed on lines 9 and 108
import csv
# File name to open
f = open('dataset.csv')
# Holds file data
data = []
# Reads file input and puts into list array
for l in  csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
    data.append(l)
# Holds data
outputData = []
tempData = []
secondTempData = []
positionSubject = "" # "Subject"
positionItem = "" # "Item"
positionSentence1 = "" # "Sentence1"
positionSentence2 = "" # "Sentence2"
postionCount = len(data[0]) # "Count"
# Gets positions of each required column
for i, cell in enumerate(data[0]):
    if cell == u"Subject" or cell == u"ï»¿Subject":
        positionSubject = i
    if cell == u"Item" or cell == u"ï»¿Item":
        positionItem = i
    if cell == u"Sentence1" or cell == u"ï»¿Sentence1":
        positionSentence1 = i
    if cell == u"Sentence2" or cell == u"ï»¿Sentence2": 
        positionSentence2 = i
# Gets column headers on outputData
outputData.append(data.pop(0))
# Loops thru data, processes, and adds to output
while len(data) > 0:
	# Clears temp data
	tempData[:] = []
	# Resets count
	wordsCount = 0
	# Gets subject and item number from top row
	subject = data[0][positionSubject]
	item = data[0][positionItem]
	# Gets next section of sentences matching subject & item number
	for words in data:
		if words[positionSubject] == subject and words[positionItem] == item:		
			tempData.append(words)
			wordsCount += 1
		else:
			break	
	tempCounter = 0
	# Removes (top rows) found words in data
	while tempCounter < wordsCount:
		data.pop(0)
		tempCounter += 1
	# Gets number of words for each sentence
	firstCount = tempData[0][positionSentence1].count(" ")
	secondCount = tempData[0][positionSentence2].count(" ")
	# First sentence shorter OR Both sentences same length
	# Outputs first sentence, then second
	if firstCount <= secondCount and firstCount > 0:	
		tempCounter = 0
		while tempCounter <= firstCount:
			# Skips rows in order to get first sentence complete
			outputData.append(tempData.pop(tempCounter))
			tempCounter += 1
		# Only Second sentence remains, and outputs	
		outputData.extend(tempData)
	# Second sentence shorter
	# Gets second sentence, outputs first, then outputs second
	if firstCount > secondCount:
		tempCounter = 1
		secondTempData[:] = []
		while tempCounter <= secondCount + 1:
			# Stores second sentence in secondTempData list
			secondTempData.append(tempData.pop(tempCounter))
			tempCounter += 1
		# Only first sentence remains (in tempData), and outputs
		outputData.extend(tempData)
		# Outputs second sentence
		outputData.extend(secondTempData)
#Loops thru and appends line number to end
try:
	# Added header title for line number column
	outputData[0].append("Count")
	tempCounter = 1
	# Adds line number at end of line for each sentence group
	while True:	
		# Gets current/previous subject/item numbers
		subject = outputData[tempCounter][positionSubject]
		previousSubject = outputData[tempCounter - 1][positionSubject]
		item = outputData[tempCounter][positionItem]
		previousItem = outputData[tempCounter - 1][positionItem]				
		if subject == previousSubject and item == previousItem:
			# If row is part of previous row, increment line counter
			outputData[tempCounter].append(outputData[tempCounter - 1][postionCount] + 1)
		else:
			# Else put 1 for line counter, start of new sentence group
			outputData[tempCounter].append(1)
		tempCounter += 1
except:
	# When finished adding line numbers, throws exception, 
	# falls into here, and prints to console
	print(tempCounter)
# Writes data to output.csv, can rename
with open("output.csv","w",newline="") as f:
    cw = csv.writer(f)
    cw.writerows(outputData)
