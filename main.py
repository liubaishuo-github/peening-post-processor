def txt_connect(txt_before):  #connect the lines divided by $, and put into txt
    txt = []
    temp = ''
    for i in txt_before:
        i = i.strip()
        if i == '':
            continue
        if i[-1] != '$':
            txt.append((temp + i).strip())
            temp = ''
        else:
            temp = temp + i.rstrip('$')
    return txt

def op_goto(apt, last, feedratee, last_feedd):
    pch_val = rotation_matrix.transf(*list(map(float,apt)),last[4])
    #print(pch_val)
    x = str(round(pch_val[0], 4))
    y = str(round(pch_val[1], 4))
    z = str(round(pch_val[2], 4))
    a = str(round(pch_val[3], 3))
    b = str(round(pch_val[4], 3))

    if float(x) != float(last[0]):
        str_x = 'X' + x
    else:
        str_x = ''

    if float(y) != float(last[1]):
        str_y = 'Y' + y
    else:
        str_y = ''

    if float(z) != float(last[2]):
        str_z = 'Z' + z
    else:
        str_z = ''

    if float(a) != float(last[3]):
        str_a = 'A' + a
    else:
        str_a = ''

    if float(b) != float(last[4]):
        str_b = 'B' + b
    else:
        str_b = ''

    if feedratee != last_feedd:
        str_f = 'F' + str(round(feedratee, 1))
    else:
        str_f = ''

    n_block = str_x + str_y + str_z + str_a + str_b + str_f
    last_zbb = [x, y, z, a, b]
    last_feedd = feedratee
    return n_block, last_zbb, last_feedd
#=====================main==========================
#=====================main==========================

import os, re, datetime
import rotation_matrix , op
dir = os.getcwd()

filename = rf"{dir}\peening.aptsource"

file = open(filename, encoding='utf-8-sig')
txt_temp = file.readlines()
file.close

txt = txt_connect(txt_temp)
#for i in txt:
#    print(i)
#print('-------')

ppword_list = ['PPRINT', 'RAPID', 'FEDRAT', 'STOP', 'DWELL', 'AIR',\
                'STEEL', 'GLASS', 'RECIPE', 'SPINDLE', 'SUBPROGRAM']

pch = []
last_zb = ['0', '0', '0', '0', '0']
op._init()
op.set_value('feedrate', 6000.0)
last_feed = 6000.0
feedrate = 6000.0
for i in txt:
    if i[0:4] == 'GOTO':
        apt_point = re.findall('-?\d+\.\d+',i)
        #print(apt_point
        temp = op_goto(apt_point, last_zb, feedrate, last_feed)
        pch.append(temp[0])
        last_zb = temp[1]
        last_feed = temp[2]
    for j in ppword_list:
        ppword_match_object = re.match(j,i)
        if ppword_match_object:
            ppword = ppword_match_object.group()
            print("match success:" + j)
            exec('temp = op.'+ ppword + '(i)')
            #print(type(temp))
            if temp[0] == 1:
                pch.append(temp[1])
            elif temp[0] ==2:
                pch.extend(temp[1])
            break
    feedrate = op.get_value('feedrate')

    #print('in main, the feedrate is:' + str(feedrate))



pch.insert(0,'X0Z0A0B0F6000.0')
pch.insert(1,'Y0')
n = 10
for indexx, valuee in enumerate(pch):
    if valuee[0] != '(':
        pch[indexx] = 'N' + str(n) + valuee
        n = n + 10

dt = datetime.datetime.now()
time_str = '(Generate on  ' + dt.strftime('%b-%d-%Y  %H:%M:%S') + ')'
pch.insert(0, time_str)



print('============')
for i in pch:
    print(i)

filename_out = rf"{dir}\peening.ppg"
file_out = open(filename_out, mode='w', encoding='utf-8')
for i in pch:
    file_out.write(i + '\n')
file_out.close
