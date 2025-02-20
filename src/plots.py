import matplotlib.pyplot as plt
plt.rcParams.update({
    "text.usetex": True})
import numpy as np
from functions_utils import *

phi = np.load("src/data/phi.npy")
psi =  np.load("src/data/psi.npy")
f = np.load("src/data/emissions.npy")
phi_usa = np.load("src/data/phi_USA.npy")
psi_usa = np.load("src/data/psi_USA.npy")
f_usa = np.load("src/data/usa_emissions.npy")
f_scope2_usa = np.load("src/data/sc2_usa_emissions.npy")



countries = ['AUS', 'AUT', 'BEL', 'BGR', 'BRA', 'CAN', 'CHE', 'CHN', 'CYP', 'CZE', 'DEU', 'DNK', 'ESP', 'EST',
             'FIN', 'FRA', 'GBR', 'GRC', 'HRV', 'HUN', 'IDN', 'IND', 'IRL', 'ITA', 'JPN', 'KOR', 'LTU', 'LUX',
             'LVA', 'MEX', 'MLT', 'NLD', 'NOR', 'POL', 'PRT', 'ROU', 'RUS', 'SVK', 'SVN', 'SWE', 'TUR', 'TWN',
             'USA', 'ROW']

sectors = ['A01', 'A02', 'A03', 'B', 'C10C12', 'C13C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23',
           'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31C32', 'C33', 'D35', 'E36', 'E37E39', 'F', 'G45',
           'G46', 'G47', 'H49', 'H50', 'H51', 'H52', 'H53', 'I', 'J58', 'J59J60', 'J61', 'J62J63', 'K64', 'K65',
           'K66', 'L68', 'M69M70', 'M71', 'M72', 'M73', 'M74M75', 'N', 'O84', 'P85', 'Q', 'RS','T', 'U']

#Figures in the paper
def figure4(): #Figure that plots the responsibility for five countries, as a function of the discount factor
    fig,ax = plt.subplots(1,2,sharey=True)
    ax[0].plot(varying_gamma(1000, phi, psi, 1, 1, f, "BRA", countries),label='BRA')
    ax[0].plot(varying_gamma(1000, phi, psi, 1, 1, f, "CAN", countries),label='CAN')
    ax[0].plot(varying_gamma(1000, phi, psi, 1, 1, f, "IDN", countries),label='IDN')
    ax[0].plot(varying_gamma(1000, phi, psi, 1, 1, f, "KOR", countries),label='KOR')
    ax[0].plot(varying_gamma(1000, phi, psi, 1, 1, f, "FRA", countries),label='FRA')
    ax[0].set_xlabel("Discount factor ($\gamma$)")
    ax[0].set_ylabel("Responsibility ($kton CO_2$)")
    ax[1].plot(varying_delta(1000, phi, psi, 1, 0, f, "BRA", countries),label='BRA')
    ax[1].plot(varying_delta(1000, phi, psi, 1, 0, f, "CAN", countries),label='CAN')
    ax[1].plot(varying_delta(1000, phi, psi, 1, 0, f, "IDN", countries),label='IDN')
    ax[1].plot(varying_delta(1000, phi, psi, 1, 0, f, "KOR", countries),label='KOR')
    ax[1].plot(varying_delta(1000, phi, psi, 1, 0, f, "FRA", countries),label='FRA')
    ax[1].set_xlabel("Discount factor ($\delta$)")
    ax[0].legend()
    ax[0].ticklabel_format(style='sci', axis='y', scilimits=(O, O))
    plt.tight_layout()
    plt.show()
    return

def figure5to8(country): #Figure that plots the responsibility of a single country as a function of the discount factor
    x = np.append(np.arange(0,1,0.025),0.99)
    upstream = varying_gamma(1000, phi, psi, 1, 1, f, country, countries)[1]
    downstream = varying_delta(1000, phi, psi, 1, 0, f, country, countries)[1]
    labda12 = [float(0.5)*upstream[i] + float(0.5)*downstream[i] for i in range(0,len(upstream))]
    plt.figure()
    plt.plot(x,upstream,label= fr"{country}, $\lambda = 1$ (upstream)")
    plt.plot(x,downstream,label = fr"{country}, $\lambda = 0$ (downstream)")
    plt.plot(x,labda12, label =fr"{country}, $\lambda = \frac{1}{2}$")
    plt.xlabel("Discount factor ($\gamma$ or $\delta$)")
    plt.ylabel("Responsibility $(kton CO_2)$")
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.legend()
    plt.show()
    return

def figure9_10(sector): #Figure that plots the responsibility of a single US sector as a function of the discount factor
    x = np.append(np.arange(0,1,0.025),0.99)
    upstream = varying_gamma_sect(1000, phi_usa, psi_usa, 1, 1, f_usa, sector, sectors)[1]
    downstream = varying_delta_sect(1000, phi_usa, psi_usa, 1, 0, f_usa, sector, sectors)[1]
    #labda12 = [float(0.5)*upstream[i] + float(0.5)*downstream[i] for i in range(0,len(upstream))]
    plt.plot(x,upstream,label= fr"{sector}, $\lambda = 1$ (upstream)")
    plt.plot(x,downstream,label = fr"{sector}, $\lambda = 0$ (downstream)")
    #plt.plot(x,labda12, label =fr"{sector}, $\lambda = \frac{1}{2}$")
    plt.xlabel("Discount factor ($\gamma$ or $\delta$)")
    plt.ylabel("Responsibility $(kton CO_2)$")
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.legend()
    plt.show()
    return


def figure11(list_sectors): #Figure that plots the responsibility of multiple sectors (added together) as a function of the discount factor
    x = np.append(np.arange(0,1,0.025),0.99)
    plt.figure()
    total_sector_upstream = np.zeros(len(x))
    total_sector_downstream = np.zeros(len(x))
    for sector in list_sectors:
        upstream = np.array(varying_gamma_sect(1000, phi_usa, psi_usa, 1, 1, f_usa, sector, sectors)[1])
        total_sector_upstream += upstream
        downstream = np.array(varying_delta_sect(1000, phi_usa, psi_usa, 1, 0, f_usa, sector, sectors)[1])
        total_sector_downstream += downstream
    plt.plot(x,total_sector_upstream, label="C, $\lambda = 1$ (upstream)") #Change label name 
    plt.plot(x,total_sector_downstream,label="C, $\lambda = 0$ (downstream)")
    plt.xlabel("Discount factor ($\gamma$ or $\delta$)")
    plt.ylabel("Responsibility $(kton CO_2)$")
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.show()
    return


def figure12(list_sectors): #Figure that plots the responsibility of multiple sectors (not added together) as a function of the discount factor
    x = np.append(np.arange(0,1,0.025),0.99)
    plt.figure()
    for sector in list_sectors:
        upstream = varying_gamma_sect(1000, phi_usa, psi_usa, 1, 1, f_usa, sector, sectors)[1]
        plt.plot(x,upstream, label=fr"{sector}")
    plt.xlabel("Discount factor ($\gamma$ or $\delta$)")
    plt.ylabel("Responsibility $(kton CO_2)$")
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0)
    plt.tight_layout()
    plt.show()
    return


def figure13(sector): #Figure that plots the scope 2 responsibility as a function of the discount factor. Emissions of sector D35 are allocated over all other sectors
    x = np.append(np.arange(0,1,0.025),0.99)
    if sector == "D35":
        direct = 0.0
    else: 
        direct = f_usa[sector_index(sector,sectors)]
    print("Direct emissions are",direct)
    scope2up = varying_gamma_sect(1000, phi_usa, psi_usa, 1, 1, f_scope2_usa, sector, sectors)[1]
    print("scope2up",scope2up)
    scope2down = varying_delta_sect(1000, phi_usa, psi_usa, 1, 0, f_scope2_usa, sector, sectors)[1]
    scope2_upstream = [a + direct for a in scope2up]
    print("scope2upstream",scope2_upstream)
    scope2_downstream = [a + direct for a in scope2down]
    plt.plot(x,scope2_upstream,label= fr"{sector}, $\lambda = 1$ (upstream)")
    plt.plot(x,scope2_downstream,label = fr"{sector}, $\lambda = 0$ (downstream)")
    plt.xlabel("Discount factor ($\gamma$ or $\delta$)")
    plt.ylabel("Responsibility $(kton CO_2)$")
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.tight_layout()
    plt.legend()
    plt.show()
    return

def figure14(sectorlist): #Figure that plots the scope 2 responsibility for an aggregated sector (e.g. sector C consisting of C10C12, C13C15,.. ,C33) as a function of the discount factor. Emissions of sector D35 are allocated over all other sectors
    x = np.append(np.arange(0,1,0.025),0.99)
    total_sector_upstream = np.zeros(len(x)) 
    total_sector_downstream = np.zeros(len(x)) 
    for sector in sectorlist:
        if sector == "D35":
            total_sector_upstream += np.zeros(len(x)) #Initialize with direct emissions, which are zero for sector D35 in this case
            total_sector_downstream += np.zeros(len(x)) 
        else: 
            total_sector_upstream += np.full(len(x),f_usa[sector_index(sector,sectors)])
            total_sector_downstream += np.full(len(x),f_usa[sector_index(sector,sectors)])
            print("direct for upsector",total_sector_upstream, sector)
        upstream = np.array(varying_gamma_sect(1000, phi_usa, psi_usa, 1, 1, f_scope2_usa, sector, sectors)[1])
        total_sector_upstream += upstream
        downstream = np.array(varying_delta_sect(1000, phi_usa, psi_usa, 1, 0, f_scope2_usa, sector, sectors)[1])
        total_sector_downstream += downstream
        print("total_sector_upstream","sector",total_sector_upstream,sector)
    plt.plot(x,total_sector_upstream,label="C, $\lambda = 1$ (upstream)") #Change label according to sector
    plt.plot(x,total_sector_downstream,label = "C, $\lambda = 0$ (downstream)")
    plt.xlabel("Discount factor ($\gamma$ or $\delta$)")
    plt.ylabel("Responsibility $(kton CO_2)$")
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.tight_layout()
    plt.legend()
    plt.show()
    return
