import pandas as pd
import random

def Load_Data():
    df1 = pd.read_csv('data/1.csv')
    df2 = pd.read_csv('data/2.csv')
    df3 = pd.read_csv('data/3.csv')
    df4 = pd.read_csv('data/4.csv')
    df5 = pd.read_csv('data/5.csv')
    df6 = pd.read_csv('data/6.csv')
    a = [df1,df2,df3,df4,df5,df6]
    b = [df1.shape[0],df2.shape[0],df3.shape[0],df4.shape[0],df5.shape[0],df6.shape[0]]
    df_sizes = [0,df1.shape[0],df1.shape[0]+df2.shape[0],
                df1.shape[0]+df2.shape[0]+df3.shape[0],
                df1.shape[0]+df2.shape[0]+df3.shape[0]+df4.shape[0],
                df1.shape[0]+df2.shape[0]+df3.shape[0]+df4.shape[0]+df5.shape[0],
                df1.shape[0]+df2.shape[0]+df3.shape[0]+df4.shape[0]+df5.shape[0]+df6.shape[0]]
    Gdata, file_index = [], 0
    for doc_index in range(0,55109):
        if doc_index == df_sizes[file_index+1]:
            file_index += 1
        target_data = a[file_index].loc[doc_index-df_sizes[file_index],'content']
        Gdata.append(target_data)
    return (Gdata)