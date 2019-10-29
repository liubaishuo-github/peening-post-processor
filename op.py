import re


#======global varible between moduals======
def _init():#初始化
    global _global_dict
    _global_dict = {}

def set_value(key,value):
    _global_dict[key] = value

def get_value(key):
    return _global_dict[key]
#======global varible between moduals======



def FEDRAT(apt):
    set_value('feedrate',round(float(re.findall('\d+\.\d+', apt)[0]),1))
    #print(get_value('feedrate'))
    return 0, ''

def RAPID(apt):
    set_value('feedrate', 6000.0)
    return 0, ''

def PPRINT(apt):
    #print(apt[7:])
    return 1, apt[7:].strip()

def STOP(apt):
    return 1, 'M0'

def DWELL(apt):
    num = re.search('\d+\.?\d*|\.\d+', apt)
    if num:
        return 1, 'G4X'+ num.group()

def AIR(apt):
    if re.search('ON',apt):
        a = ['M71 (AIR ON)', 'G4X5']
    elif re.search('OFF',apt):
        a = ['M81 (AIR OFF)']
    return 2, a

def STEEL(apt):
    if re.search('ON',apt):
        a = ['M52 (STEEL ON)', 'G4X5']
    elif re.search('OFF',apt):
        a = ['M62 (STEEL OFF)', 'G4X5']
    return 2, a

def GLASS(apt):
    if re.search('ON',apt):
        a = ['M51 (GLASS ON)', 'G4X5']
    elif re.search('OFF',apt):
        a = ['M61 (GLASS OFF)', 'G4X5']
    return 2, a

def RECIPE(apt):
    pass

def SPINDLE(apt):
    pass

def SUBPROGRAM(apt):
    pass
