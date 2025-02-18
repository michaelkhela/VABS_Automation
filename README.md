# VABS Auto-Scoring  

## Overview  

VABS Auto-Scoring is a Python-based tool designed to automate the scoring of Vineland Adaptive Behavior Scale (VABS) assessments for the BRIDGE study. This script processes raw scores from a q-global export creating a REDCap ready import.  

This tool was created by Michael Khela for use across the LCN, tailored specifically for the BRIDGE REDCap build.  

## Authors  

Michael Khela  
Email: michael.khela99@gmail.com  

## Requirements  

**Python Version:** 3.12.1  

**Required Python libraries:**  
- pandas (2.2.0)  
- openpyxl (3.1.2)  

To install dependencies, run:  

```sh
pip install pandas openpyxl
```

## Installation  

1. Clone or download this repository.  
2. Copy the relevant scripts to your working directory.  
3. Ensure the input CSV file is formatted correctly with the required columns.  

## Usage  

### 1. Export Data from Q-Global 
1. Log into Q-global (https://qglobal.pearsonassessments.com/qg/login.seam)
2. Click ‘More Actions’, then ‘Export Assessment Records’
3. Click ‘Search Reports’ and select ‘Vineland-3 Comprehensive Report’  
4. Select the records
5. Confrigure the export according yo your study requirments
6. Download and rename export as "Qglobal_VABS_YYYY-MM-DD.csv"

### 3. Run the Script  
Run the following command in your terminal:  

```sh
python BRIDGE_Run_VABS.py
```

Alternatively, run the script in **Spyder** (Anaconda) by:  
- Opening `BRIDGE_Run_VABS.py`.  
- Updating the path if necessary.  
- Ensuring the `REDCap_file name` matches the downloaded CSV.  
- Clicking **Run** to execute the script.  

Once completed, a message should confirm successful execution.  

### 4. Output  
The script generates an output CSV file in the output directory, following this format:  

This file is structured for direct import into REDCap.  

## Notes  

- This script is specifically tailored for the BRIDGE study.   
- Only **Research Assistants** should import the script's output into Internal REDCap.  

## Contact  

For issues or inquiries, contact:  
Michael Khela – michael.khela99@gmail.com  
