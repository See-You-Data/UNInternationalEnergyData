import pandas as pd
import countries as c

def generate_df():
    for i in range(1,13):
        if i == 1:
            df = pd.read_csv('raw_data/all_energy_statistics' + str(i) +'.csv')
            df_cols = df.columns.to_list()
        else:
            df1 = pd.read_csv('raw_data/all_energy_statistics' + str(i) + '.csv',header=None)
            df1.columns = df_cols
            df = df.append(df1)



    return df