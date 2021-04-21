import pandas as pd
import numpy as np
import math

def create_even_groups(df,column,n_groups,verbose=False):
    '''
    Take a value counts dataframe, and create a new column assigning each row a group based on the value count
    For example, with a value counts dataframe showing the number of datapoints per country, create a new column assigning each country to a group
    I.e., Germany and the UK are in the top {}% of countries by value count and thus are assigned group {} 

    Parameters
    ----------
    df : pandas dataframe
        The UN data dataframe. This will be converted into a value_counts dataframe
    column : string
        The name of the df column to perform the value_counts operation on
    n_groups : int
        The number of groups to split the data by
    verbose : boolean
        If True, print extra information for debugging/ sanity checks
 
     Returns
     -------
     df : pandas dataframe
         The value counts dataframe with the new column denoting the group assigned to each row
    '''
    # Convert the dataframe into a value_counts dataframe
    df = df[column].value_counts().to_frame()
    
    # Ensuring the dataframe is sorted from largest to smallest
    df.sort_values(by=column,ascending=False,inplace=True)
    
    # Making labels list for labeling groups: if n_groups = 3 then labels are 'Group 1', 'Group 2' and 'Group 3'
    group_labels=[]
    for i in np.arange(1,n_groups+1): # so it starts at 1 i.e. 1,2,3 rather than 0,1,2 if n_groups = 3
        group_labels.append(f'Group {i}')
    
    # Working out number of rows in each group
    df_length = df.shape[0]
    group_size = round(df_length/n_groups)
    
    # Creating thresholds
    counter=1
    threshold_list=[]
    for i in range(n_groups):
        threshold_list.append(counter*group_size)
        counter+=1

    if verbose:
        print('Auto-generated labels:')
        print(group_labels)
        print(f'\ndf length is {df_length}')
        print(f'Size of each group: {group_size}\n')
        
        # Printing group thresholds
        for index,value in enumerate(threshold_list):
            print(f'{group_labels[index]} threshold = {value}')
            counter+=1
        print('\n')
        
    # Making initial dataframe to append future ones from for loop to
    df1 = df.iloc[:threshold_list[0]].copy()
    df1['Label']=group_labels[0]
    
    # Now iterating through an making further groups    
    #remaining_labels=group_labels[1:].copy()
    
    # Below is hell but it seems to work
    counter=1
    for i in range(counter,n_groups): # as one group is already done
        if verbose: print(f'i: {i}')
        try:
            if verbose:
                print('"Try" of Try/ Except worked...')
                print(f'Threshold lower limit: {threshold_list[counter-1]}')
                print(f'Threshold uppper limit: {threshold_list[counter]}')
            df2=df.iloc[threshold_list[counter-1]:threshold_list[counter]].copy()
        except:
            if verbose:
                print('"Except" of Try/ Except worked...')
                print(f'Threshold lower limit: {threshold_list[counter]}')
            df2=df.iloc[threshold_list[counter]:].copy() # for the final time
            
        df2['Label']=group_labels[counter]
        if verbose: print(f'Label assigned: {group_labels[counter]}')
        
        df1=df1.append(df2)
        counter+=1
        if verbose: print('\n')
    
    # Some quick assert statements (should be moved to unit tests at some point)
    smallest_group = df1['Label'].value_counts().min()
    assert math.isclose(smallest_group,group_size,abs_tol=1)
    assert df1['Label'].value_counts().mode()[0] == group_size
    
    return df1
