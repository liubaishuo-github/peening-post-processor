import re, math


#======global varible between moduals======
def _init():#初始化
    global _global_dict
    _global_dict = {}
    _global_dict['standoff'] = 6.0

def set_value(key,value):
    _global_dict[key] = value

def get_value(key):
    return _global_dict[key]
#======global varible between moduals======



def FEDRAT(apt):
    set_value('feedrate',round(float(re.findall('\d+\.\d+', apt)[0]),1))
    #print(get_value('feedrate'))
    return 0, ''

def STANDOFF(apt):
    set_value('standoff', round(float(re.findall('\d+\.\d+|\d+', apt)[0]),2))
    return 0, ''

def RAPID(apt):
    set_value('feedrate', 6000.0)
    return 0, ''

def FEEDOVER(apt):
    if re.search('ON',apt):
        set_value('feed_over','ON')
    elif re.search('OFF',apt):
        set_value('feed_over','OFF')
    return 0, ''


def PPRINT(apt):
    #print(apt[7:])
    return 1, apt[7:].strip()

def STOP(apt):
    message = apt.strip()[5:]
    return 2, ['M00' + message, ' ', ' ']

def DWELL(apt):
    num = re.search('\d+\.?\d*|\.\d+', apt)
    if num:
        if get_value('feed_over') =='OFF':
            return 1, 'G04X' + num.group()
        if get_value('feed_over') =='ON':
            return 1, 'G04X[' + num.group() + '*#100]'

def AIR(apt):
    if re.search('ON',apt):
        a = ['M71 (AIR ON)', 'G04X5']
    elif re.search('OFF',apt):
        a = ['G04X5', 'M81 (AIR OFF)']
    return 2, a

def STEEL(apt):
    if re.search('ON',apt):
        a = ['M52 (STEEL ON)', 'G04X5']
    elif re.search('OFF',apt):
        a = ['M62 (STEEL OFF)']
    return 2, a

def GLASS(apt):
    if re.search('ON',apt):
        a = ['M51 (GLASS ON)', 'G04X5']
    elif re.search('OFF',apt):
        a = ['M61 (GLASS OFF)']
    return 2, a


def RECIPE(apt):
    num = re.search('\d+', apt).group()
    a = ['#999={}(SET RECIPE NUMBER)'.format(num), 'G04X1', \
        'M43(CHANGE RECIPE NUMBER)', 'G04X6']
    return 2, a

def SPINDLE(apt):
    if re.search('STOP',apt):
        a = ['M05', 'G04X5(THIS COMMENT REQD AFTER M05)']
        return 2, a

    rpm = re.search('\d+', apt).group()
    if re.search('CLW', apt) and not(re.search('CCLW', apt)):
        dir = 'M03'
    elif re.search('CCLW', apt):
        dir = 'M04'

    a = '{}S[{}*10]'.format(dir, rpm)
    return 1, a

def SUBPROG(apt):
    sub = 'M98P' + re.search('\d+', apt).group()
    return 2, [' ', sub]

def GOHOME(apt):
    a = ['X0Z0A0B0F6000.0', 'Y0']
    return 2, a

def INITIAL(apt):
    return 2, ['M48', '#998=-1','M29(DISABLE SPEED OVERIDE)']

def SATUTEST(apt):
    return 1, '#100=1(SATURATION TESTS)'

def SAVERE(apt):
    return 2, ['M45(SAVE RECORD)', 'G04X2']

def SURFACE(apt):
    num = re.search('\d+', apt).group()
    if len(num) == 1:
        enum = '0' + num

    str_a = 'IF[#10{}EQ0]GOTOSURFACE{}'.format(enum, str(int(num)+1))
    str_b = '#998={}'.format(num)
    return 2, [' ', str_a, str_b]

#the apt point cannot pass through the rotary table center point, or will lead wrong feedrate
def cal_feed(apt, last_apt, feed, zb, last_zb):

    standoff = get_value('standoff')
    #print(apt,'=====standoff:', standoff)

    x = apt[0] - standoff*apt[3]
    y = apt[1] - standoff*apt[4]
    z = apt[2] - standoff*apt[5]
    #print(apt,':')
    #print(x,y,z)
    last_x = last_apt[0] - standoff*last_apt[3]
    last_y = last_apt[1] - standoff*last_apt[4]
    last_z = last_apt[2] - standoff*last_apt[5]

    # cal the distance between point to rotary table center
    apt_X = math.sqrt(x*x + y*y)
    last_apt_X = math.sqrt(last_x*last_x + last_y*last_y)

    delta_x = apt_X - last_apt_X
    delta_z = apt[2] - last_apt[2]

    distance = math.sqrt(delta_x*delta_x + delta_z*delta_z)
    time = distance / feed
    #print(time,feed,distance)
    sum = 0
    for i in range(0,5):
        sum = sum + math.pow(zb[i]-last_zb[i], 2)

    xyzab_distance = math.sqrt(sum)
    #print(xyzab_distance)
    feed_output = xyzab_distance / time
    #print('-------------')
    return feed_output




if __name__ == "__main__":
    _init()
    set_value('standoff', 9.3)
    print(get_value("standoff"))
    set_value('standoff', 6)
    print(get_value("standoff"))
