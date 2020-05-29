import matplotlib.pyplot as plt
plt.close('all')

L = [16, 14, 12, 10, 8, 6, 4]
Q_fail = [35, 35, 35, 25, 20, 20, 20]

plt.figure(dpi=350)
plt.plot(L, Q_fail)
plt.title("Simulation Failure Values")
plt.xlabel("Length of Condenser ($l_c/l_e$ = 1) [mm]")
plt.ylabel("Heat Input [W]")