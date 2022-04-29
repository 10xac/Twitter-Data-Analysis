import numpy as np
import pandas as pd


class DataLoader:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_csv(self):
        df = pd.read_csv(self.file_name)
        return df
