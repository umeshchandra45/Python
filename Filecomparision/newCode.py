import pandas as pd
import numpy as np

def clean_text(text):
    """Function to clean unwanted characters from text."""
    if isinstance(text, str):
        return text.replace('\r', '').replace('\n', '').strip()
    return text

def main(business_file, query_file, primary_column, output_file):
    try:
        # Load data from Excel files
        print(f"Loading data from {business_file} and {query_file}")
        input_df = pd.read_excel(business_file, sheet_name='Sheet1')
        query_df = pd.read_excel(query_file)

        # Rename the primary column in both dataframes
        input_df.rename(columns={primary_column: primary_column + '_Input'}, inplace=True)
        query_df.rename(columns={primary_column: primary_column + '_Output'}, inplace=True)

        # Merge the dataframes on the primary column
        print("Merging dataframes")
        matched_df = pd.merge(input_df, query_df,
                              left_on=primary_column + '_Input',
                              right_on=primary_column + '_Output',
                              how='outer',
                              suffixes=('_Input', '_Output'))

        # Normalize string columns
        str_cols = [col for col in matched_df.columns if col.endswith('_Input') or col.endswith('_Output')]
        matched_df[str_cols] = matched_df[str_cols].applymap(clean_text)

        # Adding Status Columns
        print("Adding status columns")
        for base_column in set(col.rsplit('_', 1)[0] for col in matched_df.columns if '_' in col):
            business_column = f'{base_column}_Input'
            system_column = f'{base_column}_Output'
            status_column = f'{base_column}_Status'

            if business_column in matched_df.columns and system_column in matched_df.columns:
                # Handle rounding for specific columns
                if business_column == "Net Price_Input":
                    matched_df[business_column] = matched_df[business_column].round()
                    matched_df[system_column] = matched_df[system_column].round()

                # Check for "Matched" status
                matched_df[status_column] = matched_df.apply(
                    lambda row: 'Matched' if ' '.join(str(row[business_column]).split()).upper() == ' '.join(
                        str(row[system_column]).split()).upper()
                    else 'Not Matched', axis=1
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

        # Add column to count 'Not Matched' cells per row
        matched_df['Not Matched Count'] = matched_df[status_columns].apply(
            lambda row: (row == 'Not Matched').sum(), axis=1
        )

        # Add unique column names row
        print("Adding unique column names row")
        unique_columns_row = pd.Series({col: col for col in matched_df.columns}, name='Unique Column Names')
        matched_df = pd.concat([matched_df, unique_columns_row.to_frame().T], ignore_index=True)

        # Reorder columns to put 'Not Matched Count' at the end
        cols = [col for col in matched_df.columns if col != 'Not Matched Count'] + ['Not Matched Count']
        matched_df = matched_df[cols]

        # Add summary row
        print("Adding summary row")
        summary_data = []
        for status_column in status_columns:
            matched_count = (matched_df[status_column] == 'Matched').sum()
            error_count = (matched_df[status_column] == 'Not Matched').sum()
            total_count = len(matched_df)
            error_percentage = (error_count * 100.0) / total_count if total_count > 0 else 0
            summary_data.append({
                'Column': status_column,
                'Total Matched': matched_count,
                'Error': error_count,
                'Percent Error': f"{error_percentage:.2f}%"
            })

        # Creating summary DataFrame
        summary_df = pd.DataFrame(summary_data).set_index('Column')

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
            summary_df.to_excel(writer, sheet_name='Summary Data')

        print("File Created Successfully.............")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    business_file = fr"D:\Work\Input_Sheets\UserRole_Source.xlsx"
    query_file = fr"D:\Work\Input_Sheets\UserRole_Target.xlsx"
    primary_column = 'Id'
    output_file = "delete1"
    main(business_file, query_file, primary_column, output_file)
