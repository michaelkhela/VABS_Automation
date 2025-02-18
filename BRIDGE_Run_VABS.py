# Vineland Data Cleaning + Preparing to Import to REDCap
# PURPOSE: To clean VABS data from q-global and create an importable CSV for REDCap

# Please note the following before running the code:
# - ALL INPUT DOCUMENTS HAVE TO BE CLOSED

# ***** BRIDGE SPECIFIC ******

# Please note the following regarding data:
# - if "-888" is shown = data is not applicable to the kiddo (not shown to parent)

# Created by Michael Khela and Gabriela Davila on Feb-May/2024

import sys 
import os

# INSERT FILE NAME OF THE Q-GLOBAL EXPORT
qglobal = "Qglobal_2024-10-02.csv"

# INSERT FILE NAME OF THE ID-COHORT-DATE EXPORT FROM REDCap
sub_cohort = "IDCohortVisitDate_2024-10-02.csv"
    
# INSERT FILE PATH TO "Automated_Assessments" FOLDER
root_filepath = r"/Volumes/Groups/P00025493 = Fragile X/BRIDGE Study/Data/Automated_Assessments/"

#-----------DO NOT EDIT BELOW-------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(root_filepath + 'Assessment_Packages/VABS_package/VABS_Background_Code/'))
from BRIDGE_VABS import vabs_fcn

vabs_fcn(root_filepath, qglobal, sub_cohort)

