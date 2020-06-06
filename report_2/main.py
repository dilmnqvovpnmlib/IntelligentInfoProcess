import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston

boston = load_boston()
print(boston.DESCR)