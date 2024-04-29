import pandas as pd
import os

# Path to the folder containing TSV files
folder_path = 'datasets'

# List to store dataframes read from TSV files
dfs = []

# Read each TSV file into a dataframe and append it to the dfs list
for file_name in os.listdir(folder_path):
    if file_name.endswith('.tsv'):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path, sep='\t')
        dfs.append(df)

# Concatenate all dataframes in the list dfs
combined_df = pd.concat(dfs, ignore_index=True)

# Read the 'patents_19802010.csv' file
patents_df = pd.read_csv('patents_19802010.csv')

# Perform a left join on the patents_df and combined_df based on 'patent_id' column
merged_df = pd.merge(patents_df,combined_df, on='patent_id', how='left')

# Print the merged dataframe
print(merged_df)

#Save data to file
merged_df.to_csv('patents_with_summary.csv')