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


def pd_superposition(td, td_hist, qd_hist):
    """
    расчет безразмерного давления для последовательности безразмерных дебитов
    td -  время расчета после запуска, безразмерное
    td_hist - массив времен изменения режимов работы скважин, безразмерное
    qd_hist - массив дебитов установленных после изменения режима работы, безразмерное
    """
    # принудительно добавим нули во входные массивы, чтобы учесть запуск скважины
    qdh = np.hstack([0, qd_hist])
    tdh = np.hstack([0, td_hist])
    # построим дебиты виртуальных скважин - разности реальных дебитов при переключении
    delta_qd = np.hstack([0, np.diff(qdh)])
    # референсный безразмерный дебит это 1
    
    # векторная магия - время может быть вектором и переключения дебитов тоже вектор
    # надо организовать сумму по временам, каждая из котороых сумма по переключениям
    # делаем при помощи расчета meshgrid и поиска накопленных сумм
    qd_v, td_v =np.meshgrid(delta_qd, td)
    # используем куммулятивную сумму numpy для того что суммировать результаты
    dpd = np.cumsum(qd_v * pd_ei((td_v - tdh)) * np.heaviside((td_v - tdh), 1),1 )
    # последний столбец - полная сумма, которая нужна в качестве результата
    return dpd[:,-1]


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