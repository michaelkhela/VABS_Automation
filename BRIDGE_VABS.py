# Vineland Data Cleaning + Preparing to Import to REDCap
# PURPOSE: To clean VABS data from q-global and create an importable CSV for REDCap
# Created by Michael Khela and Gabriela Davila on Feb-May/2024

#import libraries
import pandas as pd
from datetime import datetime, timedelta

# connects to run code
def vabs_fcn(root_filepath, qglobal, sub_cohort): 
    
    # df_qglob
    df_qglob=pd.read_csv(root_filepath + 'Assessment_Packages/VABS_package/VABS_inputs/'+ qglobal, dtype=object)

    # Make a copy of df_qglob
    df_vabs = df_qglob.copy()  

    # Maps the old column headers to the new column headers
    column_mapping= {
        'ExamineeID':'subject_id',
        'AdministrationDate': 'date_vineland',
        'vi3_rec_raw': 'vas_receptive_raw',
        'vi3_exp_raw': 'vas_expressive_raw',
        'vi3_wrn_raw': 'vas_written_raw',
        'vi3_per_raw': 'vas_personal_raw',
        'vi3_dom_raw': 'vas_domestic_raw',
        'vi3_cmm_raw': 'vas_community_raw',
        'vi3_ipr_raw': 'vas_interpersonal_raw',
        'vi3_pla_raw': 'vas_play_raw',
        'vi3_cop_raw': 'vas_coping_raw',
        'vi3_gmo_raw': 'vas_gross_motor_raw',
        'vi3_fmo_raw': 'vas_fine_motor_raw',   
        'vi3_rec_ss': 'vas_receptive_vscale',
        'vi3_exp_ss': 'vas_expressive_vscale',
        'vi3_wrn_ss': 'vas_written_vscale',
        'vi3_per_ss': 'vas_personal_vscale',
        'vi3_dom_ss': 'vas_domestic_vscale',
        'vi3_cmm_ss': 'vas_community_vscale',
        'vi3_ipr_ss': 'vas_interpersonal_vscale',
        'vi3_pla_ss': 'vas_play_vscale',
        'vi3_cop_ss': 'vas_coping_vscale',
        'vi3_gmo_ss': 'vas_gross_motor_vscale',
        'vi3_fmo_ss': 'vas_fine_motor_vscale',
        'vi3_com_ss': 'vas_communication_ss',
        'vi3_dls_ss': 'vas_dailyliving_ss',
        'vi3_soc_ss': 'vas_social_ss',
        'vi3_mot_ss': 'vas_motor_ss',
        'vi3_abc_ss': 'vas_abc_ss',
        'vi3_com_pr': 'vas_communication_pr',
        'vi3_dls_pr': 'vas_dailyliving_pr',
        'vi3_soc_pr': 'vas_social_pr',
        'vi3_mot_pr': 'vas_motor_pr',
        'vi3_abc_pr': 'vas_abc_pr',
        'vi3_rec_ae': 'vas_receptive_age',
        'vi3_exp_ae':'vas_expressive_age',
        'vi3_wrn_ae': 'vas_written_age',
        'vi3_per_ae': 'vas_personal_age',
        'vi3_dom_ae': 'vas_domestic_age',
        'vi3_cmm_ae': 'vas_community_age',
        'vi3_ipr_ae': 'vas_interpersonal_age',
        'vi3_pla_ae': 'vas_play_age',
        'vi3_cop_ae': 'vas_coping_age',
        'vi3_gmo_ae': 'vas_gross_motor_age',
        'vi3_fmo_ae': 'vas_fine_motor_age',
        'vi3_rec_gsv': 'vas_receptive_gsv',
        'vi3_exp_gsv': 'vas_expressive_gsv',
        'vi3_wrn_gsv': 'vas_written_gsv',
        'vi3_per_gsv': 'vas_personal_gsv',
        'vi3_dom_gsv': 'vas_domestic_gsv',
        'vi3_cmm_gsv': 'vas_community_gsv',
        'vi3_ipr_gsv': 'vas_interpersonal_gsv',
        'vi3_pla_gsv': 'vas_play_gsv',
        'vi3_cop_gsv': 'vas_coping_gsv',
        'vi3_gmo_gsv': 'vas_gross_motor_gsv',
        'vi3_fmo_gsv': 'vas_fine_motor_gsv'
    }
    df_vabs.rename(columns=column_mapping, inplace=True)

    df_cohort_id=pd.read_csv(root_filepath + 'Assessment_Packages/VABS_package/VABS_inputs/' + sub_cohort)
    
    # Convert 'subject_id' column to str type in df_vabs
    df_vabs['subject_id'] = df_vabs['subject_id'].astype(str)

    # Adds column "vas_assessment_format" to be added for REDcap upload
    df_vabs['vas_assessment_format'] = "1"

    # Adds column "vineland3_complete" to be added for REDcap upload
    df_vabs['vineland3_complete'] = "1"  

    # Replace NaN values with -888
    df_vabs[df_vabs.isnull()] = -888

    # Convert date columns to datetime objects
    date_format = '%m/%d/%Y'

    #### Assess whether VABS data is for V1 or V2 by checking the visit date of V1/V2
    # Convert date_vineland column to datetime objects with the specified format
    df_vabs['date_vineland'] = pd.to_datetime(df_vabs['date_vineland'], format=date_format)
    df_cohort_id['visit_date'] = pd.to_datetime(df_cohort_id['visit_date'])

    # Iterate over rows in df_vabs
    for index2, row2 in df_vabs.iterrows():
        # Iterate over rows in df_cohort_id
        for index1, row1 in df_cohort_id.iterrows():
            # Check if the dates are within 3 weeks and subject IDs match
            # GDM 2024-09-19: added abs() to dates operation line
            if pd.notnull(row1['visit_date']) and pd.notnull(row2['date_vineland']):  # Check for NaN values
                if (abs(row2['date_vineland'] - row1['visit_date']) <= timedelta(weeks=3)) and (row2['subject_id'] == row1['subject_id']):
                    # Insert redcap_event_name from df_cohort_id into df_vabs
                    df_vabs.at[index2, 'redcap_event_name'] = row1['redcap_event_name']
                    break  # Break the loop after finding the match

    # copies columns for age and renames them to ae_m
    ae_cols=['vas_receptive_age', 'vas_expressive_age', 'vas_written_age', 'vas_personal_age', 'vas_domestic_age', 'vas_community_age', 'vas_interpersonal_age', 'vas_play_age', 'vas_coping_age', 'vas_gross_motor_age', 'vas_fine_motor_age']
    ae_m_cols = [name.replace('age', 'ae_m') for name in ae_cols]
    for i in range(len(ae_cols)):
        df_vabs[ae_m_cols[i]] = df_vabs[ae_cols[i]]

    # converts to age in y:m to m acccounting for "+" and "<" or ">"
    def convert_to_months(age):
        if pd.isnull(age):
            return age
        elif isinstance(age, int):
            # If the age is already in months (as an integer), return it
            return age
        else:
            # Extract any '<' or '>' symbols
            sign = ''
            if '<' in age:
                sign = '<'
                age = age.replace('<', '')
            elif '>' in age:
                sign = '>'
                age = age.replace('>', '')

            # Check if there is a '+' sign
            plus = '+' if '+' in age else ''
            age = age.replace('+', '')

        # Convert years and months to total months
        years, months = map(int, age.split(':'))
        total_months = years * 12 + months
        # Concatenate the sign and plus if present
        total_months_str = f"{sign}{total_months}{plus}"
        return total_months_str
    
    # Columns to be converted
    columns_to_convert = ['vas_receptive_ae_m', 'vas_expressive_ae_m', 'vas_written_ae_m', 'vas_personal_ae_m', 'vas_domestic_ae_m', 'vas_community_ae_m', 'vas_interpersonal_ae_m', 'vas_play_ae_m', 'vas_coping_ae_m', 'vas_gross_motor_ae_m', 'vas_fine_motor_ae_m']

    # Apply the conversion function to the relevant columns
    for column in columns_to_convert:
        df_vabs[column] = df_vabs[column].apply(convert_to_months)

    #includes all the columns that are needed
    columns_to_include = [
        'subject_id', 'date_vineland', 'vas_assessment_format',
        'vas_receptive_raw', 'vas_receptive_vscale', 'vas_receptive_age', 'vas_receptive_gsv',
        'vas_expressive_raw', 'vas_expressive_vscale', 'vas_expressive_age', 'vas_expressive_gsv',
        'vas_written_raw', 'vas_written_vscale', 'vas_written_age', 'vas_written_gsv',
        'vas_communication_ss', 'vas_communication_pr',
        'vas_personal_raw', 'vas_personal_vscale', 'vas_personal_age', 'vas_personal_gsv',
        'vas_domestic_raw', 'vas_domestic_vscale', 'vas_domestic_age', 'vas_domestic_gsv',
        'vas_community_raw', 'vas_community_vscale', 'vas_community_age', 'vas_community_gsv',
        'vas_dailyliving_ss', 'vas_dailyliving_pr',
        'vas_interpersonal_raw', 'vas_interpersonal_vscale', 'vas_interpersonal_age', 'vas_interpersonal_gsv',
        'vas_play_raw', 'vas_play_vscale', 'vas_play_age', 'vas_play_gsv',
        'vas_coping_raw', 'vas_coping_vscale', 'vas_coping_age', 'vas_coping_gsv',
        'vas_social_ss', 'vas_social_pr',
        'vas_gross_motor_raw', 'vas_gross_motor_vscale', 'vas_gross_motor_age', 'vas_gross_motor_gsv',
        'vas_fine_motor_raw', 'vas_fine_motor_vscale', 'vas_fine_motor_age', 'vas_fine_motor_gsv',
        'vas_motor_ss', 'vas_motor_pr', 'vas_abc_ss', 'vas_abc_pr','vineland3_complete','redcap_event_name','vas_receptive_ae_m', 
        'vas_expressive_ae_m', 'vas_written_ae_m', 'vas_personal_ae_m', 'vas_domestic_ae_m', 'vas_community_ae_m', 'vas_interpersonal_ae_m',
        'vas_play_ae_m', 'vas_coping_ae_m', 'vas_gross_motor_ae_m', 'vas_fine_motor_ae_m'
    ]
    df_vabs_mod=df_vabs[columns_to_include]

    
    # Rearrange the DataFrame columns to match the specified order
    data_vabs = df_vabs_mod[[
        'subject_id', 'redcap_event_name', 'date_vineland', 'vas_assessment_format',
        'vas_receptive_raw', 'vas_receptive_vscale', 'vas_receptive_age', 'vas_receptive_ae_m', 'vas_receptive_gsv',
        'vas_expressive_raw', 'vas_expressive_vscale', 'vas_expressive_age', 'vas_expressive_ae_m', 'vas_expressive_gsv',
        'vas_written_raw', 'vas_written_vscale', 'vas_written_age', 'vas_written_ae_m', 'vas_written_gsv',
        'vas_communication_ss', 'vas_communication_pr',
        'vas_personal_raw', 'vas_personal_vscale', 'vas_personal_age', 'vas_personal_ae_m', 'vas_personal_gsv',
        'vas_domestic_raw', 'vas_domestic_vscale', 'vas_domestic_age', 'vas_domestic_ae_m', 'vas_domestic_gsv',
        'vas_community_raw', 'vas_community_vscale', 'vas_community_age', 'vas_community_ae_m', 'vas_community_gsv',
        'vas_dailyliving_ss', 'vas_dailyliving_pr',
        'vas_interpersonal_raw', 'vas_interpersonal_vscale', 'vas_interpersonal_age', 'vas_interpersonal_ae_m', 'vas_interpersonal_gsv',
        'vas_play_raw', 'vas_play_vscale', 'vas_play_age', 'vas_play_ae_m', 'vas_play_gsv',
        'vas_coping_raw', 'vas_coping_vscale', 'vas_coping_age', 'vas_coping_ae_m', 'vas_coping_gsv',
        'vas_social_ss', 'vas_social_pr',
        'vas_gross_motor_raw', 'vas_gross_motor_vscale', 'vas_gross_motor_age', 'vas_gross_motor_ae_m', 'vas_gross_motor_gsv',
        'vas_fine_motor_raw', 'vas_fine_motor_vscale', 'vas_fine_motor_age', 'vas_fine_motor_ae_m', 'vas_fine_motor_gsv',
        'vas_motor_ss', 'vas_motor_pr', 'vas_abc_ss', 'vas_abc_pr', 'vineland3_complete'
    ]]

    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time as a string
    date_string = current_datetime.strftime("%m-%d-%Y")

    # Construct the new CSV filename with the date
    new_csv_filename = f"Importable_VABS_BRIDGE_{date_string}.csv"

    # Specify the full file path for the new CSV file
    new_csv_file_path = root_filepath + 'VABS/' + new_csv_filename

    # Convert the new data (data_vabs) to CSV and save it as the new file
    data_vabs.to_csv(new_csv_file_path, index=False)

    # Print a message indicating that the new CSV file has been created
    print("Congratulations! The new data has been saved to:", new_csv_file_path)
