import numpy as np

def truncation_sum(q, discount, matrix):  
    res = np.zeros(matrix.shape)
    for i in range(q):
        res = res + np.linalg.matrix_power(discount * matrix, i)
    return res

def q_approx(q, up, down, gamma, delta, labda, f):
    up_resp = (1-gamma) * np.matmul(truncation_sum(q, gamma, up), f)
    down_resp = (1-delta) * np.matmul(truncation_sum(q, delta, down), f)
    return labda * up_resp + (1-labda) * down_resp

def q_approx_sect(q, up_sect, down_sect, gamma, delta, labda, f_sect):
    up_resp_sect = (1-gamma) * np.matmul(truncation_sum(q, gamma, up_sect), f_sect)
    down_resp_sect = (1-delta) * np.matmul(truncation_sum(q, delta, down_sect), f_sect)
    return labda * up_resp_sect + (1-labda) * down_resp_sect

def country_index(ctry, countries):
    return countries.index(ctry)

def sector_index(sect, sectors):
    return sectors.index(sect)

def varying_gamma(q, up, down, delta, labda, f, ctry, countries):
    y = []
    x = np.append(np.arange(0,1,0.025),0.99)
    indx = country_index(ctry, countries)
    for gamma in x:
        resp = q_approx(q, up, down, gamma, delta, labda, f)
        y.append(int(resp[indx]))
    return x, y

def varying_delta(q, up, down, gamma, labda, f, ctry, countries):
    y = []
    x = np.append(np.arange(0,1,0.025),0.99)
    indx = country_index(ctry, countries)
    for delta in x:
        resp = q_approx(q, up, down, gamma, delta, labda, f)
        y.append(int(resp[indx]))
    return x, y

def varying_gamma_sect(q, up_sect, down_sect, delta, labda, f_sect, sect, sectors):
    y_sect = []
    x_sect = np.append(np.arange(0,1,0.025),0.99)
    indx = sector_index(sect, sectors)
    for gamma in x_sect:
        resp_sect = q_approx_sect(q, up_sect, down_sect, gamma, delta, labda, f_sect)
        y_sect.append(int(resp_sect[indx]))
    return x_sect, y_sect

def varying_delta_sect(q, up_sect, down_sect, gamma, labda, f_sect, sect, sectors):
    y_sect = []
    x_sect = np.append(np.arange(0,1,0.025),0.99)
    indx = sector_index(sect, sectors)
    for delta in x_sect:
        resp_sect = q_approx(q, up_sect, down_sect, gamma, delta, labda, f_sect)
        y_sect.append(int(resp_sect[indx]))
    return x_sect, y_sect

def labda_half(q,up,down,delta,gamma,labda1,labda2, f,ctry,countries):
    upstream = varying_gamma(q, up, down, delta, labda1, f, ctry, countries)[1]
    downstream = varying_delta(q, up, down, gamma, labda2, f, ctry, countries)[1]
    return [float(0.5)*(a+b) for a, b in zip(upstream,downstream)]

