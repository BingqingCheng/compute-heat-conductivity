import sys
import numpy as np
import scipy
from scipy.optimize import curve_fit
#import matplotlib.pyplot as plt
from math import pi

def S_k_omega(w,ksqr,gamma,DT,cs,b):
    """
    gamma: cp/cv
    DT: heat diffusivity
    cs: speed of sound
    b: Kinematic longitudinal viscosity
    ca: sound attentation
    """
    k = np.sqrt(ksqr)
    # sound attenuation constant
    ca = (gamma-1)/2.*DT + b/2.
    pole1 = (w+cs*k)**2 + (ca*ksqr)**2
    pole2 = (w-cs*k)**2 + (ca*ksqr)**2
    Skw = (gamma-1.)/gamma*(2.*DT*ksqr)/(w**2+(DT*ksqr)**2)
    Skw += (ca*ksqr/gamma)*(1./pole1+1./pole2)
    return Skw

def main(stemperature=1.0, sdensity=0.2, sysname="density-real", snumk='512'):

    temperature = round(float(stemperature),1)
    density = round(float(sdensity),1)
    numk = int(snumk)

    # read in the thermal properties
    thermal_list = np.genfromtxt("../../thermodynamic-properties/thermal-properties-direct.dat")
    thermal_dict = {0:{0:[]}}
    for entry in thermal_list:
        T = round(entry[0],1)
        thermal_dict[T]={}
    for entry in thermal_list:
        T = round(entry[0],1)
        D = round(entry[1],1)
        thermal_dict[T][D] = entry[2:]
    [ cv_now, cp_now, gamma_now, Xt_now, cs_now ] = thermal_dict[temperature][density]

    # read in the k grid
    k_grid = np.loadtxt("kgrid.dat", skiprows=0)[:,:]
    # read in the power spectrum
    fft_cxx = np.loadtxt("fft-"+sysname+".dat", skiprows=1)[:,:]
    omegas = fft_cxx[:,0]

    # get parameter at different k
    results_allk = np.zeros((numk,8), dtype=float)
    results_allk[:,1:4] = k_grid[:,:]

    for testindex in range(1,numk):
        fitresult = []
        ksqr_now = np.sum(np.square(k_grid[testindex]))
        def func(x, a, b):
            return S_k_omega(x, ksqr_now, gamma_now , a/cp_now, cs_now, b)
        try:
            popt, pcov = curve_fit(func, omegas, fft_cxx[:,testindex])
            perr = np.sqrt(np.diag(pcov))
            print(ksqr_now, popt, perr)
        except:
            popt = [float('nan'), float('nan'), float('nan')]
            perr = [float('nan'), float('nan'), float('nan')]
        results_allk[testindex, 0] = ksqr_now
        results_allk[testindex, -4:] = [popt[0], perr[0], popt[1], perr[1]]

    results_no_nan = [ a for a in results_allk if a[-1]>0 ]
    np.savetxt("fit-fft-"+sysname+".dat", results_no_nan, header='# k_sqr kx ky kz lambda lambda_error b b_error')

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2], sys.argv[3], sys.argv[4])
