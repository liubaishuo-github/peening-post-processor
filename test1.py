import re
def DWELL(apt):
    num = re.search('\d+\.?\d*|\.\d+', apt)
    if num:
        print(num.group())


ap = 'DWELL/5.500'
a = 'DWELL/0.89'
b = 'DWELL/1231'
c = 'DWELL/8'
f = 'DWELL/9.'
d = 'DWELL/.390'

DWELL(ap)
DWELL(a)
DWELL(b)
DWELL(c)
DWELL(f)
DWELL(d)
