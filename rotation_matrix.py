from numpy import mat
from math import sin, cos, radians, degrees, \
                radians, asin, atan2, fabs


def rot_y(de):
    t = mat([
                [ cos(de), 0, sin(de)],
                [ 0,       1,       0],
                [-sin(de), 0, cos(de)]
                                        ])
    return t


def rot_z(de):
    t = mat([
                [cos(de), -sin(de), 0],
                [sin(de),  cos(de), 0],
                [ 0,       0,       1]
                                        ])
    return t



def transf(x_apt, y_apt, z_apt, ii, jj, kk, last_b):
    i, j, k = -ii, -jj, -kk

    if i == 0:
        a = -degrees(atan2(k,j))
    else:
        a = degrees(asin(-k))

    if fabs(k) == 1:
        b = float(last_b)
    elif i == 0:
        b = 90
    else:
        b = degrees(atan2(j,i))


    nozzle_length = 3.63
    nozzle_offset = 7.63
    table_x_offset = 30
    table_z_offset = 54.375

    point_init = mat([nozzle_length, 0 , -nozzle_offset]).T

    point_after = rot_z(radians(b)) * rot_y(radians(a)) * point_init


    x = x_apt + table_x_offset - point_after[0,0]
    y = y_apt - point_after[1,0]
    z = table_z_offset - z_apt + point_after[2,0]


    #print(x, y, z, a, b)

    return [x, y, z, a, b]
