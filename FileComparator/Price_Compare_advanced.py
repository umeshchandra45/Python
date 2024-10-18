import pandas as pd
import numpy as np
from openpyxl import load_workbook
from msal import ConfidentialClientApplication
from simple_salesforce import Salesforce, SalesforceLogin
from copy import deepcopy

# from dotenv import load_dotenv
#
# load_dotenv()

def main(business_file, query_file, primary_column, output_file):
    input_df = pd.read_excel(business_file, sheet_name='Sheet1')
    query_df = pd.read_excel(query_file)  # Query DF nothing but the system extract data

    input_df = input_df.rename(columns={primary_column: primary_column + '_Input'})
    query_df = query_df.rename(columns={primary_column: primary_column + '_Output'})

    matched_df = pd.DataFrame()

    # Merge the two dataframes(Business & System) on the primary column
    matched_df = pd.merge(input_df, query_df, left_on=primary_column + '_Input', right_on=primary_column + '_Output',
                          how='outer', suffixes=('_Input', '_Output'))
    base_columns = set(col.rsplit('_', 1)[0] for col in matched_df.columns if '_' in col)
    matched_df_copy = deepcopy(matched_df)
    matched_df_copy = matched_df_copy.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    matched_df_copy = matched_df_copy.applymap(lambda x: x.upper() if isinstance(x, str) else x)
    # Adding Status Column
    # import pdb;pdb.set_trace()
    for base_column in base_columns:
        business_column = f'{base_column}_Input'
        system_column = f'{base_column}_Output'
        status_column = f'{base_column}_Status'
        if business_column in matched_df_copy.columns and system_column in matched_df_copy.columns:
            # df.value1 = df.value1.round()
            if business_column in ["Net Price _Input"]:
                matched_df_copy[business_column] = matched_df_copy[business_column].round()
                matched_df_copy[system_column] = matched_df_copy[system_column].round()
                matched_df[status_column] = np.where(matched_df_copy[business_column] == matched_df_copy[system_column], 'Matched',
                                                 'Not Matched')
            else:
                matched_df[status_column] = np.where(matched_df_copy[business_column] == matched_df_copy[system_column],
                                                     'Matched',
                                                     'Not Matched')
            # Get the current column names
            cols = list(matched_df.columns)
            cols.remove(business_column)
            cols.remove(system_column)
            cols.remove(status_column)
            cols.extend([business_column, system_column, status_column])
            matched_df = matched_df[cols]
    output_file = fr"D:\Work\Output_Sheets\{output_file}_output.xlsx"
    matched_df.to_excel(output_file, index=False)
    print("File Created Successfully.............")


if __name__ == "__main__":
    business_file = fr"D:\Work\Input_Sheets\PGGA-SE_CM_Businessfile 2.xlsx"
    query_file = fr"D:\Work\Input_Sheets\PGGA-SE_CM_SystemExtract -26thJuly.xlsx"
    primary_column = 'Business Partner ICV/GUID'
    # primary_column = 'Material ID'
    # primary_column = 'Product Code'
    output_file = "Data_PGGA-SE_CM_SystemExtract-26thJuly"
    main(business_file, query_file, primary_column, output_file)