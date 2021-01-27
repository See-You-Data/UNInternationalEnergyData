import pandas as pd
import numpy as np

def create_even_groups(df,col,n):
	'''
	Take a value counts dataframe, and create a new column assigning each row a group based on the value count
	For example, with a value counts dataframe showing the number of datapoints per country, create a new column assigning each country to a group
	I.e., Germany and the UK are in the top {}% of countries by value count and thus are assigned group {} 

	Parameters
	----------
	df : pandas dataframe
		A value counts dataframe
	col : string
		The name of the column of the value counts
	n : int
		The number of groups to split the data by
 	
 	Returns
 	-------
 	df : pandas dataframe
 		 The value counts dataframe with the new column
	'''
	labels=[]

	for i in np.arange(1,n+1):
		labels.append(f'Q{i}')
    
	print(labels)
    
	display(df[col])
    
	df['groups'] = pd.qcut(x=df[col],q=n,labels=labels)
    
	return df