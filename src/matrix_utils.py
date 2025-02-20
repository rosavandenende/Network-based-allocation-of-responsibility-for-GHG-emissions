import pandas as pd
import numpy as np
from functions_utils import sector_index

#All these functions are intended to extract the correct data and save it as csv files. Only need to run once. 

def convert_xlsb_to_csv(xlsb_file, csv_file):
    # Read the single sheet directly
    df = pd.read_excel(xlsb_file, engine='pyxlsb',header = None)
    print(f"Matrix shape: {df.shape}") #Check whether we have the right dimensions(2464x2464)
    df.to_csv(csv_file, index=False, header=False) #No header
    return

def aggregate_matrix_countries(csv_file, output_csv, block_size=56):
    df = pd.read_csv(csv_file, header=None) # Load the CSV file into a DataFrame
    matrix = df.values # Convert to NumPy array for faster operations
    rows, cols = matrix.shape 
    if rows % block_size != 0 or cols % block_size != 0:
        raise ValueError("Matrix dimensions are not divisible by block size")
    num_blocks = rows // block_size # Calculate the number of blocks, check if it is indeed the size of all sectors 

    aggregated_matrix = np.zeros((num_blocks, num_blocks))  # Create an empty matrix for aggregation
    # Perform block aggregation
    for i in range(num_blocks):
        for j in range(num_blocks):
            block = matrix[
                i * block_size:(i + 1) * block_size,
                j * block_size:(j + 1) * block_size
            ]
            aggregated_matrix[i, j] = np.sum(block)
    pd.DataFrame(aggregated_matrix).to_csv(output_csv, index=False, header=False) #Save aggregated matrix to CSV
    print(f"Aggregated matrix saved to {output_csv}")
    return

def create_phi_psi_matrices(csv_file,psi_csv_path,phi_csv_path):
    # Load the aggregated 44x44 matrix
    df = pd.read_csv(csv_file, header=None)
    matrix = df.values

    # Create Phi: Row-normalized and then transposed
    row_sums = matrix.sum(axis=1, keepdims=True)
    phi = np.divide(matrix, row_sums, where=row_sums != 0).T  # Transpose after normalization

    # Create Psi: Column-normalized
    col_sums = matrix.sum(axis=0, keepdims=True)
    psi = np.divide(matrix, col_sums, where=col_sums != 0)

    # Convert results to DataFrames
    phi_df = pd.DataFrame(phi)
    psi_df = pd.DataFrame(psi)
    phi_df.to_csv(phi_csv_path, index=False, header=False)
    psi_df.to_csv(psi_csv_path, index=False, header=False)

    print(f"Phi matrix saved to {phi_csv_path}")
    print(f"Psi matrix saved to {psi_csv_path}")
    return 


def unwrap_emissions(file_emissions, output_csv="emissions_summary.csv"):
    tabs = pd.ExcelFile(file_emissions).sheet_names # Read Excel file and get sheet names
    country_list = tabs[2:45]   # Select country sheets (excluding ROW for now)
    list_emissions = []
    for i in np.arange(2, 45):
        country_data = pd.read_excel(file_emissions, sheet_name=i)
        list_emissions.append(country_data['2014'].sum()) #we want to have the total emissions, so we sum

    df_co2 = pd.DataFrame({'emissions': list_emissions}, index=country_list)
    df_nld = pd.DataFrame({'emissions': [1.6e+05]}, index=['NLD']) # Add Netherlands (NLD) emissions manually
    df_co2 = pd.concat([df_co2, df_nld])  # Concatenate all data

     # Separate ROW if it exists
    if 'RoW' in df_co2.index:
        df_row = df_co2.loc[['RoW']]
        df_co2 = df_co2.drop(index='RoW').sort_index()
        df_co2 = pd.concat([df_co2, df_row])
    else:
        df_co2 = df_co2.sort_index()

    # Print the final DataFrame
    print("\nFinal Emissions DataFrame (alphabetical with ROW at the end):")
    print(df_co2)

    df_co2.to_csv(output_csv, index=False)  # Save DataFrame to CSV
    print(f"Emissions summary saved to {output_csv}")
    return df_co2
    
def extract_usa_emissions(file_emissions, output_csv="usa_2014.csv"):
    # Load the 'USA' sheet from the Excel file
    df_usa = pd.read_excel(file_emissions, sheet_name='USA')
    if '2014' not in df_usa.columns:
        raise ValueError("The column '2014' is not found in the 'USA' sheet.") 
    usa_2014 = df_usa[['2014']]     # Extract only the '2014' column
    usa_2014.to_csv(output_csv, index=False) 
    print(f"'2014' column from 'USA' sheet saved to {output_csv}")
    return usa_2014

def save_csv_as_npy(input_path, output_path):
    np.save(output_path,np.loadtxt(input_path, delimiter = ","))

def scope2_emissions(sect,sectors):
    f_scope2 = np.zeros(len(sectors))
    index = sector_index(sect,sectors)
    f_scope2[index] = np.load("src/data/usa_emissions.npy")[index]
    print(f_scope2)
    np.save("sc2_usa_emissions.npy",f_scope2)

