#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# -*- coding: utf-8 -*-
# Python script to identify distinct suppliers (vendors) in USA spend database
# ​https://www.usaspending.gov/DownloadCenter/Pages/dataarchives.aspx
# The above site has data for Contracts, Grants, Loans and Other Financial
# Assistance. This script focuses on Full Contracts dataset from years
# 2010 thru 2016. Contracts datasets are the largest among the four - Contracts,
# Grants, Loans and Other Financial Assistance. 
#
# The script:
# (i) produces summary of NULL values for selected columns and
# (ii) prints its findings
# (iii) Creates 3 files with specified year of ALL in the name.
# These 3 files contain distinct DUNS in first, sorted vendor names in second
# and two columngs with matching info in the third file.
# 
import sys
import getopt
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

# Most places, vendoralternatename, vendorlegalorganizationname, vendordoingbusinessas
# streetaddress2, streetaddress3, vendor_cd are Null. So they will not be
# used in fuzzy matching.
# After a brief review of the Contracts dataset, the following columns were
# identified to determine distinct suppliers.
#
selCols = ["vendorname", "streetaddress", "city", "state", "zipcode",
           "vendorcountrycode", "dunsnumber",
           "womenownedflag", "veteranownedflag", "minorityownedbusinessflag"]

def compareRecords(rec1, rec2):
    # rec1 and rec2 are lists with following format
    # ['vendorname', 'vendoraddress']
    # vendoraddress = 'streetaddress + city + state + zipcode + vendorcountrycode'
    # 
    # compare the fields in the two records, and return True if rec2 and rec1
    # represent the same vendor.
    # Comparison is done using the following rules.
    # If there is an exact match in vendorname, then same vendor.
    # If there is an exact match in vendoraddress then same vendor.
    # Perfrom fuzzy match on vendorname, and decide based on the score.
    # Perform fuzzy match on vendoraddress and decide based on score.

    if (rec1[0] != 'UNKNOWN' and rec2[0] != 'UNKNOWN'):
        if (rec1[0] == rec2[0]): # Exact match on VENDORNAME
            return 'VENDORNAME_EXACT'
        
    if (len(rec1[1]) != 0 and len(rec2[1]) != 0):
        if (rec1[1] == rec2[1]): # Exact match on Vendor Address
            return 'VENDORADDRESS_EXACT'
      
    # vendornames may or may not have common parts like LLC, Inc, Corp
    # In order to avoild low fuzzy match score due to inconsistent presence
    # of these these terms, use partial_ratio when matching vendorname.
    # partial_ratio is based on best matching substring.
    
    if (rec1[0] != 'UNKNOWN' and rec2[0] != 'UNKNOWN'):
        if (fuzz.partial_ratio(rec1[0], rec2[0]) > 95):
            return 'VENDORNAME_FUZZY'

    # In cae of vendoraddress, ratio (instead of partial_ratio) is used to
    # perform fuzzy match. ratio uses the complete strings to match. This is
    # done to avoid, best mathcing of substring of state code+zip and or town

    if (len(rec1[1]) != 0 and len(rec2[1]) != 0):
        if (fuzz.partial_ratio(rec1[1], rec2[1]) > 95):
            return 'VENDORADDRESS_FUZZY'
   
    return 'NO_MATCH'


def usage(argv):
    print("""
Usage: """ + argv[0] + """ --YearVal=val

YearVal can be:
<any one of 2010, 2011, 2012, 2013, 2014, 2015, 2016 or ALL>
ALL means find distinct suppliers after combining rows from years 2010 thru 2016
  """)


def main(argv):
    if (len(argv) == 1): # Display usage and exit.
        usage(argv)
        return 2
    validVals = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', 'ALL']
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["YearVal="])
    except getopt.GetoptError:
        usage(argv)
        return 2
    
    if len(opts) == 0:
        usage(argv)
        return 2
    # Process arguments. 
    for opt, arg in opts:
        if opt != "--YearVal":
            usage(argv)
            return 2
        
        if opt == "--YearVal":
            if (arg not in validVals):
                usage(argv)
                return 2
            year = str(arg) # Set year val for further procerssing.
            
    fnamePrefix = '/Users/prashantratnaparkhi/tamr/{0}'.format(year)
    if year == 'ALL': # Read all data from 2010 thru 2016 and combine.
        df10 = pd.read_csv('/Users/prashantratnaparkhi/tamr/2010_All_Contracts_Full_20170315.csv',usecols = selCols, dtype='unicode')
        df11 = pd.read_csv('/Users/prashantratnaparkhi/tamr/2011_All_Contracts_Full_20170315.csv',usecols = selCols, dtype='unicode')
        df12 = pd.read_csv('/Users/prashantratnaparkhi/tamr/2012_All_Contracts_Full_20170315.csv',usecols = selCols, dtype='unicode')
        df13 = pd.read_csv('/Users/prashantratnaparkhi/tamr/2013_All_Contracts_Full_20170315.csv',usecols = selCols, dtype='unicode')
        df14 = pd.read_csv('/Users/prashantratnaparkhi/tamr/2014_All_Contracts_Full_20170315.csv',usecols = selCols, dtype='unicode')
        df15 = pd.read_csv('/Users/prashantratnaparkhi/tamr/2015_All_Contracts_Full_20170315.csv',usecols = selCols, dtype='unicode')
        df16 = pd.read_csv('/Users/prashantratnaparkhi/tamr/2016_All_Contracts_Full_20170315.csv',usecols = selCols, dtype='unicode')
        
        dfList = [df10, df11, df12, df13, df14, df15, df16]
        dataFSelCols = pd.concat(dfList)              
    else:
        fnameSuffix = '_All_Contracts_Full_20170315.csv'
        inpFile = fnamePrefix + fnameSuffix
        dataFSelCols = pd.read_csv(inpFile, usecols = selCols, dtype='unicode')


    ## Use the following 3 file names to write output
    opF1 = fnamePrefix+'SelVN-UnqDUNS.csv'
    opF2 = fnamePrefix+'SelVN-Sorted.csv'
    opF3 = fnamePrefix+'SelVN-Matched.csv'
    
    ## Select all vendors with unique DUNS number
    dfSelVN=dataFSelCols.drop_duplicates('dunsnumber', keep=False)
    dfSelVN.to_csv(opF1)

    srtVN = dfSelVN.sort_values(by=('vendorname'), ascending=True)
    srtVN.to_csv(opF2)


    # Let us focus on using vendorname, address and perform fuzzy matching using vendorname
    # and vendoraddress. Unque DUNS numbers are already matched. 
    print('Column Name                COUNT(NULL)')
    print(pd.isnull(srtVN).sum())  ## Shows col name & number of null values.

    ## Add two columns to the sorted dataframe
    srtVN['matches']= "NO_MATCH" ## Set to no match initially.
    # This will be set to the vendorname with which it matches. 
    srtVN['matchcategory']= "NONE" ## Set to NONE initially.
    # This will set to one of the following
    # 'VENDORNAME_EXACT', 'VENDORADDRESS_EXACT', ''VENDORNAME_FUZZY', or
    # 'VENDORADDRESS_FUZZY'

    # streetaddress, city, state, zipcode, vendorcountrycode are NULL at relatively
    # few places. If NULL, then set the value to "".

    srtVN.streetaddress.fillna("", inplace=True)
    srtVN.city.fillna("", inplace=True)
    srtVN.state.fillna("", inplace=True)
    srtVN.zipcode.fillna("", inplace=True)
    srtVN.vendorcountrycode.fillna("", inplace=True)

    #vendorname is NULL at few places, set it to "UNKNOWN".
    srtVN.vendorname.fillna("UNKNOWN", inplace=True)

    numRows = len(srtVN.index)

    rowsToCheck = 10 ## as the dataframe is sorted compare with only next 10 rows.
    for i in xrange(0, numRows):
        if srtVN.iloc[i, 10] == 'NO_MATCH':
            ## Still not a match with any other
            for k in xrange(1, rowsToCheck+1):
                j = i+k
                if (j < numRows):
                    if srtVN.iloc[j, 10] == 'NO_MATCH':
                        ## Still not a match with any other                   
                        rl1 = []
                        rl2 = []        
                        r1 = "".join(str(v) for v in list(srtVN.iloc[i, 1:5]))
                        r2 = "".join(str(v) for v in list(srtVN.iloc[j, 1:5]))
                        rl1.append(str(srtVN.iloc[i, 0]))
                        rl2.append(str(srtVN.iloc[j, 0]))
                        rl1.append(r1)
                        rl2.append(r2)
                        #rl1.append(str(srtVN.iloc[i, 6]))
                        #rl2.append(str(srtVN.iloc[j, 6]))
                        comparison = compareRecords(rl1, rl2)
                        if (comparison == 'VENDORNAME_EXACT'):
                            srtVN.iloc[j, 10] = srtVN.iloc[i, 0]
                            srtVN.iloc[j, 11] = 'VENDORNAME_EXACT'
                        if (comparison == 'VENDORADDRESS_EXACT'):
                            srtVN.iloc[j, 10] = srtVN.iloc[i, 0]
                            srtVN.iloc[j, 11] = 'VENDORADDRESS_EXACT'
                        if (comparison == 'VENDORNAME_FUZZY'):
                            srtVN.iloc[j, 10] = srtVN.iloc[i, 0]
                            srtVN.iloc[j, 11] = 'VENDORNAME_FUZZY'
                        if (comparison == 'VENDORADDRESS_FUZZY'):
                            srtVN.iloc[j, 10] = srtVN.iloc[i, 0]
                            srtVN.iloc[j, 11] = 'VENDORADDRESS_FUZZY'

    # Write to file after adding matches and matchescategory columns
    srtVN.to_csv(opF3)

    # Print the results.

    unm = srtVN[srtVN.matches == 'NO_MATCH']
    vem = srtVN[srtVN.matchcategory == 'VENDORNAME_EXACT']
    addrem = srtVN[srtVN.matchcategory == 'VENDORADDRESS_EXACT']
    addrfz = srtVN[srtVN.matchcategory == 'VENDORADDRESS_FUZZY']
    vnmfz = srtVN[srtVN.matchcategory == 'VENDORNAME_FUZZY']

    print('*** Now printing the findings ***')
    print('YEAR {0}'.format(year))
    print('Number of vendor records in contracts full file is: {0}'.format(len(dataFSelCols.index)))
    print('Number of unique DUNS numbers in contracts full file is: {0}'.format(numRows))
    print('Number of exact matching vendor names: {0}'.format(len(vem.index)))
    print('Number of exact matching vendor address: {0}'.format(len(addrem.index)))
    print('Number of fuzzy matching vendor names: {0}'.format(len(vnmfz.index)))
    print('Number of fuzzy matching vendor address: {0}'.format(len(addrfz.index)))
    print('Finally, number of distinct vendors found: {0}'.format(len(unm.index)))

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))


