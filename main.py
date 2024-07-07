from chepy import Chepy

filename = "~/Documents/a1b94e324beb19da2cabb254652df7c75dfcdad3c099012bb10e06448198d204.vbs"

c = Chepy(filename)

c.load_file()
c.to_string()

defined_regx_1 = r'Call Polyptote\("([^"]+)"\)'

c.regex_search(defined_regx_1)
c.join()
c.remove_whitespace(spaces=False, tabs=False)

defined_regx_2 = r'Charcuteries \'([^\']+)\''

c.regex_search(defined_regx_2)
c.join()

replace_regx = r'.......(.)'

c.find_replace(replace_regx,r'\1')

print(c)
