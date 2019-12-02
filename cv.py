#note: can only be used for 2nd,3th quadrant
def cal_feed(zb_old, zb_old_last, zb_new, zb_new_last, feed_old):
    zb_old = list(map(float,zb_old))
    zb_old_last = list(map(float,zb_old_last))
    feed_old = float(feed_old)

    sum = 0
    for i in range(0,5):
        sum = sum + math.pow(zb_old[i]-zb_old_last[i], 2)
    xyzab_distance_old = math.sqrt(sum)
    time = xyzab_distance_old / feed_old

    sum = 0
    for i in range(0,5):
        sum = sum + math.pow(zb_new[i]-zb_new_last[i], 2)
    xyzab_distance_new = math.sqrt(sum)

    feed_new = xyzab_distance_new / time
    print(feed_new)
    return feed_new


import os, re, math

dir = os.getcwd()

filename = rf"{dir}\cv_input.txt"

file = open(filename, encoding='utf-8-sig')
txt_temp = file.readlines()
file.close
txt_out = ['Y0F6000']

for index, i in enumerate(txt_temp):
    if len(re.findall('-?\d+\.\d+', i)) < 5:
        txt_out.append(i.strip())
        continue

    N_num = re.match('N\d+', i).group()
    point_before = re.findall('-?\d+\.\d+', i)[0:5]
    feed_old = re.findall('-?\d+\.\d+', i)[5]
    #print(point_before)
    x0 = float(point_before[0]) - 30
    y0 = float(point_before[1])
    z0 = float(point_before[2])
    a0 = float(point_before[3])
    b0 = float(point_before[4])
    #print(x0, y0, z0, a0, b0)
    x = -math.sqrt(x0*x0 + y0*y0) + 30
    y = 0
    z = z0
    a = a0
    b = b0 - math.degrees(math.atan(y0/x0))
    #print(x,y,z,a,b)
    zb_new = [x, y, z, a, b]



    if index == 0:
        N_block = N_num + 'X' + str(round(x,4)) + \
            'Z' + str(round(z,4)) + 'A' + str(round(a,3)) + 'B' + str(round(b,3)) + 'F6000.0'
    else:
        feed_new = cal_feed(point_before, zb_old_last, zb_new, zb_new_last, feed_old)
        N_block = N_num + 'X' + str(round(x,4)) + \
            'Z' + str(round(z,4)) + 'A' + str(round(a,3)) + 'B' + str(round(b,3)) + 'F[' + str(round(feed_new,2)) + '/#100]'

    zb_new_last = [x, y, z, a, b]
    zb_old_last = point_before
    txt_out.append(N_block)

for i in txt_out:
    print(i)

filename_out = rf"{dir}\cv_output.txt"
file_out = open(filename_out, mode='w', encoding='utf-8')
for i in txt_out:
    file_out.write(i + '\n')
file_out.close
