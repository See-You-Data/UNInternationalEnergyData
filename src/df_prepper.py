import pandas as pd
import numpy as np
import os

def csv_combiner(df,verbose=False):
	'''
	Our data is currently sourced from 12 .csv files (Eurostat's Standard Data and Metadata Exchange API infrastructure is very opaque)
	This function combines these into one pandas dataframe

	Parameters
	----------
	df : pandas dataframe
		The first .csv file of the 10 to be combined
	verbose : boolean
		If True, print extra information for debugging
 	
 	Returns
 	-------
 	df : pandas dataframe
 		 The combined .csv files as a dataframe, replacing the input
	'''
	column_names = df.columns.to_list()
	file_number = 2

	for i in np.arange(11):
	    if verbose == True: print(f'About to load file number {file_number}')
	    df_ = pd.read_csv(f'raw_data/all_energy_statistics{file_number}.csv',header=None) # header=None ensures the column names are set to numbers i.e. not the first row
	    df_.columns = column_names
	    df = df.append(df_)
	    file_number+=1 # used for selecting correct file name in each iteration

	assert df.shape[0] == 1189482, 'Dataframes don\'t match!' # https://www.kaggle.com/alexanderklarge/checking-out-data-set-for-seeyoudata-project
	return(df)

def df_groupby_flatten(df_groupby):
	'''
	A Pandas groupby object often needs flattening for easier analysis
	'''
	df_groupby = df_groupby.unstack()
	df_groupby.columns = df_groupby.columns.droplevel()
	df_groupby.reset_index(inplace=True)
	df_groupby.set_index(df_groupby.columns[1],inplace=True)
	return(df_groupby)

def df_groupby_then_flatten(df,cols_to_keep,cols_to_groupby,aggregate='sum'):
	'''
	Perform a groupby on the raw dataframe, then flatten with df_groupby_flatten()

	Parameters
	----------
	df : pandas dataframe
		The dataframe returned by csv_combiner()
	cols_to_keep : list of strings
		List of df columns to keep from the original df
	cols_to_groupby : list of strings
		List of df columns to use as groupby index
	aggregate : string
		String of desired aggregate i.e. mean, sum
 	
 	Returns
 	-------
 	df_groupby : pandas dataframe object
	'''
	if aggregate == 'sum':
		df_groupby = df[cols_to_keep].groupby(cols_to_groupby).sum()
	elif aggregate == 'mean':
		df_groupby = df[cols_to_keep].groupby(cols_to_groupby).mean()
	else:
		pass
    
    # Runs another function
	df_groupby = df_groupby_flatten(df_groupby)
        
	return(df_groupby)

