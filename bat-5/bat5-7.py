"""
Here is the pseudocode:

1. Create a variable called insertions and set it to 0
2. Create a variable called deletions and set it to 0
3. Read all lines that start with a "@" and discard them because they are not needed
4. For the remaining lines that are left in the file
		1. read every line with a csv reader and do the following
			1. assign columns 3 - 9 from the csv reader's last read line to seperate variables 
			2. if all column 3-9 variables contain only (* or 0)
				1. discard the line because it is a non-alignment
			3. else assign a variable called cigar to the value of column 6
				1. if the varaible cigar contains a 'D'
					1. increment deletions counter varaible
				1. if the varaible cigar contains an 'I'
					1. increment insertions counter varaible

5. after all the lines have been read print out total insertions and deletions
"""


import csv
import sys

filename = sys.argv[1]
insertions=0
deletions=0

with open (filename) as file:
	reader = csv.reader(file, delimiter='\t')

	for line in reader:
		if line[0][0] == '@' :
			continue

		else :
			three, four, five, six, seven, eight, nine = [line[i] for i in (2, 3, 4, 5, 6, 7, 8)]

			# print(three,four,five,six,seven,eight,nine)
			if ((three == '*' or three == '0') and
                (four == '*' or four == '0') and
				(five == '*' or five == '0') and
				(six == '*' or six == '0') and
				(seven == '*' or seven == '0') and
				(eight == '*' or eight == '0') and
				(nine == '*' or nine == '0')):
				continue
			
			else : 
				cigar = six
				if (cigar.find('I') >= 0) :
					insertions += 1
				if (cigar.find('D') >= 0) :
					deletions += 1



print("number of insertions ",insertions)
print("number of deletions ",deletions)
