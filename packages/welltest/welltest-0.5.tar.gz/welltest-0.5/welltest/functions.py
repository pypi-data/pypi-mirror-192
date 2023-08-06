"""
simple welltest functions
ver 0.2 from 20/01/2022
Khabibullin Rinat
"""

import numpy as np
from scipy.special import  expi

# Define functions for converting dimensional variables into dimensionless variables and vice versa
# to be used later for graphing and calculations

# Naming functions, we'll keep following conventions
# first comes the name of what we're looking at
# at the end comes result dimension, if appropriate

def r_from_rd_m(rd, rw_m=0.1):
    """
    translate dimensionless distance into dimensional distance
    rd - dimensionless distance
    rw_m - well radius, m
    """
    return rd*rw_m


def rd_from_r(r_m, rw_m=0.1):
    """
    translate dimensional distance to dimensionless distance
    r_m - dimensional distance, m
    rw_m - well radius, m
    """
    return r_m/rw_m


def t_from_td_hr(td, k_mD=10, phi=0.2, mu_cP=1, ct_1atm=1e-5, rw_m=0.1):
    """
    conversion of dimensionless time to dimensional time, result in hours
    td - dimensionless time
    k_mD - formation permeability, mD
    phi - porosity, fractions of units
    mu_cP - dynamic fluid viscosity, cP
    ct_1atm - total compressibility, 1/atm
    rw_m - well radius, m
    """
    return td * phi * mu_cP * ct_1atm * rw_m * rw_m / k_mD / 0.00036


def td_from_t(t_hr, k_mD=10, phi=0.2, mu_cP=1, ct_1atm=1e-5, rw_m=0.1):
    """
    dimension time conversion to dimensionless time
    t_hr - dimensional time, hour
    k_mD - formation permeability, mD
    phi - porosity, fractions of units
    mu_cP - dynamic fluid viscosity, cP
    ct_1atm - total compressibility, 1/atm
    rw_m - well radius, m
    """
    return 0.00036 * t_hr * k_mD / (phi * mu_cP * ct_1atm * rw_m * rw_m) 

def p_from_pd_atma(pd, k_mD=10, h_m=10, q_sm3day=20, b_m3m3=1.2, mu_cP=1, pi_atma=250):
    """
    conversion of dimensionless pressure to dimensional pressure, result in absolute atmospheres
    pd - dimensionless pressure
    k_mD - formation permeability, mD
    h_m - reservoir thickness, m
    q_sm3day - flow rate at the surface, m3 /day in s.c.
    fvf_m3m3 - oil volumetric ratio, m3/m3
    mu_cP - dynamic viscosity of fluid, cP
    pi_atma - initial pressure, absolute atm
    """
    return pi_atma - pd * 18.41 * q_sm3day * b_m3m3 * mu_cP / k_mD / h_m 

def pd_from_p(p_atma, k_mD=10, h_m=10, q_sm3day=20, b_m3m3=1.2, mu_cP=1, pi_atma=250):
    """
    translate dimensional pressure into dimensionless pressure
    p_atma - pressure
    k_mD - formation permeability, mD
    h_m - reservoir thickness, m
    q_sm3day - flow rate at the surface, m3/day in s.c.
    fvf_m3m3 - oil volumetric ratio, m3/m3
    mu_cP - dynamic viscosity of fluid, cP
    pi_atma - initial pressure, absolute atm
    """
    return (pi_atma - p_atma) / (18.41 * q_sm3day * b_m3m3 * mu_cP) * k_mD * h_m 


# Line source solution for diffusivity equation
def pd_ei(td, rd=1):
    """
    Line source solution for diffusivity equation
    td - time dimensionless 
    rd - radius dimensionless, distance from well
    """
    # when calculating, make sure that td=0 will not affect the calculation, even if td is an array and only one element is zero
    td = np.array(td, dtype = float)
    return np.multiply(-0.5, 
                       expi(np.divide(-rd**2 / 4 , 
                                      td, 
                                      out=np.zeros_like(td), where=td!=0)), 
                       out=np.zeros_like(td), where=td!=0)


def pd_superposition(td, td_hist, qd_hist, rd=1):
    """
    calculation of dimensionless pressure for the sequence of dimensionless flow rates
    td - calculation time after startup, dimensionless
    td_hist - array of well operation mode change times, dimensionless
    qd_hist - array of flow rates set after regime change, dimensionless
    rd - radius dimensionless, distance from well
    """
    # forcibly add zeros to the input arrays to account for well startup
    qdh = np.hstack([0, qd_hist])
    tdh = np.hstack([0, td_hist])
    # plot the virtual wells' flow rates - the differences of the real flow rates at switching
    delta_qd = np.hstack([0, np.diff(qdh)])
    # reference dimensionless flow rate is 1
    
    # vector magic - time can be a vector and switching flow rates is also a vector
    # we must arrange sum over times, each of which is a sum over switches
    # we do it by means of meshgrid calculation and searching for accumulated sums
    qd_v, td_v =np.meshgrid(delta_qd, td)
    # use cumulative sum numpy to sum the results
    dpd = np.cumsum(qd_v * pd_ei((td_v - tdh), rd=rd) * np.heaviside((td_v - tdh), 1),1 )
    # the last column is the full sum, which is needed as a result
    return dpd[:,-1]

def p_superposition_atma(t_hr, t_hist_hr, q_hist_sm3day,
                         k_mD=10, h_m=10, b_m3m3=1.2, mu_cP=1, pi_atma=250, phi=0.2, 
                         ct_1atm=1e-05, rw_m=0.1):
    """
    pressure  estimation for arbitrary flow rate sequence
    t_hr - time after startup in hours
    t_hist_hr - array of well operation mode change times
    q_hist_sm3day - array of flow rates determined after the change of operation mode
    k_mD=10 - permeability, mD 
    h_m=10 - reservoir thickness, m 
    b_m3m3=1.2 - volume coefficient, m3/m3, 
    mu_cP=1 - oil viscosity, cP, 
    pi_atma=250 - initial pressure, atm, 
    phi=0.2 - porosity, fractions of units, 
    ct_1atm=1e-05 - total compressibility, 1/atm, 
    rw_m=0.1 - well radius
    """
    q_ref=1.
    return p_from_pd_atma(pd_superposition(td_from_t(t_hr, k_mD=k_mD, phi=phi, mu_cP=mu_cP, 
                                                     ct_1atm=ct_1atm, rw_m=rw_m),
                                           td_from_t(t_hist_hr, k_mD=k_mD, phi=phi, mu_cP=mu_cP, 
                                                     ct_1atm=ct_1atm, rw_m=rw_m),
                                           q_hist_sm3day / q_ref), 
                          k_mD=10, h_m=10, q_sm3day=q_ref, b_m3m3=1.2, mu_cP=1, pi_atma=250)



def pd_ei_lin(td, rd=1, dqd_dtd=1):
    """
    Решение линейного стока уравнения фильтрации
    rd - безразмерное расстояние
    td - безразмерное время
    """
    # при расчете убедимся, что td=0 не повлияет на расчет, 
    # даже если td массив и нулевой только один элемент
    td = np.array(td, dtype = float)
    pd =  (1 + rd**2/4/td) * (-expi(-rd**2 / 4 /td)) - np.exp(-rd**2 / 4 /td)
    return dqd_dtd * td * pd / 2

def pd_superposition_lin(td, td_hist, qd_hist, rd=1):
    """
    расчет безразмерного давления для последовательности безразмерных дебитов
    td -  время расчета после запуска, безразмерное
    td_hist - массив времен изменения режимов работы скважин, безразмерное
    qd_hist - массив дебитов установленных после изменения режима работы, безразмерное
    """
    # принудительно добавим нули во входные массивы, чтобы учесть запуск скважины
    qdh = np.hstack([qd_hist])
    tdh = np.hstack([td_hist])
    # построим дебиты виртуальных скважин - разности реальных дебитов при переключении
    delta_qd = np.hstack([np.diff(qdh),0])
    delta_td = np.hstack([np.diff(tdh),1])
    
    dq_dt = delta_qd / delta_td
    dq_dt = np.diff(np.hstack([0, delta_qd / delta_td]))
    
    # референсный безразмерный дебит это 1
    
    # векторная магия - время может быть вектором и переключения дебитов тоже вектор
    # надо организовать сумму по временам, каждая из котороых сумма по переключениям
    # делаем при помощи расчета meshgrid и поиска накопленных сумм
    qd_v, td_v =np.meshgrid(delta_qd, td)
    
    dpd = np.cumsum(pd_ei_lin((td_v - tdh), rd=rd, dqd_dtd=dq_dt) * np.heaviside((td_v - tdh), 1),1 )

    return dpd[:,-1]

def p_superposition_lin_atma(t_hr, t_hist_hr, q_hist_sm3day,
                         k_mD=10, h_m=10, b_m3m3=1.2, mu_cP=1, pi_atma=250, phi=0.2, 
                         ct_1atm=1e-05, rw_m=0.1):
    """
    расчет давления для запуска и последующей остановки скважины
    t_hr - время после запуска в часах
    t_hist_hr - массив времен изменения режимов работы скважин
    q_hist_sm3day - массив дебитов установленных после изменения режима работы
    k_mD=10 - проницаемость, мД, 
    h_m=10 - мощность пласта, м, 
    b_m3m3=1.2 - объемный коэффициент, м3/м3, 
    mu_cP=1 - вязкость нефти, сП, 
    pi_atma=250 - начальное давление, атм, 
    phi=0.2 - пористость, доли единиц, 
    ct_1atm=1e-05 - общая сжимаемость, 1/атм, 
    rw_m=0.1 - радиус скважины
    """
    q_ref=1.
    return p_from_pd_atma(pd_superposition_lin(td_from_t(t_hr, k_mD=k_mD, phi=phi, mu_cP=mu_cP, 
                                                     ct_1atm=ct_1atm, rw_m=rw_m),
                                               td_from_t(t_hist_hr, k_mD=k_mD, phi=phi, mu_cP=mu_cP, 
                                                     ct_1atm=ct_1atm, rw_m=rw_m),
                                               q_hist_sm3day / q_ref), 
                          k_mD=10, h_m=10, q_sm3day=q_ref, b_m3m3=1.2, mu_cP=1, pi_atma=250)

def p_ss_atma(p_res_atma = 250,
              q_liq_sm3day = 50,
              mu_cP = 1,
              B_m3m3 = 1.2,
              k_mD = 40,
              h_m = 10,
              r_e = 240,
              r = 0.1):
    """
    function for calculating the pressure at an arbitrary point in the reservoir for the steady-state solution 
    p_res_atma   - reservoir pressure, supply pressure
    q_liq_sm3day - fluid flow rate at the surface under standard conditions
    mu_cP        - oil viscosity (in situ conditions)
    B_m3m3       - oil formation volume factor (FVF)
    k_mD         - formation permeability
    h_m          - formation thickness
    r_e          - external reservoir radius 
    r            - distance at which the calculation is made
    """

    return p_res_atma - 18.41 * q_liq_sm3day*mu_cP*B_m3m3/k_mD/h_m * np.log(r_e/r)