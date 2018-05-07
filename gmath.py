import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    a = calculate_ambient(ambient, areflect)
    d = calculate_diffuse(light, dreflect, normal)
    s = calculate_specular(light, sreflect, view, normal)
    x = a[0] + d[0] + s[0]
    y = a[1] + d[1] + s[1]
    z = a[2] + d[2] + s[2]
    return limit_color([x,y,z])

def calculate_ambient(alight, areflect):
    x = int(alight[0] * areflect[0])
    y = int (alight[1] * areflect[1])
    z = int(alight[2] * areflect[2])
    return limit_color([x,y,z])

def calculate_diffuse(light, dreflect, normal):
    color_x = light[1][0] * dreflect[0] 
    color_y = light[1][1] * dreflect[1]
    color_z = light[1][2] * dreflect[2]
    l = normalize(light[0])
    n = normalize(normal)
    dot = dot_product(n,l)
    diffuse = [int(color_x*dot), int(color_y*dot), int(color_z*dot)]
    return limit_color(diffuse)

def calculate_specular(light, sreflect, view, normal):
    color_x = light[1][0] * sreflect[0] 
    color_y = light[1][1] * sreflect[1]
    color_z = light[1][2] * sreflect[2]
    color = [color_x, color_y, color_z]
    l = normalize(light[0])
    v = normalize(view)
    n = normalize(normal)
    first = [x*2*dot_product(n,l) for x in n]
    second = [x-y for x,y in zip(first,l)]
    third  = [int(x*(dot_product(second,v)**8)) for x in color]
    if dot_product(n,l) <= 0:
        return [0,0,0]
    return limit_color(third)

def limit_color(color):
    for x in range(len(color)):
        if color[x] <= 0:
            color[x] = 0
        if color[x] >= 255:
            color[x] = 255
    return color 

#vector functions
def normalize(vector):
    vx = float(vector[0]) 
    vy = float(vector[1])
    vz = float(vector[2])
    mag = math.sqrt(vx**2 + vy**2 + vz**2)
    return [vx/mag, vy/mag, vz/mag]
    

def dot_product(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
