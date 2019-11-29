#note: can only be used for 2nd,3th quadrant



import os, re, math

dir = os.getcwd()

filename = rf"{dir}\cv_input.txt"

file = open(filename, encoding='utf-8-sig')
txt_temp = file.readlines()
file.close
txt_out = ['Y0F6000']

for i in txt_temp:
    N_num = re.match('N\d+', i).group()
    point_before = re.findall('-?\d+\.\d+', i)[0:5]
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

    N_block = N_num + 'X' + str(round(x,4)) + \
            'Z' + str(round(z,4)) + 'A' + str(round(a,3)) + 'B' + str(round(b,3))

    txt_out.append(N_block)

for i in txt_out:
    print(i)

filename_out = rf"{dir}\cv_output.txt"
file_out = open(filename_out, mode='w', encoding='utf-8')
for i in txt_out:
    file_out.write(i + '\n')
file_out.close
