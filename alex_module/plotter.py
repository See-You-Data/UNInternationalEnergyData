from matplotlib import pyplot as plt 
import seaborn as sns
plt.style.use('seaborn')
plt.style.use('seaborn-poster')

def plot_from_flattened(df,x,y,index_as_x=True,verbose=False,title='Title goes here',figsize=[15,10]):
    fig = plt.figure(figsize=figsize)
    ax = plt.axes()
    
    if index_as_x == True:
        ax.plot(df.index,df[y])
        if verbose==True: display(df.index,df[y]) 
    else:
        ax.plot(df[x],df[y])
        if verbose==True: display(df[x],df[y])
    
    plt.legend(y)
    plt.title(title)