#  -*- coding:utf-8 -*-



import  numpy as np

import math

from PythontoBomJson.useful_tools import Noround, delphi_format

EPSILON = 1e-40

TVector3f = [0.1,0.1,0.1]

IdentityHmgMatrix = [[1, 0, 0, 0],

                     [0, 1, 0, 0],

                     [0, 0, 1, 0],

                     [0, 0, 0, 1]]

EmptyHmgMatrix = [[0, 0, 0, 0],

                 [0, 0, 0, 0],

                 [0, 0, 0, 0],

                 [0, 0, 0, 0]]

IdentityMatrix =[[1, 0, 0],

               [0, 1, 0],

               [0, 0, 1]]

X = 0

Y = 1

Z = 2

W = 3

oy = 1

oz = 0

yMatrix =[

    [math.cos(oy), 0, math.sin(oy), 0],

    [0, 1, 0, 0],

    [-math.sin(oy), 0, math.cos(oy), 0],

    [0, 0, 0, 1]

    ]

#// 绕z轴的旋转矩阵

zMatrix =[

[math.cos(oz), -math.sin(oz), 0, 0],

[math.sin(oz), math.cos(oz), 0, 0],

[0, 0, 1, 0],

[0, 0, 0, 1]

]



EPSILON2  = 1e-30

cOne = 1.0

def DegToRad(Degrees):

    Result = Degrees * (math.pi / 180)

    return Result



def CreateTranslationMatrix(V):

    Result = [[1, 0, 0, 0],

                     [0, 1, 0, 0],

                     [0, 0, 1, 0],

                     [0, 0, 0, 1]]

    Result[W][X] =V[X]

    Result[W][Y] =V[Y]

    Result[W][Z] =V[Z]

    return Result



def AffineVectorMake(x,y,z):

    Result = [0,0,0]

    Result[0] = x

    Result[1] = y

    Result[2] = z

    return Result



def CreateRotationMatrix(anAxis, angle):

    Result = [[1, 0, 0, 0],

              [0, 1, 0, 0],

              [0, 0, 1, 0],

              [0, 0, 0, 1]]

    sine, cosine = SinCos(angle)

    one_minus_cosine = 1 - cosine

    axis = VectorNormalize(anAxis)    #VectorNormalize???



    Result[X][X] = (one_minus_cosine * axis[0] * axis[0]) + cosine

    Result[X][Y] = (one_minus_cosine * axis[0] * axis[1]) - (axis[2] * sine)

    Result[X][Z] = (one_minus_cosine * axis[2] * axis[0]) + (axis[1] * sine)

    Result[X][W] = 0



    Result[Y][X] = (one_minus_cosine * axis[0] * axis[1]) + (axis[2] * sine)

    Result[Y][Y] = (one_minus_cosine * axis[1] * axis[1]) + cosine

    Result[Y][Z] = (one_minus_cosine * axis[1] * axis[2]) - (axis[0] * sine)

    Result[Y][W] = 0



    Result[Z][X] = (one_minus_cosine * axis[2] * axis[0]) - (axis[1] * sine)

    Result[Z][Y] = (one_minus_cosine * axis[1] * axis[2]) + (axis[0] * sine)

    Result[Z][Z] = (one_minus_cosine * axis[2] * axis[2]) + cosine

    Result[Z][W] = 0



    Result[W][X] = 0

    Result[W][Y] = 0

    Result[W][Z] = 0

    Result[W][W] = 1

    return Result



def VectorMake(x, y, z, w = 0):

    Result =[0,0,0,0]

    Result[0] = x

    Result[1] = y

    Result[2] = z

    Result[3] = w

    return Result



def MakeVector(v,x,y,z):

    v[0] = x

    v[1] = y

    v[2] = z



    return v



def SetVector(v ,x, y, z):



   v[0]=x

   v[1]=y

   v[2]=z

   return v



def SinCos(angle):

    # s =('%.4f' % math.sin(angle))

    # c =('%.4f' % math.cos(angle))

    s = math.sin(angle)

    if angle == 1.5707963705 or angle == math.pi/2 or angle == -math.pi/2:

        c = -4.37113882867379E-8

        print('7777777')

    else:

        c = math.cos(angle)

        print('7777778')

    print('s=',s,'c=',c)

    return s,c



def CreateRotationMatrixX( angle ) :

    s,c =SinCos(angle)

    print(s,c)

    Result = CreateRotationMatrixX1(s, c)

    return Result



def CreateRotationMatrixX1(sine, cosine) :





    Result = [[0, 0, 0, 0],

                 [0, 0, 0, 0],

                 [0, 0, 0, 0],

                 [0, 0, 0, 0]]

    Result[X][X] = 1

    Result[Y][Y] = cosine

    print('cosine=',cosine)

    print('Result[Y][Y]=',Result[Y][Y])

    Result[Y][Z] = sine

    Result[Z][Y] = -sine

    Result[Z][Z] = cosine

    Result[W][W] = 1

    return Result



def CreateRotationMatrixZ( angle ) :

    s,c = SinCos(angle)

    Result = CreateRotationMatrixZ1(s, c)

    return Result



def CreateRotationMatrixZ1(sine, cosine):

    Result = [[0, 0, 0, 0],

                 [0, 0, 0, 0],

                 [0, 0, 0, 0],

                 [0, 0, 0, 0]]

    Result[X][X] = cosine

    Result[X][Y] = sine

    Result[Y][X] = -sine

    Result[Y][Y] = cosine

    Result[Z][Z] = 1

    Result[W][W] = 1

    return Result



def MatrixMultiply(m1,m2):

    return (np.mat(m1) * np.mat(m2))



def VectorTransform(V,M):

    Result = [0,0,0,0]

    M = M.tolist()

    if len(V)<=3:

        Result = [0, 0, 0]

        #print V

        Result[X] = V[X] * M[X][X] + V[Y] * M[Y][X] + V[Z] * M[Z][X] + M[W][X]

        #print V[Y],M[Y][Y]

        #print VGround(V[X], 8) * VGround(M[X][Y], 8),VGround(V[Y], 8) * VGround(M[Y][Y], 8),V[Z] * M[Z][Y],M[W][Y]

        Result[Y] = delphi_format(V[X] * M[X][Y] + V[Y] * M[Y][Y] + V[Z] * M[Z][Y] + M[W][Y],4)

        Result[Z] = delphi_format(V[X] * M[X][Z] + V[Y] * M[Y][Z] + V[Z] * M[Z][Z] + M[W][Z],4)

        #print Result

        return Result

    else:

        #print 'V=',V,'M=',M

        #print V[X],M[X][X], V[Y], M[Y][X], V[Z], M[Z][X]

        Result[X] = V[X] * M[X][X] + V[Y] * M[Y][X] + V[Z] * M[Z][X]

        Result[Y] = V[X] * M[X][Y] + V[Y] * M[Y][Y] + V[Z] * M[Z][Y]

        Result[Z] = V[X] * M[X][Z] + V[Y] * M[Y][Z] + V[Z] * M[Z][Z]

        Result[W] = V[W]

        return Result



def MatrixDeterminant(M):

    Result =  M[X][X] * (M[Y][Y] * M[Z][Z] - M[Z][Y] * M[Y][Z])- M[X][Y] * (M[Y][X] * M[Z][Z] - M[Z][X] * M[Y][Z])+ M[X][Z] * (M[Y][X] * M[Z][Y] - M[Z][X] * M[Y][Y])

    return Result



def MatrixDetInternal( a1, a2, a3, b1, b2, b3, c1, c2, c3):



    Result=  a1 * (b2 * c3 - b3 * c2) - b1 * (a2 * c3 - a3 * c2) + c1 * (a2 * b3 - a3 * b2)

    return Result



def VGround(anum, x):

    # 按指定的位数x进行anum的小数截取, 不四舍五入

    xx = int("1" + "0" * x)

    bnum = int(anum * xx) / xx

    return (bnum)



def AdjointMatrix(M):

    a1 = VGround(M[X][X], 8)

    b1 = VGround(M[X][Y], 8)

    c1 = VGround(M[X][Z], 8)

    d1 = VGround(M[X][W], 8)

    a2 = VGround(M[Y][X], 8)

    b2 = VGround(M[Y][Y], 8)

    c2 = VGround(M[Y][Z], 8)

    d2 = VGround(M[Y][W], 8)

    a3 = VGround(M[Z][X], 8)

    b3 = VGround(M[Z][Y], 8)

    c3 = VGround(M[Z][Z], 8)

    d3 = VGround(M[Z][W], 8)

    a4 = VGround(M[W][X], 8)

    b4 = VGround(M[W][Y], 8)

    c4 = VGround(M[W][Z], 8)

    d4 = VGround(M[W][W], 8)

    # a1= M[X][X]

    # b1= M[X][Y]

    # c1= M[X][Z]

    # d1= M[X][W]

    # a2= M[Y][X]

    # b2= M[Y][Y]

    # c2= M[Y][Z]

    # d2= M[Y][W]

    # a3= M[Z][X]

    # b3= M[Z][Y]

    # c3= M[Z][Z]

    # d3= M[Z][W]

    # a4= M[W][X]

    # b4= M[W][Y]

    # c4= M[W][Z]

    # d4= M[W][W]



    M[X][X]= MatrixDetInternal(b2, b3, b4, c2, c3, c4, d2, d3, d4)



    M[Y][X]=-MatrixDetInternal(a2, a3, a4, c2, c3, c4, d2, d3, d4)

    M[Z][X]= MatrixDetInternal(a2, a3, a4, b2, b3, b4, d2, d3, d4)

    M[W][X]=-MatrixDetInternal(a2, a3, a4, b2, b3, b4, c2, c3, c4)



    M[X][Y]=-MatrixDetInternal(b1, b3, b4, c1, c3, c4, d1, d3, d4)

    M[Y][Y]= MatrixDetInternal(a1, a3, a4, c1, c3, c4, d1, d3, d4)

    M[Z][Y]=-MatrixDetInternal(a1, a3, a4, b1, b3, b4, d1, d3, d4)

    M[W][Y]= MatrixDetInternal(a1, a3, a4, b1, b3, b4, c1, c3, c4)



    M[X][Z]= MatrixDetInternal(b1, b2, b4, c1, c2, c4, d1, d2, d4)

    M[Y][Z]=-MatrixDetInternal(a1, a2, a4, c1, c2, c4, d1, d2, d4)

    M[Z][Z]= MatrixDetInternal(a1, a2, a4, b1, b2, b4, d1, d2, d4)

    M[W][Z]=-MatrixDetInternal(a1, a2, a4, b1, b2, b4, c1, c2, c4)



    M[X][W]=-MatrixDetInternal(b1, b2, b3, c1, c2, c3, d1, d2, d3)

    M[Y][W]= MatrixDetInternal(a1, a2, a3, c1, c2, c3, d1, d2, d3)

    M[Z][W]=-MatrixDetInternal(a1, a2, a3, b1, b2, b3, d1, d2, d3)

    M[W][W]= MatrixDetInternal(a1, a2, a3, b1, b2, b3, c1, c2, c3)



def ScaleMatrix( M, factor):

   for i in range(0,2):

      M[i][0] = M[i][0] * factor

      M[i][1] = M[i][1] * factor

      M[i][2] = M[i][2] * factor

      M[i][3] = M[i][3] * factor



def InvertMatrix(M):



    det = MatrixDeterminant(M)



    if abs(det) < EPSILON :

        M = IdentityMatrix



    else:

        AdjointMatrix(M)

        ScaleMatrix(M, 1/det)



    return M



def MatrixInvert(M):

    if not isinstance(M, list):

        M = M.tolist()

    Result = M

    Result = InvertMatrix(Result)

    return np.mat(Result)



class TQuaternion(object):

    def __init__(self):



        self.ImagPart = AffineVectorMake(0,0,0)

        self.RealPart = 0



def MaxFloat(v1,v2):

    Result = 0

    if v1 > v2 :Result =v1

    else: Result =v2

    return Result



def VectorNorm(v) :



   Result =v[0]*v[0]+v[1]*v[1]+v[2]*v[2]

   return Result



def QuaternionMagnitude(q) :



   Result =math.sqrt(VectorNorm(q.ImagPart)+math.pow(q.RealPart, 2))

   return Result



def ScaleVector(v,factor):

    v[0] =v[0]*factor

    v[1] =v[1]*factor

    v[2] =v[2]*factor



def  NormalizeQuaternion(q):



   m =QuaternionMagnitude(q)

   if m >EPSILON2 :

        f = 1/m

        ScaleVector(q.ImagPart, f)

        q.RealPart = q.RealPart*f

   else:

       q .ImagPart = [0,0,0]

       q. RealPart = 1



def QuaternionFromMatrix(mat) :

    Result = TQuaternion()

    if not isinstance(mat,list):

        mat = mat.tolist()

    #print mat,mat[0][0],mat[1][1],mat[2][2]

    traceMat  = 1 + mat[0][0] + mat[1][1] + mat[2][2]

    if traceMat> EPSILON2 :



        s =math.sqrt(traceMat)*2

        invS =1/s

        Result.ImagPart[0] = (mat[1][2]-mat[2][1])*invS

        Result.ImagPart[1] = (mat[2][0]-mat[0][2])*invS

        Result.ImagPart[2] = (mat[0][1]-mat[1][0])*invS

        Result.RealPart = 0.25*s

    elif (mat[0][0]>mat[1][1]) and (mat[0][0]>mat[2][2]) :

        s =math.sqrt(MaxFloat(EPSILON2, cOne+mat[0][0]-mat[1][1]-mat[2][2]))*2

        invS =1/s

        Result.ImagPart[0] =0.25*s

        Result.ImagPart[1] =(mat[0,1]+mat[1,0])*invS

        Result.ImagPart[2] =(mat[2,0]+mat[0,2])*invS

        Result.RealPart   =(mat[1,2]-mat[2,1])*invS

    elif (mat[1][1]>mat[2][2]):

        s = math.sqrt(MaxFloat(EPSILON2, cOne+mat[1,1]-mat[0][0]-mat[2][2]))*2

        invS =1/s

        Result.ImagPart[0] =(mat[0][1]+mat[1][0])*invS

        Result.ImagPart[1] =0.25*s

        Result.ImagPart[2] =(mat[1][2]+mat[2][1])*invS

        Result.RealPart    =(mat[2][0]-mat[0][2])*invS

    else:

        s =math.sqrt(MaxFloat(EPSILON2, cOne+mat[2][2]-mat[0][0]-mat[1][1]))*2

        invS =1/s

        Result.ImagPart[0]=(mat[2][0]+mat[0][2])*invS

        Result.ImagPart[1]=(mat[1,2]+mat[2][1])*invS

        Result.ImagPart[2]=0.25*s

        Result.RealPart   =(mat[0,1]-mat[1][0])*invS



    NormalizeQuaternion(Result)

    return Result



def ClampValue(aValue, aMin, aMax ):

    if aValue < aMin : Result = aMin



    elif(aValue > aMax) : Result = aMax

    else: Result = aValue

    return Result



def RadToDeg(Radians):



   Result = Radians*(180/math.pi)

   return Result



def QuaternionToRollPitchYaw(q, roll, pitch, yaw):

    x = q.ImagPart[0]

    y = q.ImagPart[1]

    z = q.ImagPart[2]

    w = q.RealPart

    roll = math.atan2(2 * (w * z + x * y), 1 - 2 * (z * z + x * x))

    pitch = math.asin(ClampValue(2 * (w * x - y * z), -1.0, 1.0))

    yaw = math.atan2(2 * (w * y + z * x), 1 - 2 * (x * x + y * y))

    return roll,pitch,yaw



if __name__ =='__main__':

    pass

    # def pnumber(num):

    #     if int(num)==float(num): return int(num)

    #     else: return float(num)

    # from decimal import *

    # getcontext().prec = 10

    # m3 = CreateRotationMatrixX(math.pi/2)

    # with open('1.txt','w') as f:

    #     print 'm3[1][2]=',m3[1][1]

    #     f.write('p.m=' + str(pnumber(m3[0][0])) + ',' + str(pnumber(m3[0][1])) + ',' + str(pnumber(m3[0][2])) + ',' + str(

    #         pnumber(m3[0][3])) + ',' \

    #             + str((m3[1][0])) + ',' + str((m3[1][1])) + ',' + str((m3[1][2])) + ',' + str(

    #         (m3[1][3])) + ',' \

    #             + str((m3[2][0])) + ',' + str((m3[2][1])) + ',' + str((m3[2][2])) + ',' + str(

    #         (m3[2][3])) + ',' \

    #             + str(pnumber(m3[3][0])) + ',' + str(pnumber(m3[3][1])) + ',' + str(pnumber(m3[3][2])) + ',' + str(

    #         pnumber(m3[3][3])) + '\n')

    # IdentityHmgMatrix = [[1, 0, 0, 0],

    #                      [0, 1, 0, 0],

    #                      [0, 0, 1, 0],

    #                      [0, 0, 0, 1]]

    # m = np.mat([[0, 1,  0, 0],[-1,  0,  0, 0],[0,0,1,0],[2565 , 1418 , 60,  1]])

    #

    # m1 = np.mat([[ 0.000e+00,  1.000e+00 , 0.000e+00 , 0.000e+00],

    #  [-1.000e+00 , 0.000e+00 , 0.000e+00 , 0.000e+00],

    #  [ 0.000e+00 , 0.000e+00 , 1.000e+00 , 0.000e+00],

    #  [ 2.527e+03 , 1.418e+03 , 0.000e+00 , 1.000e+00]])

    # tm = MatrixMultiply(m1, MatrixInvert(m))

    # print tm

    # q = QuaternionFromMatrix(tm)

    # roll = 0

    # pitch = 0

    # yaw = 0

    # roll, pitch, yaw = QuaternionToRollPitchYaw(q, roll, pitch, yaw)

    # print q.ImagPart

    # print q.RealPart

    # print roll, pitch, yaw

    #print math.atan2(11.08246118811, 120.10203994937)

    # v1 = [0,44,9]

    #

    # m = np.mat([[-4.37113882867379E-8,1,0,0],[ -1,-4.37113882867379E-8,0,0],[ 0,  0,  1,  0],[409.999969482422,1509,78,1.0]])

    #

    # v1 = VectorTransform(v1, m)

    # print '',v1

    # v1 = VectorTransform(v1, MatrixInvert(m))

    # print v1