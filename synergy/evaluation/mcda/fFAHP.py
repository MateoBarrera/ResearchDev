# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 09:41:50 2021

Funciones del proceso FAHP

@author: FZ Hogar
"""
import numpy as np


# Defuzzicación para convertir los números triangulares en números reales.
def defuzzicacion(mC):
    mCd = np.zeros((mC.shape[0], mC.shape[1]))
    for i in range(mCd.shape[0]):
        for j in range(mCd.shape[1]):
            mCd[i, j] = (mC[i, j, 0] + 4 * mC[i, j, 1] + mC[i, j, 2]) / 6

    return mCd


# Vector de prioridad a partir de la matriz defuzzificada
def cPesos(mC):
    sFl = np.sum(mC, 0)  # Suma de las filas de la matriz
    mCn = mC / sFl  # Matriz normalizada
    wj = np.mean(mCn, 1)  # Pesos a partir del promedio de las columnas

    cj = np.sum(mC * wj, 1)
    dj = cj / wj
    lmax = np.mean(dj)  # Auto-valor máximo de la matriz defuzzificada

    CI, CR = iConsistencia(mC.shape[0], lmax)
    if CR < 0.10:
        print("CI = ", CI)
        print("CR = ", CR)
        print("Wi = ", wj)
        print("______________________________________________________________")
    else:
        print("La matriz no pasó la verificación de consistencia")
        print("\n")
        wj = None
        print("______________________________________________________________")

    return wj


# Verifica el índice y la relación de consistencia
def iConsistencia(n, lmax):
    if n == 2:
        CI = 0
        CR = 0
    else:
        CA = {
            3: 0.5247,
            4: 0.8816,
            5: 1.1086,
            6: 1.2479,
            7: 1.3417,
            8: 1.4057,
            9: 1.4499,
            10: 1.4854,
            11: 1.51,
            12: 1.54,
        }  # Índice de consistencia aleatoria
        CI = (lmax - n) / (n - 1)  # Índice de verificación de consistencia
        CR = CI / CA[n]  # Razón de consistencia

    return CI, CR


# Agregación mediante la media geométrica
def agregacionmg(mIC):
    mA = np.zeros(mIC[0].shape)
    for i in range(mIC[0].shape[0]):
        for j in range(mIC[0].shape[1]):
            ld = np.zeros(len(mIC))
            md = np.zeros(len(mIC))
            ud = np.zeros(len(mIC))
            for k in range(len(mIC)):
                ld[k] = mIC[k][i, j, 0]
                md[k] = mIC[k][i, j, 1]
                ud[k] = mIC[k][i, j, 2]
            mA[i, j, 0] = (np.prod(ld)) ** (1 / len(mIC))
            mA[i, j, 1] = (np.prod(md)) ** (1 / len(mIC))
            mA[i, j, 2] = (np.prod(ud)) ** (1 / len(mIC))

    return mA


# Agrega las matrices individuales en una única matriz
def agregacion(mIC):
    mA = np.zeros(mIC[0].shape)
    for i in range(0, np.size(mIC[0], 0)):
        for j in range(0, np.size(mIC[0], 1)):
            ld = np.zeros(len(mIC))
            md = np.zeros(len(mIC))
            ud = np.zeros(len(mIC))
            for k in range(0, len(mIC)):
                ld[k] = mIC[k][i, j, 0]
                md[k] = mIC[k][i, j, 1]
                ud[k] = mIC[k][i, j, 2]
            mA[i, j, 0] = min(ld)
            mA[i, j, 1] = np.mean(md)
            mA[i, j, 2] = max(ud)

    return mA


# Media geométrica difusa
def mediagd(mA):
    ri = np.ones((np.size(mA, 0), np.size(mA, 2)))
    for i in range(np.size(mA, 0)):
        for j in range(np.size(mA, 1)):
            ri[i, :] = ri[i, :] * mA[i, j]
        ri[i, :] = ri[i, :] ** (1 / np.size(mA, 1))

    return ri


# Pesos difusos
def pesosd(ri):
    wi = np.zeros(ri.shape)
    for i in range(np.size(ri, 0)):
        wi[i, :] = ri[i, :] * (np.sum(ri, 0) ** (-1))

    return wi


# Los pesos difusos se transforman en un número equivalente positivo y se normaliza
def defuzzicacionw(wi):
    Mi = np.sum(wi, 1) / 3
    Ni = Mi / np.sum(Mi)  # Pesos de los criterios
    return Ni
