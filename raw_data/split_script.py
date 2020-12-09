# Source file can be downloaded here - https://www.kaggle.com/unitednations/international-energy-statistics
# The Kaggle user combined multiple UN files into a single CSV with a size of ~120MB
# This exceeds the GitHub limit for file uploads, so I split it into 12 seperate files
# The below code won't work unless you also have the source file downloaded and in the right place - I've uploaded this just for completeness
# (The below code was taken from https://stackoverflow.com/questions/36445193/splitting-one-csv-into-multiple-files-in-python)
csvfile = open('all_energy_statistics.csv', 'r').readlines()
filename = 1
for i in range(len(csvfile)):
    if i % 100000 == 0:
        open('all_energy_statistics' + str(filename) + '.csv', 'w+').writelines(csvfile[i:i+100000])
        filename += 1