# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 09:04:05 2021

Script para ponderar las dimensiones y los criterios a partir de las evaluaciones 
difusas en cada escenario de importancia dimensional.

@author: FZ Hogar
"""
import numpy as np
import pandas as pd
import fFAHP as ahp

"""Comparación pareada de las dimensiones___________________________________"""
# Escenario 1: EPI: Técnico = Económico = Ambiental = Social
EPID = np.array(
    [
        [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],  # Técnica
        [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],  # Económica
        [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],  # Ambiental
        [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
    ]
)  # Social

# Escenario 2: ET1: Técnico > Económico = Ambiental = Social
ET1D = np.array(
    [
        [1, 3, 3, 3],  # Técnica
        [1 / 3, 1, 1, 1],  # Económica
        [1 / 3, 1, 1, 1],  # Ambiental
        [1 / 3, 1, 1, 1],
    ]
)  # Social

# Escenario 3: ET2: Técnico > Económico > Ambiental > Social
ET2D = np.array(
    [
        [1, 3, 5, 7],  # Técnica
        [1 / 3, 1, 3, 5],  # Económica
        [1 / 5, 1 / 3, 1, 3],  # Ambiental
        [1 / 7, 1 / 5, 1 / 3, 1],
    ]
)  # Social

# Escenario 4: ET3: Técnico > Económico > Social > Ambiental
ET3D = np.array(
    [
        [1, 3, 7, 5],  # Técnica
        [1 / 3, 1, 5, 3],  # Económica
        [1 / 7, 1 / 5, 1, 1 / 3],  # Ambiental
        [1 / 5, 1 / 3, 3, 1],
    ]
)  # Social

# Escenario 5: ET4: Técnico > Ambiental > Económico > Social
ET4D = np.array(
    [
        [1, 5, 3, 7],  # Técnica
        [1 / 5, 1, 1 / 3, 3],  # Económica
        [1 / 3, 3, 1, 5],  # Ambiental
        [1 / 7, 1 / 3, 1 / 5, 1],
    ]
)  # Social

# Escenario 6: ET5: Técnico > Ambiental > Social > Económico
ET5D = np.array(
    [
        [1, 7, 3, 5],  # Técnica
        [1 / 7, 1, 1 / 5, 1 / 3],  # Económica
        [1 / 3, 5, 1, 3],  # Ambiental
        [1 / 5, 3, 1 / 3, 1],
    ]
)  # Social

# Escenario 7: ET6: Técnico > Social > Económico > Ambiental
ET6D = np.array(
    [
        [1, 5, 7, 3],  # Técnica
        [1 / 5, 1, 3, 1 / 3],  # Económica
        [1 / 7, 1 / 3, 1, 1 / 5],  # Ambiental
        [1 / 3, 3, 5, 1],
    ]
)  # Social

# Escenario 8: ET7: Técnico > Social > Ambiental > Económico
ET7D = np.array(
    [
        [1, 7, 5, 3],  # Técnica
        [1 / 7, 1, 1 / 3, 1 / 5],  # Económica
        [1 / 5, 3, 1, 1 / 3],  # Ambiental
        [1 / 3, 5, 3, 1],
    ]
)  # Social

# Escenario 9: EE1: Económico > Técnico = Ambiental = Social
EE1D = np.array(
    [
        [1, 1 / 3, 1, 1],  # Técnica
        [3, 1, 3, 3],  # Económica
        [1, 1 / 3, 1, 1],  # Ambiental
        [1, 1 / 3, 1, 1],
    ]
)  # Social

# Escenario 10: EE2: Económico > Técnico > Ambiental > Social
EE2D = np.array(
    [
        [1, 1 / 3, 3, 5],  # Técnica
        [3, 1, 5, 7],  # Económica
        [1 / 3, 1 / 5, 1, 3],  # Ambiental
        [1 / 5, 1 / 7, 1 / 3, 1],
    ]
)  # Social

# Escenario 11: EE3: Económico > Técnico > Social > Ambiental
EE3D = np.array(
    [
        [1, 1 / 3, 5, 3],  # Técnica
        [3, 1, 7, 5],  # Económica
        [1 / 5, 1 / 7, 1, 1 / 3],  # Ambiental
        [1 / 3, 1 / 5, 3, 1],
    ]
)  # Social

# Escenario 12: EE4: Económico > Ambiental > Técnico > Social
EE4D = np.array(
    [
        [1, 1 / 5, 1 / 3, 3],  # Técnica
        [5, 1, 3, 7],  # Económica
        [3, 1 / 3, 1, 5],  # Ambiental
        [1 / 3, 1 / 7, 1 / 5, 1],
    ]
)  # Social

# Escenario 13: EE5: Económico > Ambiental > Social > Técnico
EE5D = np.array(
    [
        [1, 1 / 7, 1 / 5, 1 / 3],  # Técnica
        [7, 1, 3, 5],  # Económica
        [5, 1 / 3, 1, 3],  # Ambiental
        [3, 1 / 5, 1 / 3, 1],
    ]
)  # Social

# Escenario 14: EE6: Económico > Social > Técnico > Ambiental
EE6D = np.array(
    [
        [1, 1 / 5, 3, 1 / 3],  # Técnica
        [5, 1, 7, 3],  # Económica
        [1 / 3, 1 / 7, 1, 1 / 5],  # Ambiental
        [3, 1 / 3, 5, 1],
    ]
)  # Social

# Escenario 15: EE7: Económico > Social > Ambiental > Técnico
EE7D = np.array(
    [
        [1, 1 / 7, 1 / 3, 1 / 5],  # Técnica
        [7, 1, 5, 3],  # Económica
        [3, 1 / 5, 1, 1 / 3],  # Ambiental
        [5, 1 / 3, 3, 1],
    ]
)  # Social

# Escenario 16: EA1: Ambiental > Técnico = Económico = Social
EA1D = np.array(
    [
        [1, 1, 1 / 3, 1],  # Técnica
        [1, 1, 1 / 3, 1],  # Económica
        [3, 3, 1, 3],  # Ambiental
        [1, 1, 1 / 3, 1],
    ]
)  # Social

# Escenario 17: EA2: Ambiental > Técnico > Económico > Social
EA2D = np.array(
    [
        [1, 3, 1 / 3, 5],  # Técnica
        [1 / 3, 1, 1 / 5, 3],  # Económica
        [3, 5, 1, 7],  # Ambiental
        [1 / 5, 1 / 3, 1 / 7, 1],
    ]
)  # Social

# Escenario 18: EA3: Ambiental > Técnico > Social > Económico
EA3D = np.array(
    [
        [1, 5, 1 / 3, 3],  # Técnica
        [1 / 5, 1, 1 / 7, 1 / 3],  # Económica
        [3, 7, 1, 5],  # Ambiental
        [1 / 3, 3, 1 / 5, 1],
    ]
)  # Social

# Escenario 19: EA4: Ambiental > Económico > Técnico > Social
EA4D = np.array(
    [
        [1, 1 / 3, 1 / 5, 3],  # Técnica
        [3, 1, 1 / 3, 5],  # Económica
        [5, 3, 1, 7],  # Ambiental
        [1 / 3, 1 / 5, 1 / 7, 1],
    ]
)  # Social

# Escenario 20: EA5: Ambiental > Económico > Social > Técnico
EA5D = np.array(
    [
        [1, 1 / 5, 1 / 7, 1 / 3],  # Técnica
        [5, 1, 1 / 3, 3],  # Económica
        [7, 3, 1, 5],  # Ambiental
        [3, 1 / 3, 1 / 5, 1],
    ]
)  # Social

# Escenario 21: EA6: Ambiental > Social > Técnico > Económico
EA6D = np.array(
    [
        [1, 3, 1 / 5, 1 / 3],  # Técnica
        [1 / 3, 1, 1 / 7, 1 / 5],  # Económica
        [5, 7, 1, 3],  # Ambiental
        [3, 5, 1 / 3, 1],
    ]
)  # Social

# Escenario 22: EA7: Ambiental > Social > Económico > Técnico
EA7D = np.array(
    [
        [1, 1 / 3, 1 / 7, 1 / 5],  # Técnica
        [3, 1, 1 / 5, 1 / 3],  # Económica
        [7, 5, 1, 3],  # Ambiental
        [5, 3, 1 / 3, 1],
    ]
)  # Social

# Escenario 23: ES1: Social > Técnico = Económico = Ambiental
ES1D = np.array(
    [
        [1, 1, 1, 1 / 3],  # Técnica
        [1, 1, 1, 1 / 3],  # Económica
        [1, 1, 1, 1 / 3],  # Ambiental
        [3, 3, 3, 1],
    ]
)  # Social

# Escenario 24: ES2: Social > Técnico > Económico > Ambiental
ES2D = np.array(
    [
        [1, 3, 5, 1 / 3],  # Técnica
        [1 / 3, 1, 3, 1 / 5],  # Económica
        [1 / 5, 1 / 3, 1, 1 / 7],  # Ambiental
        [3, 5, 7, 1],
    ]
)  # Social

# Escenario 25: ES3: Social > Técnico > Ambiental > Económico
ES3D = np.array(
    [
        [1, 5, 3, 1 / 3],  # Técnica
        [1 / 5, 1, 1 / 3, 1 / 7],  # Económica
        [1 / 3, 3, 1, 1 / 5],  # Ambiental
        [3, 7, 5, 1],
    ]
)  # Social

# Escenario 26: ES4: Social > Económico > Técnico > Ambiental
ES4D = np.array(
    [
        [1, 1 / 3, 3, 1 / 5],  # Técnica
        [3, 1, 5, 1 / 3],  # Económica
        [1 / 3, 1 / 5, 1, 1 / 7],  # Ambiental
        [5, 3, 7, 1],
    ]
)  # Social

# Escenario 27: ES5: Social > Económico > Ambiental > Técnico
ES5D = np.array(
    [
        [1, 1 / 5, 1 / 3, 1 / 7],  # Técnica
        [5, 1, 3, 1 / 3],  # Económica
        [3, 1 / 3, 1, 1 / 5],  # Ambiental
        [7, 3, 5, 1],
    ]
)  # Social

# Escenario 28: ES6: Social > Ambiental > Técnico > Económico
ES6D = np.array(
    [
        [1, 3, 1 / 3, 1 / 5],  # Técnica
        [1 / 3, 1, 1 / 5, 1 / 7],  # Económica
        [3, 5, 1, 1 / 3],  # Ambiental
        [5, 7, 3, 1],
    ]
)  # Social

# Escenario 29: ES7: Social > Ambiental > Económico > Técnico
ES7D = np.array(
    [
        [1, 1 / 3, 1 / 5, 1 / 7],  # Técnica
        [3, 1, 1 / 3, 1 / 5],  # Económica
        [5, 3, 1, 1 / 3],  # Ambiental
        [7, 5, 3, 1],
    ]
)  # Social

"""Comparación pareada de los criterios ____________________________"""
# Escenario 1: EPI: Técnico = Económico = Ambiental = Social
EPIC = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # (Tec):Penetración de fuentes renovables
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # (Tec):Excedente de energía
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # (Eco):Costo de capital
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # (Eco):Costos de O&M
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # (Eco):Costo nivelado LCOE
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # (Amb):Emisiones de CO2
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # (Amb):Área de terreno
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # (Soc):Aceptabilidad Social
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 2: ET1: Técnico > Económico = Ambiental = Social
ET1C = np.array(
    [
        [1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3],  # (Tec):Penetración de fuentes renovables
        [1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3],  # (Tec):Excedente de energía
        [1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
        ],  # (Eco):Costo de capital
        [1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1, 1, 1, 1],  # (Eco):Costos de O&M
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
        ],  # (Eco):Costo nivelado LCOE
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
        ],  # (Amb):Área de terreno
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1, 1, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 3: ET2: Técnico > Económico > Ambiental > Social
ET2C = np.array(
    [
        [1, 1, 1, 1, 1, 3, 3, 3, 5, 5, 7, 7],  # (Tec):Penetración de fuentes renovables
        [1, 1, 1, 1, 1, 3, 3, 3, 5, 5, 7, 7],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 3, 3, 3, 5, 5, 7, 7],  # (Tec):Excedente de energía
        [1, 1, 1, 1, 1, 3, 3, 3, 5, 5, 7, 7],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            5,
            5,
            7,
            7,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            3,
            3,
            5,
            5,
        ],  # (Eco):Costo de capital
        [1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 3, 3, 5, 5],  # (Eco):Costos de O&M
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            3,
            3,
            5,
            5,
        ],  # (Eco):Costo nivelado LCOE
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            3,
            3,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            3,
            3,
        ],  # (Amb):Área de terreno
        [
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 5, 1 / 5, 1 / 5, 1 / 3, 1 / 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 4: ET3: Técnico > Económico > Social > Ambiental
ET3C = np.array(
    [
        [1, 1, 1, 1, 1, 3, 3, 3, 7, 7, 5, 5],  # (Tec):Penetración de fuentes renovables
        [1, 1, 1, 1, 1, 3, 3, 3, 7, 7, 5, 5],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 3, 3, 3, 7, 7, 5, 5],  # (Tec):Excedente de energía
        [1, 1, 1, 1, 1, 3, 3, 3, 7, 7, 5, 5],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            7,
            7,
            5,
            5,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            5,
            5,
            3,
            3,
        ],  # (Eco):Costo de capital
        [1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 5, 5, 3, 3],  # (Eco):Costos de O&M
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            5,
            5,
            3,
            3,
        ],  # (Eco):Costo nivelado LCOE
        [
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1 / 3,
            1 / 3,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1 / 3,
            1 / 3,
        ],  # (Amb):Área de terreno
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 3, 1 / 3, 1 / 3, 3, 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 5: ET4: Técnico > Ambiental > Económico > Social
ET4C = np.array(
    [
        [1, 1, 1, 1, 1, 5, 5, 5, 3, 3, 7, 7],  # (Tec):Penetración de fuentes renovables
        [1, 1, 1, 1, 1, 5, 5, 5, 3, 3, 7, 7],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 5, 5, 5, 3, 3, 7, 7],  # (Tec):Excedente de energía
        [1, 1, 1, 1, 1, 5, 5, 5, 3, 3, 7, 7],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            5,
            5,
            5,
            3,
            3,
            7,
            7,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            3,
            3,
        ],  # (Eco):Costo de capital
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            3,
            3,
        ],  # (Eco):Costos de O&M
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            3,
            3,
        ],  # (Eco):Costo nivelado LCOE
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            3,
            1,
            1,
            5,
            5,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            3,
            1,
            1,
            5,
            5,
        ],  # (Amb):Área de terreno
        [
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 3, 1 / 3, 1 / 3, 1 / 5, 1 / 5, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 6: ET5: Técnico > Ambiental > Social > Económico
ET5C = np.array(
    [
        [1, 1, 1, 1, 1, 7, 7, 7, 3, 3, 5, 5],  # (Tec):Penetración de fuentes renovables
        [1, 1, 1, 1, 1, 7, 7, 7, 3, 3, 5, 5],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 7, 7, 7, 3, 3, 5, 5],  # (Tec):Excedente de energía
        [1, 1, 1, 1, 1, 7, 7, 7, 3, 3, 5, 5],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            7,
            7,
            7,
            3,
            3,
            5,
            5,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Eco):Costo de capital
        [
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Eco):Costos de O&M
        [
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Eco):Costo nivelado LCOE
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            5,
            5,
            5,
            1,
            1,
            3,
            3,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            5,
            5,
            5,
            1,
            1,
            3,
            3,
        ],  # (Amb):Área de terreno
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5, 3, 3, 3, 1 / 3, 1 / 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 7: ET6: Técnico > Social > Económico > Ambiental
ET6C = np.array(
    [
        [1, 1, 1, 1, 1, 5, 5, 5, 7, 7, 3, 3],  # (Tec):Penetración de fuentes renovables
        [1, 1, 1, 1, 1, 5, 5, 5, 7, 7, 3, 3],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 5, 5, 5, 7, 7, 3, 3],  # (Tec):Excedente de energía
        [1, 1, 1, 1, 1, 5, 5, 5, 7, 7, 3, 3],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            5,
            5,
            5,
            7,
            7,
            3,
            3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1,
            3,
            3,
            1 / 3,
            1 / 3,
        ],  # (Eco):Costo de capital
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1,
            3,
            3,
            1 / 3,
            1 / 3,
        ],  # (Eco):Costos de O&M
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1,
            3,
            3,
            1 / 3,
            1 / 3,
        ],  # (Eco):Costo nivelado LCOE
        [
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1 / 5,
            1 / 5,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1 / 5,
            1 / 5,
        ],  # (Amb):Área de terreno
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            3,
            5,
            5,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 3, 3, 3, 5, 5, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 8: ET7: Técnico > Social > Ambiental > Económico
ET7C = np.array(
    [
        [1, 1, 1, 1, 1, 7, 7, 7, 5, 5, 3, 3],  # (Tec):Penetración de fuentes renovables
        [1, 1, 1, 1, 1, 7, 7, 7, 5, 5, 3, 3],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 7, 7, 7, 5, 5, 3, 3],  # (Tec):Excedente de energía
        [1, 1, 1, 1, 1, 7, 7, 7, 5, 5, 3, 3],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            7,
            7,
            7,
            5,
            5,
            3,
            3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Eco):Costo de capital
        [
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Eco):Costos de O&M
        [
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 7,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Eco):Costo nivelado LCOE
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            3,
            3,
            3,
            1,
            1,
            1 / 3,
            1 / 3,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            3,
            3,
            3,
            1,
            1,
            1 / 3,
            1 / 3,
        ],  # (Amb):Área de terreno
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            5,
            5,
            5,
            3,
            3,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 5, 5, 5, 3, 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 9: EE1: Económico > Técnico = Ambiental = Social
EE1C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1,
        ],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3],  # (Eco):Costo de capital
        [3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3],  # (Eco):Costos de O&M
        [3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3],  # (Eco):Costo nivelado LCOE
        [1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1],  # (Amb):Emisiones de CO2
        [1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1],  # (Amb):Área de terreno
        [1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1],  # (Soc):Aceptabilidad Social
        [1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 10: EE2: Económico > Técnico > Ambiental > Social
EE2C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            5,
            5,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            5,
            5,
        ],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1 / 3, 3, 3, 5, 5],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            5,
            5,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            5,
            5,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [3, 3, 3, 3, 3, 1, 1, 1, 5, 5, 7, 7],  # (Eco):Costo de capital
        [3, 3, 3, 3, 3, 1, 1, 1, 5, 5, 7, 7],  # (Eco):Costos de O&M
        [3, 3, 3, 3, 3, 1, 1, 1, 5, 5, 7, 7],  # (Eco):Costo nivelado LCOE
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            3,
            3,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            3,
            3,
        ],  # (Amb):Área de terreno
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 7, 1 / 7, 1 / 7, 1 / 3, 1 / 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 11: EE3: Económico > Técnico > Social > Ambiental
EE3C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            5,
            5,
            3,
            3,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            5,
            5,
            3,
            3,
        ],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1 / 3, 5, 5, 3, 3],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            5,
            5,
            3,
            3,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            5,
            5,
            3,
            3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [3, 3, 3, 3, 3, 1, 1, 1, 7, 7, 5, 5],  # (Eco):Costo de capital
        [3, 3, 3, 3, 3, 1, 1, 1, 7, 7, 5, 5],  # (Eco):Costos de O&M
        [3, 3, 3, 3, 3, 1, 1, 1, 7, 7, 5, 5],  # (Eco):Costo nivelado LCOE
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
            1 / 7,
            1,
            1,
            1 / 3,
            1 / 3,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
            1 / 7,
            1,
            1,
            1 / 3,
            1 / 3,
        ],  # (Amb):Área de terreno
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1 / 5,
            3,
            3,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 5, 1 / 5, 1 / 5, 3, 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 12: EE4: Económico > Ambiental > Técnico > Social
EE4C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            3,
            3,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            3,
            3,
        ],  # (Tec):Cuota de generación renovable
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            3,
            3,
        ],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            3,
            3,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            3,
            3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [5, 5, 5, 5, 5, 1, 1, 1, 3, 3, 7, 7],  # (Eco):Costo de capital
        [5, 5, 5, 5, 5, 1, 1, 1, 3, 3, 7, 7],  # (Eco):Costos de O&M
        [5, 5, 5, 5, 5, 1, 1, 1, 3, 3, 7, 7],  # (Eco):Costo nivelado LCOE
        [3, 3, 3, 3, 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 5, 5],  # (Amb):Emisiones de CO2
        [3, 3, 3, 3, 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 5, 5],  # (Amb):Área de terreno
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 7, 1 / 7, 1 / 7, 1 / 5, 1 / 5, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 13: EE5: Económico > Ambiental > Social > Técnico
EE5C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Cuota de generación renovable
        [
            1,
            1,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [7, 7, 7, 7, 7, 1, 1, 1, 3, 3, 5, 5],  # (Eco):Costo de capital
        [7, 7, 7, 7, 7, 1, 1, 1, 3, 3, 5, 5],  # (Eco):Costos de O&M
        [7, 7, 7, 7, 7, 1, 1, 1, 3, 3, 5, 5],  # (Eco):Costo nivelado LCOE
        [5, 5, 5, 5, 5, 1 / 3, 1 / 3, 1 / 3, 1, 1, 3, 3],  # (Amb):Emisiones de CO2
        [5, 5, 5, 5, 5, 1 / 3, 1 / 3, 1 / 3, 1, 1, 3, 3],  # (Amb):Área de terreno
        [
            3,
            3,
            3,
            3,
            3,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [3, 3, 3, 3, 3, 1 / 5, 1 / 5, 1 / 5, 1 / 3, 1 / 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 14: EE6: Económico > Social > Técnico > Ambiental
EE6C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            3,
            3,
            1 / 3,
            1 / 3,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            3,
            3,
            1 / 3,
            1 / 3,
        ],  # (Tec):Cuota de generación renovable
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            3,
            3,
            1 / 3,
            1 / 3,
        ],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            3,
            3,
            1 / 3,
            1 / 3,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            3,
            3,
            1 / 3,
            1 / 3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [5, 5, 5, 5, 5, 1, 1, 1, 7, 7, 3, 3],  # (Eco):Costo de capital
        [5, 5, 5, 5, 5, 1, 1, 1, 7, 7, 3, 3],  # (Eco):Costos de O&M
        [5, 5, 5, 5, 5, 1, 1, 1, 7, 7, 3, 3],  # (Eco):Costo nivelado LCOE
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
            1 / 7,
            1,
            1,
            1 / 5,
            1 / 5,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
            1 / 7,
            1,
            1,
            1 / 5,
            1 / 5,
        ],  # (Amb):Área de terreno
        [3, 3, 3, 3, 3, 1 / 3, 1 / 3, 1 / 3, 5, 5, 1, 1],  # (Soc):Aceptabilidad Social
        [3, 3, 3, 3, 3, 1 / 3, 1 / 3, 1 / 3, 5, 5, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 15: EE7: Económico > Social > Ambiental > Técnico
EE7C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Cuota de generación renovable
        [
            1,
            1,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [7, 7, 7, 7, 7, 1, 1, 1, 5, 5, 3, 3],  # (Eco):Costo de capital
        [7, 7, 7, 7, 7, 1, 1, 1, 5, 5, 3, 3],  # (Eco):Costos de O&M
        [7, 7, 7, 7, 7, 1, 1, 1, 5, 5, 3, 3],  # (Eco):Costo nivelado LCOE
        [
            3,
            3,
            3,
            3,
            3,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1 / 3,
            1 / 3,
        ],  # (Amb):Emisiones de CO2
        [
            3,
            3,
            3,
            3,
            3,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1 / 3,
            1 / 3,
        ],  # (Amb):Área de terreno
        [5, 5, 5, 5, 5, 1 / 3, 1 / 3, 1 / 3, 3, 3, 1, 1],  # (Soc):Aceptabilidad Social
        [5, 5, 5, 5, 5, 1 / 3, 1 / 3, 1 / 3, 3, 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 16: EA1: Ambiental > Técnico = Económico = Social
EA1C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1,
            1,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1,
            1,
        ],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1, 1],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1,
            1,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1,
            1,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1, 1],  # (Eco):Costo de capital
        [1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1, 1],  # (Eco):Costos de O&M
        [1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1, 1],  # (Eco):Costo nivelado LCOE
        [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3],  # (Amb):Emisiones de CO2
        [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3],  # (Amb):Área de terreno
        [1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1, 1],  # (Soc):Aceptabilidad Social
        [1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 17: EA2: Ambiental > Técnico > Económico > Social
EA2C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            5,
            5,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            5,
            5,
        ],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 3, 3, 3, 1 / 3, 1 / 3, 5, 5],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            5,
            5,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            5,
            5,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            3,
            3,
        ],  # (Eco):Costo de capital
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            3,
            3,
        ],  # (Eco):Costos de O&M
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            3,
            3,
        ],  # (Eco):Costo nivelado LCOE
        [3, 3, 3, 3, 3, 5, 5, 5, 1, 1, 7, 7],  # (Amb):Emisiones de CO2
        [3, 3, 3, 3, 3, 5, 5, 5, 1, 1, 7, 7],  # (Amb):Área de terreno
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 3, 1 / 3, 1 / 3, 1 / 7, 1 / 7, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 18: EA3: Ambiental > Técnico > Social > Económico
EA3C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            5,
            5,
            5,
            1 / 3,
            1 / 3,
            3,
            3,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            5,
            5,
            5,
            1 / 3,
            1 / 3,
            3,
            3,
        ],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 5, 5, 5, 1 / 3, 1 / 3, 3, 3],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            5,
            5,
            5,
            1 / 3,
            1 / 3,
            3,
            3,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            5,
            5,
            5,
            1 / 3,
            1 / 3,
            3,
            3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
        ],  # (Eco):Costo de capital
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
        ],  # (Eco):Costos de O&M
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
        ],  # (Eco):Costo nivelado LCOE
        [3, 3, 3, 3, 3, 7, 7, 7, 1, 1, 5, 5],  # (Amb):Emisiones de CO2
        [3, 3, 3, 3, 3, 7, 7, 7, 1, 1, 5, 5],  # (Amb):Área de terreno
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            3,
            1 / 5,
            1 / 5,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 3, 3, 3, 1 / 5, 1 / 5, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 19: EA4: Ambiental > Económico > Técnico > Social
EA4C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            3,
            3,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            3,
            3,
        ],  # (Tec):Cuota de generación renovable
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            3,
            3,
        ],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            3,
            3,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            3,
            3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [3, 3, 3, 3, 3, 1, 1, 1, 1 / 3, 1 / 3, 5, 5],  # (Eco):Costo de capital
        [3, 3, 3, 3, 3, 1, 1, 1, 1 / 3, 1 / 3, 5, 5],  # (Eco):Costos de O&M
        [3, 3, 3, 3, 3, 1, 1, 1, 1 / 3, 1 / 3, 5, 5],  # (Eco):Costo nivelado LCOE
        [5, 5, 5, 5, 5, 3, 3, 3, 1, 1, 7, 7],  # (Amb):Emisiones de CO2
        [5, 5, 5, 5, 5, 3, 3, 3, 1, 1, 7, 7],  # (Amb):Área de terreno
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 5, 1 / 5, 1 / 5, 1 / 7, 1 / 7, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 20: EA5: Ambiental > Económico > Social > Técnico
EA5C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
        ],  # (Tec):Cuota de generación renovable
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
        ],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
            1 / 3,
            1 / 3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [5, 5, 5, 5, 5, 1, 1, 1, 1 / 3, 1 / 3, 3, 3],  # (Eco):Costo de capital
        [5, 5, 5, 5, 5, 1, 1, 1, 1 / 3, 1 / 3, 3, 3],  # (Eco):Costos de O&M
        [5, 5, 5, 5, 5, 1, 1, 1, 1 / 3, 1 / 3, 3, 3],  # (Eco):Costo nivelado LCOE
        [7, 7, 7, 7, 7, 3, 3, 3, 1, 1, 5, 5],  # (Amb):Emisiones de CO2
        [7, 7, 7, 7, 7, 3, 3, 3, 1, 1, 5, 5],  # (Amb):Área de terreno
        [
            3,
            3,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1,
            1,
        ],  # (Soc):Aceptabilidad Social
        [3, 3, 3, 3, 3, 1 / 3, 1 / 3, 1 / 3, 1 / 5, 1 / 5, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 21: EA6: Ambiental > Social > Técnico > Económico
EA6C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Cuota de generación renovable
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
        ],  # (Eco):Costo de capital
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
        ],  # (Eco):Costos de O&M
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
        ],  # (Eco):Costo nivelado LCOE
        [5, 5, 5, 5, 5, 7, 7, 7, 1, 1, 3, 3],  # (Amb):Emisiones de CO2
        [5, 5, 5, 5, 5, 7, 7, 7, 1, 1, 3, 3],  # (Amb):Área de terreno
        [3, 3, 3, 3, 3, 5, 5, 5, 1 / 3, 1 / 3, 1, 1],  # (Soc):Aceptabilidad Social
        [3, 3, 3, 3, 3, 5, 5, 5, 1 / 3, 1 / 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 22: EA7: Ambiental > Social > Económico > Técnico
EA7C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
        ],  # (Tec):Cuota de generación renovable
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
        ],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
            1 / 5,
            1 / 5,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [3, 3, 3, 3, 3, 1, 1, 1, 1 / 5, 1 / 5, 1 / 3, 1 / 3],  # (Eco):Costo de capital
        [3, 3, 3, 3, 3, 1, 1, 1, 1 / 5, 1 / 5, 1 / 3, 1 / 3],  # (Eco):Costos de O&M
        [
            3,
            3,
            3,
            3,
            3,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
        ],  # (Eco):Costo nivelado LCOE
        [7, 7, 7, 7, 7, 5, 5, 5, 1, 1, 3, 3],  # (Amb):Emisiones de CO2
        [7, 7, 7, 7, 7, 5, 5, 5, 1, 1, 3, 3],  # (Amb):Área de terreno
        [5, 5, 5, 5, 5, 3, 3, 3, 1 / 3, 1 / 3, 1, 1],  # (Soc):Aceptabilidad Social
        [5, 5, 5, 5, 5, 3, 3, 3, 1 / 3, 1 / 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 23: ES1: Social > Técnico = Económico = Ambiental
ES1C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
        ],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 3],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 3],  # (Eco):Costo de capital
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 3],  # (Eco):Costos de O&M
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 3],  # (Eco):Costo nivelado LCOE
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 3],  # (Amb):Emisiones de CO2
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 3],  # (Amb):Área de terreno
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1],  # (Soc):Aceptabilidad Social
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 24: ES2: Social > Técnico > Económico > Ambiental
ES2C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            5,
            5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            5,
            5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 3, 3, 3, 5, 5, 1 / 3, 1 / 3],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            5,
            5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            5,
            5,
            1 / 3,
            1 / 3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            3,
            3,
            1 / 5,
            1 / 5,
        ],  # (Eco):Costo de capital
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            3,
            3,
            1 / 5,
            1 / 5,
        ],  # (Eco):Costos de O&M
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            3,
            3,
            1 / 5,
            1 / 5,
        ],  # (Eco):Costo nivelado LCOE
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1 / 7,
            1 / 7,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1 / 7,
            1 / 7,
        ],  # (Amb):Área de terreno
        [3, 3, 3, 3, 3, 5, 5, 5, 7, 7, 1, 1],  # (Soc):Aceptabilidad Social
        [3, 3, 3, 3, 3, 5, 5, 5, 7, 7, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 25: ES3: Social > Técnico > Ambiental > Económico
ES3C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            5,
            5,
            5,
            3,
            3,
            1 / 3,
            1 / 3,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            5,
            5,
            5,
            3,
            3,
            1 / 3,
            1 / 3,
        ],  # (Tec):Cuota de generación renovable
        [1, 1, 1, 1, 1, 5, 5, 5, 3, 3, 1 / 3, 1 / 3],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            5,
            5,
            5,
            3,
            3,
            1 / 3,
            1 / 3,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            5,
            5,
            5,
            3,
            3,
            1 / 3,
            1 / 3,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
        ],  # (Eco):Costo de capital
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
        ],  # (Eco):Costos de O&M
        [
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
        ],  # (Eco):Costo nivelado LCOE
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            3,
            1,
            1,
            1 / 5,
            1 / 5,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            3,
            1,
            1,
            1 / 5,
            1 / 5,
        ],  # (Amb):Área de terreno
        [3, 3, 3, 3, 3, 7, 7, 7, 5, 5, 1, 1],  # (Soc):Aceptabilidad Social
        [3, 3, 3, 3, 3, 7, 7, 7, 5, 5, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 26: ES4: Social > Económico > Técnico > Ambiental
ES4C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Cuota de generación renovable
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            3,
            3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [3, 3, 3, 3, 3, 1, 1, 1, 5, 5, 1 / 3, 1 / 3],  # (Eco):Costo de capital
        [3, 3, 3, 3, 3, 1, 1, 1, 5, 5, 1 / 3, 1 / 3],  # (Eco):Costos de O&M
        [3, 3, 3, 3, 3, 1, 1, 1, 5, 5, 1 / 3, 1 / 3],  # (Eco):Costo nivelado LCOE
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1 / 7,
            1 / 7,
        ],  # (Amb):Emisiones de CO2
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1 / 5,
            1,
            1,
            1 / 7,
            1 / 7,
        ],  # (Amb):Área de terreno
        [5, 5, 5, 5, 5, 3, 3, 3, 7, 7, 1, 1],  # (Soc):Aceptabilidad Social
        [5, 5, 5, 5, 5, 3, 3, 3, 7, 7, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 27: ES5: Social > Económico > Ambiental > Técnico
ES5C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
        ],  # (Tec):Cuota de generación renovable
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
        ],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 5,
            1 / 3,
            1 / 3,
            1 / 7,
            1 / 7,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [5, 5, 5, 5, 5, 1, 1, 1, 3, 3, 1 / 3, 1 / 3],  # (Eco):Costo de capital
        [5, 5, 5, 5, 5, 1, 1, 1, 3, 3, 1 / 3, 1 / 3],  # (Eco):Costos de O&M
        [5, 5, 5, 5, 5, 1, 1, 1, 3, 3, 1 / 3, 1 / 3],  # (Eco):Costo nivelado LCOE
        [
            3,
            3,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1 / 5,
            1 / 5,
        ],  # (Amb):Emisiones de CO2
        [
            3,
            3,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1 / 5,
            1 / 5,
        ],  # (Amb):Área de terreno
        [7, 7, 7, 7, 7, 3, 3, 3, 5, 5, 1, 1],  # (Soc):Aceptabilidad Social
        [7, 7, 7, 7, 7, 3, 3, 3, 5, 5, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 28: ES6: Social > Ambiental > Técnico > Económico
ES6C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Cuota de generación renovable
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
        ],  # (Eco):Costo de capital
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
        ],  # (Eco):Costos de O&M
        [
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 3,
            1,
            1,
            1,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
        ],  # (Eco):Costo nivelado LCOE
        [3, 3, 3, 3, 3, 5, 5, 5, 1, 1, 1 / 3, 1 / 3],  # (Amb):Emisiones de CO2
        [3, 3, 3, 3, 3, 5, 5, 5, 1, 1, 1 / 3, 1 / 3],  # (Amb):Área de terreno
        [5, 5, 5, 5, 5, 7, 7, 7, 3, 3, 1, 1],  # (Soc):Aceptabilidad Social
        [5, 5, 5, 5, 5, 7, 7, 7, 3, 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

# Escenario 29: ES7: Social > Ambiental > Económico > Técnico
ES7C = np.array(
    [
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
        ],  # (Tec):Penetración de fuentes renovables
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
        ],  # (Tec):Cuota de generación renovable
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
        ],  # (Tec):Excedente de energía
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
        ],  # (Tec):Energía esperada no suministrada
        [
            1,
            1,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
            1 / 7,
            1 / 7,
        ],  # (Tec):Probabilidad de pérdida de suministro
        [3, 3, 3, 3, 3, 1, 1, 1, 1 / 3, 1 / 3, 1 / 5, 1 / 5],  # (Eco):Costo de capital
        [3, 3, 3, 3, 3, 1, 1, 1, 1 / 3, 1 / 3, 1 / 5, 1 / 5],  # (Eco):Costos de O&M
        [
            3,
            3,
            3,
            3,
            3,
            1,
            1,
            1,
            1 / 3,
            1 / 3,
            1 / 5,
            1 / 5,
        ],  # (Eco):Costo nivelado LCOE
        [5, 5, 5, 5, 5, 3, 3, 3, 1, 1, 1 / 3, 1 / 3],  # (Amb):Emisiones de CO2
        [5, 5, 5, 5, 5, 3, 3, 3, 1, 1, 1 / 3, 1 / 3],  # (Amb):Área de terreno
        [7, 7, 7, 7, 7, 5, 5, 5, 3, 3, 1, 1],  # (Soc):Aceptabilidad Social
        [7, 7, 7, 7, 7, 5, 5, 5, 3, 3, 1, 1],
    ]
)  # (Soc):Potencial de creación de empleo

"""Cálculo de los pesos de las dimensiones de análisis______________________"""
# Cálculo de los pesos y de la razón de consistencia de las valoraciones en cada escenario:
EPIDd = ahp.defuzzicacion(EPID)

print("Wi de las dimensiones en EPI:")
wiEPI = ahp.cPesos(EPIDd)

print("Wi de las dimensiones en ET1:")
wiET1 = ahp.cPesos(ET1D)

print("Wi de las dimensiones en ET2:")
wiET2 = ahp.cPesos(ET2D)

print("Wi de las dimensiones en ET3:")
wiET3 = ahp.cPesos(ET3D)

print("Wi de las dimensiones en ET4:")
wiET4 = ahp.cPesos(ET4D)

print("Wi de las dimensiones en ET5:")
wiET5 = ahp.cPesos(ET5D)

print("Wi de las dimensiones en ET6:")
wiET6 = ahp.cPesos(ET6D)

print("Wi de las dimensiones en ET7:")
wiET7 = ahp.cPesos(ET7D)

print("Wi de las dimensiones en EE1:")
wiEE1 = ahp.cPesos(EE1D)

print("Wi de las dimensiones en EE2:")
wiEE2 = ahp.cPesos(EE2D)

print("Wi de las dimensiones en EE3:")
wiEE3 = ahp.cPesos(EE3D)

print("Wi de las dimensiones en EE4:")
wiEE4 = ahp.cPesos(EE4D)

print("Wi de las dimensiones en EE5:")
wiEE5 = ahp.cPesos(EE5D)

print("Wi de las dimensiones en EE6:")
wiEE6 = ahp.cPesos(EE6D)

print("Wi de las dimensiones en EE7:")
wiEE7 = ahp.cPesos(EE7D)

print("Wi de las dimensiones en EA1:")
wiEA1 = ahp.cPesos(EA1D)

print("Wi de las dimensiones en EA2:")
wiEA2 = ahp.cPesos(EA2D)

print("Wi de las dimensiones en EA3:")
wiEA3 = ahp.cPesos(EA3D)

print("Wi de las dimensiones en EA4:")
wiEA4 = ahp.cPesos(EA4D)

print("Wi de las dimensiones en EA5:")
wiEA5 = ahp.cPesos(EA5D)

print("Wi de las dimensiones en EA6:")
wiEA6 = ahp.cPesos(EA6D)

print("Wi de las dimensiones en EA7:")
wiEA7 = ahp.cPesos(EA7D)

print("Wi de las dimensiones en ES1:")
wiES1 = ahp.cPesos(ES1D)

print("Wi de las dimensiones en ES2:")
wiES2 = ahp.cPesos(ES2D)

print("Wi de las dimensiones en ES3:")
wiES3 = ahp.cPesos(ES3D)

print("Wi de las dimensiones en ES4:")
wiES4 = ahp.cPesos(ES4D)

print("Wi de las dimensiones en ES5:")
wiES5 = ahp.cPesos(ES5D)

print("Wi de las dimensiones en ES6:")
wiES6 = ahp.cPesos(ES6D)

print("Wi de las dimensiones en ES7:")
wiES7 = ahp.cPesos(ES7D)

"""Cálculo de los pesos de los criterios de evaluación____________________"""
# Cálculo de los pesos y del índice de consistencia de las valoraciones en cada escenario:

print("Wi de los criterios en EPI:")
wiEPIC = ahp.cPesos(EPIC)

print("Wi de los criterios en ET1:")
wiET1C = ahp.cPesos(ET1C)

print("Wi de los criterios en ET2:")
wiET2C = ahp.cPesos(ET2C)

print("Wi de los criterios en ET3:")
wiET3C = ahp.cPesos(ET3C)

print("Wi de los criterios en ET4:")
wiET4C = ahp.cPesos(ET4C)

print("Wi de los criterios en ET5:")
wiET5C = ahp.cPesos(ET5C)

print("Wi de los criterios en ET6:")
wiET6C = ahp.cPesos(ET6C)

print("Wi de los criterios en ET7:")
wiET7C = ahp.cPesos(ET7C)

print("Wi de los criterios en EE1:")
wiEE1C = ahp.cPesos(EE1C)

print("Wi de los criterios en EE2:")
wiEE2C = ahp.cPesos(EE2C)

print("Wi de los criterios en EE3:")
wiEE3C = ahp.cPesos(EE3C)

print("Wi de los criterios en EE4:")
wiEE4C = ahp.cPesos(EE4C)

print("Wi de los criterios en EE5:")
wiEE5C = ahp.cPesos(EE5C)

print("Wi de los criterios en EE6:")
wiEE6C = ahp.cPesos(EE6C)

print("Wi de los criterios en EE7:")
wiEE7C = ahp.cPesos(EE7C)

print("Wi de los criterios en EA1:")
wiEA1C = ahp.cPesos(EA1C)

print("Wi de los criterios en EA2:")
wiEA2C = ahp.cPesos(EA2C)

print("Wi de los criterios en EA3:")
wiEA3C = ahp.cPesos(EA3C)

print("Wi de los criterios en EA4:")
wiEA4C = ahp.cPesos(EA4C)

print("Wi de los criterios en EA5:")
wiEA5C = ahp.cPesos(EA5C)

print("Wi de los criterios en EA6:")
wiEA6C = ahp.cPesos(EA6C)

print("Wi de los criterios en EA7:")
wiEA7C = ahp.cPesos(EA7C)

print("Wi de los criterios en ES1:")
wiES1C = ahp.cPesos(ES1C)

print("Wi de los criterios en ES2:")
wiES2C = ahp.cPesos(ES2C)

print("Wi de los criterios en ES3:")
wiES3C = ahp.cPesos(ES3C)

print("Wi de los criterios en ES4:")
wiES4C = ahp.cPesos(ES4C)

print("Wi de los criterios en ES5:")
wiES5C = ahp.cPesos(ES5C)

print("Wi de los criterios en ES6:")
wiES6C = ahp.cPesos(ES6C)

print("Wi de los criterios en ES7:")
wiES7C = ahp.cPesos(ES7C)

"""Guardar los pesos de los criterios para el análisis en TOPSIS____________"""
wiD = np.array(
    [
        wiEPI,
        wiET1,
        wiET2,
        wiET3,
        wiET4,
        wiET5,
        wiET6,
        wiET7,
        wiEE1,
        wiEE2,
        wiEE3,
        wiEE4,
        wiEE5,
        wiEE6,
        wiEE7,
        wiEA1,
        wiEA2,
        wiEA3,
        wiEA4,
        wiEA5,
        wiEA6,
        wiEA7,
        wiES1,
        wiES2,
        wiES3,
        wiES4,
        wiES5,
        wiES6,
        wiES7,
    ]
)

wiC = np.array(
    [
        wiEPIC,
        wiET1C,
        wiET2C,
        wiET3C,
        wiET4C,
        wiET5C,
        wiET6C,
        wiET7C,
        wiEE1C,
        wiEE2C,
        wiEE3C,
        wiEE4C,
        wiEE5C,
        wiEE6C,
        wiEE7C,
        wiEA1C,
        wiEA2C,
        wiEA3C,
        wiEA4C,
        wiEA5C,
        wiEA6C,
        wiEA7C,
        wiES1C,
        wiES2C,
        wiES3C,
        wiES4C,
        wiES5C,
        wiES6C,
        wiES7C,
    ]
)

pd.DataFrame(wiC).to_excel("weight_criteria.xlsx", index=False)
#pd.DataFrame(wiC).to_csv("pesosC.csv", index=False)
