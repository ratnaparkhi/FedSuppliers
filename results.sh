#!/bin/sh 
date
echo "distinctSuppliers.py --YearVal=2016"
./distinctSuppliers.py --YearVal=2016 >> results2016.txt 2>&1
date
echo "distinctSuppliers.py --YearVal=2015"
./distinctSuppliers.py --YearVal=2015 >> results2015.txt 2>&1
date
echo "distinctSuppliers.py --YearVal=2014"
./distinctSuppliers.py --YearVal=2014 >> results2014.txt 2>&1
date
echo "distinctSuppliers.py --YearVal=2013"
./distinctSuppliers.py --YearVal=2013 >> results2013.txt 2>&1
date
echo "distinctSuppliers.py --YearVal=2012"
./distinctSuppliers.py --YearVal=2012 >> results2012.txt 2>&1
date
echo "distinctSuppliers.py --YearVal=2011"
./distinctSuppliers.py --YearVal=2011 >> results2011.txt 2>&1
date
echo "distinctSuppliers.py --YearVal=2010"
./distinctSuppliers.py --YearVal=2010 >> results2010.txt 2>&1
date
echo "distinctSuppliers.py --YearVal=ALL"
./distinctSuppliers.py --YearVal=ALL >> resultsALL.txt 2>&1
date
