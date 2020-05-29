import pandas as pd

gtoggle = [0, 9.81]
Q = [5, 10, 20, 40]
Lc = [5, 10, 15]
Le = [5, 10, 15]

for a in range(len(gtoggle)):
    for b in range(len(Q)):
        for c in range(len(Lc)):
            for d in range(len(Le)):
                if a == 0:
                    gz = gtoggle[1]
                    gr = gtoggle[0]
                else:
                    gz = gtoggle[0]
                    gr = gtoggle[1]
                
                print(f'gz: {gz}\ngr: {gr}\nQ: {Q[b]}\nLc: {Lc[c]}\nLe: {Le[d]}\n')