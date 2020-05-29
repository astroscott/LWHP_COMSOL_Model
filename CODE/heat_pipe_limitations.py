"""
This code is for estimating the performance limitations of a heat pipe.

Equations are from:
    "Mathematical Model for Heat Transfer Limitations of Heat Pipe"
    Patrik Nemec, et al.
    Mathematical and Computer Modelling, 2013

Author: Ezra McNichols
        NASA Glenn Research Center
        Turbomachinery and Turboelectric Systems
"""
import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol, nsolve
from thermo.chemical import Chemical

ax=plt.figure(1,figsize=(9,6)).add_subplot(1,1,1)
################################ Geometry ################################
#L_e=0.0254
#L_c=0.127
#L_a=0
#L_eff=0.5*L_e+L_a+0.5*L_c
g=9.81
#
#D_vane=0.377/np.pi
#q=500
##########################################################################

################################ Wick Properties ################################ 
#r_p=25e-6
#t=0.001
#epsilon=0.5
#A_w=np.pi*(D_vane)**2/4-np.pi*(D_vane-2*t)**2/4
#r_hv=(D_vane-2*t)/2
#k_s=130
#################################################################################

# Validation Parameters (Nemec et al, 2013, "Mathemtaical model for heat transfer limitations of heat pipe")
r_i=0.0065
r_hv=0.005
L_e=0.15
L_a=0.2
L_c=0.15
L_eff=0.5*L_e+L_a+0.5*L_c
A_w=0.000054
k_s=393
r_p=0.0001/2
epsilon=0.65
t=0.0015
L_t=0.5
T_w=298

#################################################################################

for T_hp in range(273,500,5):
    
    ################################ Fluid Properties ################################ 
    hp_fluid=Chemical('ethanol')
    
    hp_fluid.calculate(T=T_hp)
    P_v=hp_fluid.Psat
    hp_fluid.calculate(T=T_hp,P=P_v)
    
    rho_v=hp_fluid.rhog
    mu_v=hp_fluid.mug
    R_v=hp_fluid.Cpg-hp_fluid.Cvg
    #rho_v=P_v/(R_v*T_hp)
    gamma=hp_fluid.Cpg/hp_fluid.Cvg
    rho_l=hp_fluid.rhol
    mu_l=hp_fluid.mul
    k_l=hp_fluid.kl
    cp_l=hp_fluid.Cpl
    cv=hp_fluid.Cvg
    Pr_l=cp_l*mu_l/k_l
    h_fg=hp_fluid.Hvap
    sigma_l=hp_fluid.sigma
    
    print(T_hp-273)
    print("P_v = ", P_v)
    print("sigma_l = ", sigma_l)
    print("k_l = ", k_l)
    print("rho_v = ", rho_v)
    ##################################################################################
    
    ################################ Calculations ################################ 
    q=Symbol('q') 
    r_ce=0.443*r_p
    r_n=20e-6
    K=r_p**2*epsilon**3/(37.5*(1-epsilon)**2)
    A_v=np.pi*r_hv**2
    Re_v=2*r_hv*q/(A_v*mu_v*h_fg)
    c_fv=16/Re_v
    deltaPc=2*sigma_l/r_ce+rho_l*g*L_t*np.sin(90*np.pi/180)
    deltaPv=c_fv*Re_v*mu_v*L_eff*q/(2*r_hv**2*A_v*rho_v*h_fg)
    deltaPl=mu_l*L_eff*q/(K*A_w*rho_l*h_fg)
    f1=deltaPc-deltaPv-deltaPl
    q_cap=nsolve((f1),(q),(100))
    #k_eff=k_l*(2*k_l+k_s-2*(1-epsilon)*(k_l-k_s))/(2*k_l+k_s+(1-epsilon)*(k_l-k_s))
    #k_eff=(k_l*(k_l+k_s-(1-epsilon)*(k_l-k_s)))/(k_l+k_s+(1-epsilon)*(k_l-k_s))
    k_eff=k_s*(2+k_l/k_s-2*epsilon*(1-k_l/k_s))/(2+k_l/k_s+epsilon*(1-k_l/k_s))
    
    #q_boiling=k_eff*2*sigma_l*T_w/(t*rho_v*h_fg*r_ce)
    q_boiling=4*np.pi*L_eff*k_eff*T_hp*sigma_l/(h_fg*rho_v*np.log(r_i/r_hv))*(1/r_n-1/r_ce)
    q_sonic=1.41*A_v*rho_v*h_fg*np.sqrt(gamma*R_v*T_hp)*np.sqrt(1+gamma)/(2+gamma)
    q_ent=A_v*h_fg*np.sqrt(sigma_l*rho_v/(2*r_p))
    q_vis=r_hv**2*h_fg*rho_v*P_v*A_v/(c_fv*Re_v*mu_v*L_eff)
    q_cap2=sigma_l*rho_l*h_fg*K*A_w/(mu_l*L_eff)*(2/r_ce-rho_l*g*L_t*np.cos(180*np.pi/180)/sigma_l)
    ##############################################################################
    plt.plot(T_hp-273,q_cap,marker='o',color='red')
    plt.plot(T_hp-273,q_boiling,marker='x',color='orange')
    #plt.plot(T_hp-273,q_sonic,marker='D',color='pink')
    #plt.plot(T_hp-273,q_ent,marker='s',color='green')
    #plt.plot(T_hp-273,q_vis,marker='^',color='blue')
    plt.grid(True)
    plt.xlabel('Temperature [C]')
    plt.ylabel('Heat [W]')
     
plt.figure(1).legend(['Capillary Limit','Boiling Limit'])
plt.show()