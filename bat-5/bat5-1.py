import csv
import sys

filename = sys.argv[1]
totalcount=0
nonalignedcount=0
headercount=0

with open (filename) as file:
	reader = csv.reader(file, delimiter='\t')

	for line in reader:
		totalcount += 1
		if line[0][0] == '@' :
			headercount +=1


		else:
			columns = line
			one = columns[0]
			two = columns[1]
			three = columns[2]
			four = columns[3]
			five = columns[4]
			six = columns[5]
			seven = columns[6]
			eight = columns[7]
			nine = columns[8]
			ten = columns[9]
			eleven = columns[10] 
			# print(three,four,five,six,seven,eight,nine)
			if ((three == '*' or three == '0') and
                (four == '*' or four == '0') and
				(five == '*' or five == '0') and
				(six == '*' or six == '0') and
				(seven == '*' or seven == '0') and
				(eight == '*' or eight == '0') and
				(nine == '*' or nine == '0')):
				nonalignedcount +=1
			

print("number of lines total ",totalcount)
print("number of lines that were headers ",headercount)
print("number of lines that were not aligned ",nonalignedcount)
print("number of lines that were aligned ",totalcount - headercount - nonalignedcount)
