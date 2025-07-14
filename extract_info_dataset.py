import argparse
import os
import glob
import pydicom
import json
import os

#***************************************************************************************************************************
#The function "filter_info_dataset" assumes that the Dataset directory structure is as follows: 
#Note: Any file with an extension other than .dcm will be discarded and won't be analised
#DATASETS_DIR
#   |
#   -- DATASET Identifier
#		|
#		-- PATIENT_CASE 1
#		|		|
#		|		-- STUDY 1
#		|		|	|
#		|		|	-- SERIES 1
#		|		|	|	|
#		|		|	|	-- DICOM FILE 1(.dcm extension)
#		|		|	|	-- DICOM FILE 2(.dcm extension)
#		|		|	|	-- ..
#		|		|	-- SERIES 2
#		|		|	-- ...
#		|		-- STUDY 2
#		|		|	-- ...
#       |		-- ...
#		-- PATIENT_CASE 2
#		-- ...
# The function builds a diccionary in function of the input paramer.
# Input:
#       -- verbose: It is a bollean value. It shows on screen information about the process of build the diccionary
#       ROOT_DATASET: It is the path from starting the building of the lists.  
# Output:

#***************************************************************************************************************************
def extract_info_dataset(verbose, ROOT_DATASET_DIR, manufacturers,bodyparts, numberseries, alldicoms):
    #Dictionary with the results extracted from the datalake (path)
    list_manufacturers = []
    list_bodyparts = []    
    list_series = []
    
    
    if verbose: print("Processing Dataset  directory: " + ROOT_DATASET_DIR)
    
    #Extract Patient Cases subdirs of a given Dataset if the directory has access permision
    if not os.access(ROOT_DATASET_DIR, os.R_OK):
        print(F"Access forbiden to this folder {ROOT_DATASET_DIR}")
        print("The process has been canceled");
        return []                      
    for name_dir_patient_case in os.listdir(ROOT_DATASET_DIR):
        if os.path.isdir(os.path.join(ROOT_DATASET_DIR, name_dir_patient_case)):
            dir_patient_case = os.path.join(ROOT_DATASET_DIR, name_dir_patient_case)
            if verbose: print("**Processing Patient Case Directory" + dir_patient_case)
            #Extract Study Subdirs of a given patient Case if the directory has access permision
            if not os.access(dir_patient_case, os.R_OK):
                print(F"Access forbiden to this folder {dir_patient_case}")
                print("The process has been canceled");
                return []
            for name_dir_study in os.listdir(dir_patient_case):
                if os.path.isdir(os.path.join(dir_patient_case, name_dir_study)):
                    dir_study = os.path.join(dir_patient_case, name_dir_study)
                    if verbose: print("****Processing Study Directory: " + dir_study)
                    #Extract Series Subdirs of a given Study if the directory has access permision
                    if not os.access(dir_study, os.R_OK):
                        print(F"Access forbiden to this folder {dir_study}")
                        print("The process has been canceled");
                        return []
                    for name_dir_serie in os.listdir(dir_study):
                        if os.path.isdir(os.path.join(dir_study, name_dir_serie)):
                            dir_serie = os.path.join(dir_study, name_dir_serie)
                            if verbose: print("******Processing Series Directory: " + dir_serie)
                           
    			            #Extract dicom files of a given series if the directory has access permision
                            if not os.access(dir_serie, os.R_OK):
                                print(F"Access forbiden to this folder {dir_serie}")
                                print("The process has been canceled");
                                return []
                            list_series.append(dir_serie)
                            for dicom_file in glob.glob(os.path.join(dir_serie,"*.dcm")):
                                if verbose: print("********Processing Dicom File: " + dicom_file)
                                # Load the DICOM File to read the TAGs                                        
                                dcm = pydicom.dcmread(dicom_file)
                                
                                if (bodyparts):
                                    if (0x00180015) in dcm: # TAG BodyPart exists in DICOM file
                                        # Get the value of the TAG  
                                        tag_0018_0015 = dcm[0x0018, 0x0015].value
                                        # Print the value of the TAG 
                                        if verbose: print("********** Body Part: " + tag_0018_0015)
                                    else: # TAG BodyPart doesn't exists
                                        if verbose: print("**********The DICOM tag 0018,0015 (Body Part) is not defined in the DicOm file")
                                        tag_0018_0015 = "Undefined"
                                    if not tag_0018_0015 in list_bodyparts: list_bodyparts.append(tag_0018_0015)
                                
                                if (manufacturers):
                                    if (0x00080070) in dcm: # TAG Manufacturer exists in DICOM file
                                        # Get the value of the TAG  
                                        tag_0008_0070 = dcm[0x0008, 0x0070].value
                                        # Print the value of the TAG 
                                        if verbose: print("**********Manufacturer: " + tag_0008_0070)
                                    else: # TAG BodyPart doesn't exists
                                        if verbose: print("**********The DICOM tag 0008,0070 (Manufacturer) is not defined in the DicOm file")
                                        tag_0008_0070 = "Undefined"
                                    if not tag_0008_0070 in list_manufacturers: list_manufacturers.append(tag_0008_0070)
                                    
                                if (not alldicoms):
                                    break
                                     
    return list_manufacturers, list_bodyparts, list_series


if __name__ == '__main__':	
    parser = argparse.ArgumentParser(prog='extract_info_dataset.py', description='It Extracts Information of CHAIMELEON Dataset from a base directory.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show all info on screen about the creation process of the dictionaries.') 
    parser.add_argument('-f', '--manufacturers', action='store_true', help='It Shows all manufacturers in a dataset.') 
    parser.add_argument('-b', '--bodyparts', action='store_true', help='It Shows all body parts included in a dataset.') 
    parser.add_argument('-s', '--numberseries', action='store_true', help='It Shows number of series.') 
    parser.add_argument('-o', '--output', help='Out File') 
    parser.add_argument('-a', '--alldicoms', action='store_true', help='Read all DICOM files in the series. It is usually not required, only the first one.')
    
    
    parser.add_argument('path', help='Root of the directory to analise.')
    args = parser.parse_args()

    f = None
    if args.output:
        p = os.path.expandvars(args.output)
        print(p)
        path = os.path.dirname(p)
        os.makedirs(path, exist_ok=True)
        f = open(p, "w+")

        
    list_manufacturers, list_bodyparts, list_series  = extract_info_dataset(args.verbose, args.path, args.manufacturers, args.bodyparts, args.numberseries, args.alldicoms)

    todmp = {}

    print("\n")
    if args.manufacturers:
        print("\nList of Manufacturers:  ", end='')
        print(list_manufacturers)
        todmp["list_manufacturers"] = list_manufacturers
        
    if args.bodyparts:
        print("\nList of Body Parts:  ", end='')
        print(list_bodyparts)
        todmp["list_bodyparts"] = list_bodyparts

    if args.numberseries:
        print("\nNumber of Series:  ",end='')
        print(len(list_series))
        todmp["list_series"] = list_series
    
    if f:
        json.dump(todmp,f,indent=2)
        f.close()

 