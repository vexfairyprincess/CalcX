# custom_modules.py
import numpy as np

def cot(x):
    return 1 / np.tan(x)

def sec(x):
    return 1 / np.cos(x)

def csc(x):
    return 1 / np.sin(x)

custom_math = {
    'sin': np.sin,
    'cos': np.cos,
    'tan': np.tan,
    'cot': cot,
    'sec': sec,
    'csc': csc,
    'asin': np.arcsin,
    'acos': np.arccos,
    'atan': np.arctan,
    'sinh': np.sinh,
    'cosh': np.cosh,
    'tanh': np.tanh,
    'log': np.log,
    'log10': np.log10,
    'sqrt': np.sqrt,
    'pi': np.pi,
    'E': np.e,
    'exp': np.exp
}
