# Computing_Methodology:
import numpy as n
import sys
def cap_cal(J,H,M,L,A,B,C,D,E,ROT1,ROT2,ROT3,ROT4,ROT5,S,w,l):
    J = float(J)
    H = float(H)
    M = float(M)
    L = float(L)
    A = float(A)
    B = float(B)
    C = float(C)
    D = float(D)
    E = float(E)
    ROT1 = float(ROT1)
    ROT2 = float(ROT2)
    ROT3 = float(ROT3)
    ROT4 = float(ROT4)
    ROT5 = float(ROT5)
    S = float(S)
    w = float(w)
    l = float(l)
    SUMCAT = J + H + M + L
    if SUMCAT != 100 :
        print("Input error; J%, H%, M%, L%", J, H, M, L)
        sys.exit()
    SUMCLASS = A + B + C + D + E
    if SUMCLASS != 100 :
        print("Input error; A%, B%, C%, D%, E%", A,B,C,D,E)
        sys.exit()
    J = J/100
    H = H/100
    M = M/100
    L = L/100
    A = A/100
    B = B/100
    C = C/100
    D = D/100
    E = E/100
    Cat_Mix = [L, M, H, J]
    App_Speed = [90, 105, 135, 150, 175]
    ROT = [ROT1, ROT2, ROT3, ROT4, ROT5]
    DEP_SEP = n.array([[60, 60, 60, 60],[120, 60, 60, 60],[120, 120, 60, 60],[180, 180, 120, 60]])
    RW_TIME_SEP = n.zeros((5,5), dtype=float, order='C')
    BUFFER = n.zeros((5,5), dtype=float, order='C')
    PROB_CLASSES = n.array([[A*A, A*B, A*C, A*D, A*E],[B*A, B*B, B*C, B*D, B*E],[C*A, C*B, C*C, C*D, C*E],[D*A, D*B, D*C, D*D, D*E],[E*A, E*B, E*C, E*D,E*E]])
    PROB_CATS = n.array([[L*L, L*M, L*H, L*J],[M*L, M*M, M*H, M*J],[H*L, H*M, H*H, H*J],[J*L, J*M, J*H, J*J]])
    EX_DEP_TIME = n.zeros((4,4), dtype=float, order='C')
    EX_ARR_TIME = n.zeros((5,5), dtype=float, order='C')
    GAP = n.zeros((5,5), dtype=float, order='C')
    N = n.zeros((5,5), dtype=float, order='C')
    TIME_DIFF = n.zeros((5,5), dtype=float, order='C')
    Y = n.zeros((5,5), dtype=float, order='C')
    NP = n.zeros((5,5), dtype=float, order='C')
#Departures_Only_Capacity_Calculation:
    for i in range(4):
        for j in range(4):
            EX_DEP_TIME[i][j] = PROB_CATS[i][j]*DEP_SEP[i][j]
    DEP_CAP = sum(EX_DEP_TIME[0]) + sum(EX_DEP_TIME[1]) + sum(EX_DEP_TIME[2]) + sum(EX_DEP_TIME[3]) + 30
    DEP_CAP_NBR = 3600/DEP_CAP
    x = 0
#Arrivals_Only_Capacity_Calculation:  
    for i in range(5):
        for j in range(5):
            if App_Speed[i] <= App_Speed[j]:
                RW_TIME_SEP[i][j] = max(3600*S/App_Speed[j],ROT[i])
                BUFFER[i][j] = 18*2
            else :
                a = l + S
                b = 1/App_Speed[j]
                c = 3600*l/App_Speed[i]
                d = a*b*3600
                RW_TIME_SEP[i][j] = max(d - c, ROT[i])
                e = 18*2
                f = 3600*S/App_Speed[j]
                g = 3600*S/App_Speed[i]
                h = f - g
                x = e - h
            if x > 0:
                BUFFER[i][j] = x
            else :
                BUFFER[i][j] = 0
    AUG_MATRIX = RW_TIME_SEP + BUFFER
    for i in range(5):
        for j in range(5):
            EX_ARR_TIME[i][j] = PROB_CLASSES[i][j]*AUG_MATRIX[i][j]
    ARR_CAP = sum(EX_ARR_TIME[0]) + sum(EX_ARR_TIME[1]) + sum(EX_ARR_TIME[2]) + sum(EX_ARR_TIME[3]) + sum(EX_ARR_TIME[4])
    ARR_CAP_NBR = 3600/ARR_CAP
#100%Arrivals+Departures_ Capacity_Calculation:
    for i in range(5):
        for j in range(5):
            a = 3600*w/App_Speed[j]
            GAP[i][j] = ROT[i] + a
            TIME_DIFF[i][j] = RW_TIME_SEP[i][j] - GAP[i][j]
            if TIME_DIFF[i][j] < 0 :
                TIME_DIFF[i][j] = 0
            Y[i][j] = TIME_DIFF[i][j]/DEP_CAP
            if Y[i][j] == 0:
                N[i][j] = 0
            else:
                if int(Y[i][j]) < 1:
                    N[i][j] = 1
                else:
                    N[i][j] = int(Y[i][j]) 
            NP[i][j] = N[i][j]*PROB_CLASSES[i][j]
    Nr = sum(NP[1]) + sum(NP[2]) + sum(NP[0]) + sum(NP[3]) + sum(NP[4])
    Cp = ARR_CAP_NBR - 1
    Rf = Nr * Cp
    if Rf > DEP_CAP_NBR :
        Rf = DEP_CAP_NBR
    Mixed_Mode_Cap = Rf
    return {"numberOfDeparturesToBeInserted":Mixed_Mode_Cap,"departuresOnlyCapacity":DEP_CAP_NBR,"arrivalsOnlyCapaciy":ARR_CAP_NBR}
