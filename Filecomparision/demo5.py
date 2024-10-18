import pandas as pd
import numpy as np
from copy import deepcopy

def normalize_text(text):
    if isinstance(text, str):
        # Remove newline characters, multiple spaces and strip leading/trailing spaces
        return ' '.join(text.replace('\n', ' ').split()).upper()
    return text
def main(business_file, query_file, primary_column, output_file):
    try:
        # Load data from Excel files
        print(f"Loading data from {business_file} and {query_file}")
        input_df = pd.read_excel(business_file, sheet_name='Sheet1')
        query_df = pd.read_excel(query_file)

        # Rename the primary column in both dataframes
        input_df = input_df.rename(columns={primary_column: primary_column + '_Input'})
        query_df = query_df.rename(columns={primary_column: primary_column + '_Output'})

        # Merge the dataframes on the primary column
        print("Merging dataframes")
        matched_df = pd.merge(input_df, query_df, left_on=primary_column + '_Input', right_on=primary_column + '_Output', how='outer', suffixes=('_Input', '_Output'))

        base_columns = set(col.rsplit('_', 1)[0] for col in matched_df.columns if '_' in col)
        matched_df_copy = deepcopy(matched_df)
        matched_df_copy = matched_df_copy.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        matched_df_copy = matched_df_copy.applymap(lambda x: x.upper() if isinstance(x, str) else x)

        # Adding Status Column
        print("Adding status columns")
        for base_column in base_columns:
            business_column = f'{base_column}_Input'
            system_column = f'{base_column}_Output'
            status_column = f'{base_column}_Status'

            if business_column in matched_df_copy.columns and system_column in matched_df_copy.columns:
                # Handle rounding for specific columns
                if business_column == "Net Price _Input":
                    matched_df_copy[business_column] = matched_df_copy[business_column].round()
                    matched_df_copy[system_column] = matched_df_copy[system_column].round()

                # Check for "Matched" status
                matched_df[status_column] = np.where(
                    (matched_df_copy[business_column].fillna('') == matched_df_copy[system_column].fillna('')),
                    'Matched',
                    'Not Matched'
                )

                # Reorder columns
                cols = list(matched_df.columns)
                if business_column in cols:
                    cols.remove(business_column)
                if system_column in cols:
                    cols.remove(system_column)
                if status_column in cols:
                    cols.remove(status_column)
                cols.extend([business_column, system_column, status_column])
                matched_df = matched_df[cols]

        # Adding Pass/Fail Column
        print("Adding Pass/Fail column")
        status_columns = [col for col in matched_df.columns if col.endswith('_Status')]
        matched_df['Result'] = matched_df[status_columns].apply(
            lambda row: 'Fail' if 'Not Matched' in row.values else 'Pass', axis=1
        )

        # Ensuring 'Result' column is added at the end
        cols = list(matched_df.columns)
        if 'Result' in cols:
            cols.remove('Result')
        cols.append('Result')
        matched_df = matched_df[cols]

        # Add summary row for each status column
        print("Adding summary row")
        summary_row = pd.Series([''] * len(matched_df.columns), index=matched_df.columns)
        for status_column in status_columns:
            matched_count = (matched_df[status_column] == 'Matched').sum()
            total_count = len(matched_df)
            error_count = (matched_df[status_column] == 'Not Matched').sum()
            error_percentage = (error_count * 100.0) / total_count if total_count > 0 else 0
            summary_row[status_column] = f"Total Matched: {matched_count}, Error: {error_count}, Percent Error: {error_percentage:.2f}%"

        # Adding the summary row to the DataFrame
        matched_df = pd.concat([matched_df, pd.DataFrame([summary_row])], ignore_index=True)

        # Identifying mismatched rows and columns
        print("Identifying mismatched rows and columns")
        mismatch_data = []
        for index, row in matched_df.iterrows():
            mismatched_columns = [col for col in status_columns if row[col] == 'Not Matched']
            if mismatched_columns:
                row_data = {
                    'Row Number': index + 1,  # Row numbers in Excel are 1-based
                    'Id_Input': row[f'{primary_column}_Input'],
                    'Not Matched Columns': ', '.join([col.replace('_Status', '') for col in mismatched_columns])
                }
                mismatch_data.append(row_data)

        # Creating a DataFrame for mismatches
        mismatch_df = pd.DataFrame(mismatch_data)

        # Save to Excel
        output_file_path = fr"D:\Work\Output_Sheets\{output_file}_output.xlsx"
        print(f"Saving results to {output_file_path}")
        with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
            matched_df.to_excel(writer, sheet_name='Matched Data', index=False)
            mismatch_df.to_excel(writer, sheet_name='Mismatch Data', index=False)

        print("File Created Successfully.............")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    business_file = fr"D:\Work\Input_Sheets\Sample source.xlsx"
    query_file = fr"D:\Work\Input_Sheets\Sample target.xlsx"
    primary_column = 'Id'
    output_file = "spacedel2"
    main(business_file, query_file, primary_column, output_file)