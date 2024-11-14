import re
print( sum( [ int(x) for x in re.findall(r'\d+',open('regex_sum_2091004.txt', 'r').read()) ] ) )
