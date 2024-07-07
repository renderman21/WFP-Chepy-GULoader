from chepy import Chepy
import re

'''
TODO: Make this dynamic by
- Asking for filename
- What is the first regex
- What is the second regex
- How many characters to capture?
'''

filename = "/home/kali/Documents/a1b94e324beb19da2cabb254652df7c75dfcdad3c099012bb10e06448198d204.vbs"


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
print(defined_regx_1)
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
