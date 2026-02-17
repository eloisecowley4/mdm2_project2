import matplotlib.pyplot as plt
import pandas as pd



if __name__ == '__main__' :
    data = 'data/2/exp02H20141127_14h13.csv'
    experement = pd.read_csv(data)
    a = experement.iloc[:1000,:]