import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

with open('all_original.pickle', 'rb') as f:
        data = np.load(f,allow_pickle=True)
