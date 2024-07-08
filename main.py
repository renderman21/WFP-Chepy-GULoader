from chepy import Chepy
import re
import pathlib
import os 

working_maldir = f"{pathlib.Path(__file__).parent.resolve()}/malware"

#List malware present in malware folder
files = [f for f in os.listdir(working_maldir)]


for f in range(len(files)):
    print(f"[{f}]: {files[f]}")

num = None
while True:
    num = int(input("Choose a number: "))

    if num >= 0 and num < len(files):
        break



filename = f"{working_maldir}/{files[num]}"

found_row = ""

# Read file section
with open(filename, 'r') as f:
    #Search cls to get the starting point
    lines = f.readlines()

    for row in lines:
        search_word = '"cls'

        if row.find(search_word) != -1:
            found_row = row
            
#Find what's behind cls to determine the regex and to put for the first stage 

reg = re.search(r'(.*)(?="c)', found_row).group()

#Check if there is paranthesis
if reg.find('(') != - 1:
    reg = reg.replace('(','')
    first_cap_group = r'\("([^"]+)"\)'
else:
    
    first_cap_group = r'\"([^"]+)\"'

#Replace + with \+
if reg.find('+'):
    reg = reg.replace('+', '\+')

#Combine reg and the first_cap_group 

defined_regx_1 = rf'{reg}{first_cap_group}'
c = Chepy(filename)

c.load_file()
c.to_string()

c.regex_search(defined_regx_1)
c.join()
c.remove_whitespace(spaces=False, tabs=False)

#Find the function that encrypts the values
#Create temporary file
with open('temp.txt', 'w') as w:
    w.write(c._convert_to_str())

#Read
with open('temp.txt', 'r') as r:
    content = r.read()

match_reg = re.search(r'Function ([^\(]*)', content).group(1)

for_loop = re.search(r'For(\([^)]*\))', content).group(1)

#Get number
offset_num = int(re.search(r'\+=(\d)', for_loop).group(1))

defined_regx_2 = rf'{match_reg} \'([^\']*)\''
c.regex_search(defined_regx_2)
c.join()

#Construct replace_regx 

replace_regx = r''

for i in range(offset_num):

    if i < offset_num-1:
        replace_regx += r'.'
    else:
        replace_regx += r'(.)'


c.find_replace(replace_regx,r'\1')

with open('output.txt', 'w') as o:
    o.write(c._convert_to_str())

print("A file is created. Please check 'output.txt'")
