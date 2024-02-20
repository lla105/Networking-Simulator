from platform import java_ver
import sys
import random
#from tabulate import tabulate
import ipaddress

def DecimalToBinary(num): # don't use this. just use bin()
        if int(num) >= 1:
            DecimalToBinary(int(num) //2 )
        print(int(num)%2, end='')

def bubblesort(list):
   for iter_num in range(len(list)-1,0,-1):
      for idx in range(iter_num):
        start_ip = list[idx][2]
        end_ip = list[idx+1][2]
        if list[idx][2]<list[idx+1][2]:
            temp = list[idx]
            list[idx] = list[idx+1]
            list[idx+1] = temp

def deci_to_binary(address): #address is string. returns address as BINARY. (string)
    full_address = ''
    temp_address = ''
    for i in range(len(address)):
        if address[i] == ".":
            temp_address = bin(int(temp_address))
            full_address = full_address+ temp_address
            full_address=full_address+"."
            temp_address = ''
        else: # if digit is not a period
            temp_address = temp_address + address[i]
    full_address = full_address + bin(int(temp_address))
    return full_address

def eight_digit_binary(partaddress): #turns binary # like 1010 to 00001010
    if len(partaddress) == 35:
        return partaddress
    else:
        dot_pos = 0
        eight_count = 0
        rangenum = len(partaddress)
        for i in range(rangenum):
            if partaddress[i] == ".":
                dot_pos = i
                if eight_count == 8: #portion has full 8 digits. good!
                    continue
                else: #portion has less than 8 digits.
                    zeros = 0
                    for j in range(8-dot_pos):
                        zeros += '0'
                    partaddress = partaddress[0:dot_pos+1] + zeros + partaddress[dot_pos+1:]
    print(partaddress)
    return partaddress


def bitwise_AND(address1, address2): #BITWISE AND FUNCTION
    product_address = ''
    dot1list = []
    dot2list = []

    for i in range(len(address1)):
        if address1[i] == '.' :
            dot1list.append(i)
    for i in range(len(address2)):
        if address2[i] == '.' :
            dot2list.append(i)
    product_address += str(int(address1[:dot1list[0]]) & int(address2[:dot2list[0]])) + "."
    product_address += str(int(address1[dot1list[0]+1:dot1list[1]]) & int(address2[dot2list[0]+1:dot2list[1]])) + '.'
    product_address += str(int(address1[dot1list[1]+1:dot1list[2]]) & int(address2[dot2list[1]+1:dot2list[2]])) +'.'
    product_address += str(int(address1[dot1list[2]+1:]) & int(address2[dot2list[2]+1: ] ))
    return product_address

def forward_this(input_address, whole_table):
    match_index = [] #row number
    metric_value = []
    for i in range(len(whole_table)): #build list of bitwise AND matches by index.
        if bitwise_AND(input_address,whole_table[i][2]) == whole_table[i][0]:
            match_index.append(i)
            metric_value.append(whole_table[i][3])
    #print(f'match_index list: {match_index}')
    #print( whole_table[match_index[0]] )
    #print('\n\n')
    if len(match_index) > 1: # if more than 1 matches.
        smallest_metric_index = match_index[0]
        for i in range(len(metric_value)-1):
            if metric_value[i] < metric_value[i+1]: # i is smaller than next. good!
                continue
            elif metric_value[i] == metric_value[i+1]:
                continue
            else: # if next metric is smaller than current one.
                smallest_metric_index = match_index[i+1]
        #print(f'SMALLEST ROW IS: {whole_table[int(smallest_metric_index)]}')
        ii = int(smallest_metric_index)
        return whole_table[ii]
    else: # only 1 match
        return whole_table[match_index[0]]
    
def printpretty(whole_table):
    length = 13
    print(f'Destination    Gateway        mask           metric  interface')
    print(f'-------------  -------------  -------------  ------  ---------')
    for i in range(len(whole_table)):
        space = ' '
        space2 = ' '
        space3 = ' '
        space4 = ' '
        for j in range(14-len(whole_table[i][0])):
            space += ' '
        for j in range(14-len(whole_table[i][1])):
            space2 += ' '
        for j in range(19-len(whole_table[i][2])):
            space3 += ' '
        for j in range(2-len(whole_table[i][3])):
            space4 += ' '
        print(
            whole_table[i][0] + space +
            whole_table[i][1] + space2 + 
            whole_table[i][2] + space3 + 
            whole_table[i][3] + space4 + 
            whole_table[i][4] )
        

#====================== MAIN FUNCTION ==================================================


file_name = input("Input your file name WITHOUT inputting the file type\n (eg: If file name is abcd.txt, just type in abcd): ")
with open(file_name+".txt") as f:

#with open('tableInput.txt') as f:
    lines = f.readlines()

whole_table =[]
mask_list = []

count = 0 #the # of rows in table. just for ref
for line in lines: # parse through data, & BUILD 2D whole_table
    if line in ['\n', '\r\n']:
        break
    else: 
        space_split = line.split()
        whole_table.append(space_split)
        mask_list.append(space_split[2])
        count+=1
#whole_table is now a 2D array
#whole_table[0] would be the first row.
bubblesort(whole_table) #sort the table according to mask (longest to smallest)
#print(tabulate(whole_table,headers =['Destination','Gateway','mask','metric','interface'])) #print out sorted table.
printpretty(whole_table) #Print out table nicely
print("-------------------------------------")
addresss1 = deci_to_binary("255.255.254.0")
addresss2 = deci_to_binary("202.123.40.0")

Continue = True
while Continue == True:
    print(' ')
    user_input = str(input("Input packet destination IP address: "))
    #fake_input = '201.123.64.0'
    #fake_input2 = '202.123.40.0'
    fake_input = user_input
    #print(whole_table[0][2])
    forward_this_row = forward_this(fake_input,  whole_table)
    print(forward_this_row)
    print(f'The destination IP address is {forward_this_row[0]}')
    print(f'The next hop IP address is {forward_this_row[1]}')
    print(f'The interface the packet will leave through is {forward_this_row[4]}')
    next_round = input('Forward another packet?')
    if next_round.lower() == 'yes' :
        continue
    else: 
        Continue == False
        break
    


##################### GRADING RUBRIC ##########################
# line 16 - "Put input table into order, from longest mask to shortest mask"
# line 101 - "Print routing table (in sorted order) to screen"
# line 26 - "Convert address to binary"
# line 154 - "Read IP dest address of packet to be forwarded."
# line 26 - "Convert IP to binary"
# line 78 - "bitwise AND"
# line 87 - "The program must inlcude the use of metric"
# line 161~163 - "Output the dest IP address, next hop IP address, interface"
# line 153~169 - "ask if user wants to continue"