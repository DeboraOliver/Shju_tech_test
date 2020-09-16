#Shooju Technical Evaluation

The goal is to create a single python2/3 file that uses only standard libraries that:

    Uses only the URL https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip as input
    Downloads, unzips, parses based on that single URL input
    Writes to stdout a new line delimited (\n) JSON series-by-series representation of the input CSV

Each JSON series representation should be an object with 3 keys:

    series_id: some unique series id; it should be meaningful to the series it is identifying
    points: an array of date(time)/float arrays; the date(time) should be in ISO format as defined at https://en.wikipedia.org/wiki/ISO_8601
    fields: an object of any additional metadata available at the source that helps to describe and identify the data; a series representing Brazilian GDP might have two main keys: "country" and "concept" as in the example below


--------------------------------------------------

#Solution

##Libraries Required

import dload
import os, csv
import pandas as pd
import json


## Download, Unzip and Extract

The first part of the challenge required to download, unzip and extract a csv file from a given url. Although, there are a huge range of ways to do it, I used dload library due to its simplicity (one line code):

dload.save_unzip("https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip")

To locate the csv file, I used the os library to find the directory path and then I only had to write the csv's name:

dirpath = os.getcwd()
raw_data = dirpath + "\jodi_gas_csv_beta\jodi_gas_beta.csv"


## Defining an Id_series for each entry
###Renaming it as Id_series

##Organizing a json array for date

##





#Sources

https://gist.github.com/saluker/85c3edfe0b680a5325318aa9e80686b7
https://www.jodidata.org/gas/database/data-downloads-beta.aspx
https://www.jodidata.org/_resources/files/downloads/manuals/jodi-gas-manual.pdf
https://en.wikipedia.org/wiki/Time_series