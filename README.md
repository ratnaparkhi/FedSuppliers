# FedSuppliers
To determine distinct suppliers from USA Federal spend data

1.	Approach to find distinct suppliers.
Python pandas and fuzzywuzzy packages are used to load the data in a data-frame and to perform fuzzy matching. After a brief review of records from 2016 contracts full file, few columns were identified for the determination of distinct suppliers. The determination of distinct suppliers is done using the following rules. First, duplicate rows are eliminated if DUNS numbers are same, then exact matching is performed on vendroname and vendoraddress. After that fuzzy matching using partial_ratio (for vendorname) and ratio (for vendoraddress) functions from fuzzywuzzy package is done. The vendoraddress is created by concatenation of streetaddress, city, state, zipcode, and vendorcountrycode. Current implementation uses a ratio of greater than 95 to determine a fuzzy match. Exact quantification of accuracy of matching needs to be done. However, ratio of 95 ensures high accuracy, and it may miss a match, but has less probability of reporting a false match. Hence false positives will be less likely. 
At present, distinct suppliers are found only from full contracts datasets for years 2010 thru 2016. However, the same logic can be easily extended to determine distinct grants of loans or other recipients of funds from Federal Government. 
Once distinct suppliers are determined, it can help us to perform supplier trend analysis and answer questions such as: (i) are number of suppliers increasing or decreasing? (ii) Is the increase or decrease following some macro-economic trend? (iii) Are suppliers owned by under-represented groups increasing or decreasing?  (iv) Who are top five suppliers? (v) Who are bottom five suppliers? 

2.	How to run the script?

      •	 To find distinct suppliers in 2016 contracts full file
  
      $  ./distinctSuppliers.py --YearVal=2016 >> results2016.txt 2>&1

      •	To find distinct suppliers by combining rows from 2010 thru 2016
  
      $ ./distinctSuppliers.py --YearVal=ALL >> resultsALL.txt 2>&1

      •	The shell script results.sh from GitHub Repo runs for every year (from 2010 thru 2016) and for ALL to produce the results listed in Summary of Findings below. Note: This script took 2 hours and 10 minutes on my MacBook Pro (2.9 GHz Intel Core i7, 8GB RAM).

      •	As the filenames are hardcoded in distinctSuppliers.py, few changes may be necessary to run it in a different environment. 

3.	Suggested improvements

      •	Use external sources to match short form (abbreviations) with long form of names. For example, to match GE with General Electric, an exhaustive list of company names and their abbreviations can be created (using external sources) and then used to do vendor name matching. In the current implementation this is addressed, to some extent, by vendoraddress matching. 

      •	Use fields such as phonenumber, womenowned, minorityowned, veteranowned and others to ensure more precise matching after a fuzzy match on other fields. 


4.	Summary of findings

YEAR 2016

Number of vendor records in contracts full file is: 4802211

Number of unique DUNS numbers in contracts full file is: 50394

Number of exact matching vendor names: 659

Number of exact matching vendor address: 59

Number of fuzzy matching vendor names: 489

Number of fuzzy matching vendor address: 10

Finally, number of distinct vendors found: 49177


YEAR 2015

Number of vendor records in contracts full file is: 4357218

Number of unique DUNS numbers in contracts full file is: 50290

Number of exact matching vendor names: 736

Number of exact matching vendor address: 32

Number of fuzzy matching vendor names: 455

Number of fuzzy matching vendor address: 23

Finally, number of distinct vendors found: 49044


YEAR 2014

Number of vendor records in contracts full file is: 2523974

Number of unique DUNS numbers in contracts full file is: 51841

Number of exact matching vendor names: 739

Number of exact matching vendor address: 40

Number of fuzzy matching vendor names: 543

Number of fuzzy matching vendor address: 19

Finally, number of distinct vendors found: 50500


YEAR 2013

Number of vendor records in contracts full file is: 2512486

Number of unique DUNS numbers in contracts full file is: 53632

Number of exact matching vendor names: 872

Number of exact matching vendor address: 56

Number of fuzzy matching vendor names: 597

Number of fuzzy matching vendor address: 29

Finally, number of distinct vendors found: 52078


YEAR 2012

Number of vendor records in contracts full file is: 3124491

Number of unique DUNS numbers in contracts full file is: 59679

Number of exact matching vendor names: 946

Number of exact matching vendor address: 53

Number of fuzzy matching vendor names: 732

Number of fuzzy matching vendor address: 24

Finally, number of distinct vendors found: 57924


YEAR 2011

Number of vendor records in contracts full file is: 3404589

Number of unique DUNS numbers in contracts full file is: 62939

Number of exact matching vendor names: 1073

Number of exact matching vendor address: 55

Number of fuzzy matching vendor names: 841

Number of fuzzy matching vendor address: 20

Finally, number of distinct vendors found: 60950

YEAR 2010

Number of vendor records in contracts full file is: 3541148

Number of unique DUNS numbers in contracts full file is: 66412

Number of exact matching vendor names: 1045

Number of exact matching vendor address: 50

Number of fuzzy matching vendor names: 919

Number of fuzzy matching vendor address: 11

Finally, number of distinct vendors found: 64387

YEAR ALL

Number of vendor records in contracts full file is: 24266117

Number of unique DUNS numbers in contracts full file is: 85462

Number of exact matching vendor names: 1209

Number of exact matching vendor address: 42

Number of fuzzy matching vendor names: 1172

Number of fuzzy matching vendor address: 36

Finally, number of distinct vendors found: 83003







