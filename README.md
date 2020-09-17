# Shooju Technical Evaluation

The goal is to create a single python2/3 file that uses only standard libraries that:

Uses only the URL https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip as input
Downloads, unzips, parses based on that single URL input
Writes to stdout a new line delimited (\n) JSON series-by-series representation of the input CSV

Each JSON series representation should be an object with 3 keys:
<ol>
<li>series_id: some unique series id; it should be meaningful to the series it is identifying</li>
<li>points: an array of date(time)/float arrays; the date(time) should be in ISO format as defined at https://en.wikipedia.org/wiki/ISO_8601.</li>
<li>fields: an object of any additional metadata available at the source that helps to describe and identify the data; a series representing Brazilian GDP might have two main keys: "country" and "concept" as in the example below</li>
</ol>


--------------------------------------------------

# Solution

## Libraries Required
<ul>
    <li>import dload</li>
    <li>import os</li>
    <li>import pandas as pd</li>
</ul>

## Download, Unzip and Extract

The first part of the challenge requires to download, unzip, and extract a csv file from a given url. Although there is a few ways to do it, I used dload library due to its simplicity (one line code):

    dload.save_unzip("https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip")

To locate the csv file, I used the os library to find the directory path and then I only had to write the csv's name:

    dirpath = os.getcwd()
    raw_data = dirpath + "\jodi_gas_csv_beta\jodi_gas_beta.csv"


## Defining a series_id for each entry

First of all, we use pandas to open the csv file and to add its information in a dataframe:

    df = pd.read_csv(raw_data)

Then, we define a new column called 'series_id' and concatenate a few information to enable us to easily identify where data comes from. 

    df['series_id'] = df['REF_AREA'] + '-' + df['ENERGY_PRODUCT'] + '-' +  df['FLOW_BREAKDOWN']  + '-' +  df['UNIT_MEASURE'].map(str)

It seemed that looking to Ref_area, energy_product, flow_ breakdown, and unit measure, I could be able to identify the series. So, that sequence was used to produce unique keys.

## Organizing a json array for date

The second task was to have an array of date(time). In this case, the array was constituted of date and assessment_code <em>(could it have more than an assessment per day?)</em>.

    df = df.assign(points = df[['TIME_PERIOD', 'ASSESSMENT_CODE']].values.tolist())

A new column called <em>points</em> was used.

## Cleanse

As the task itself asks to use only three keys, there is no reason to retain non-useful columns. 

    df = pd.DataFrame(df, columns = ['series_id', 'points','field_obs_value'])

The field_obs_value is an additional information. It was renamed from OBS_value: 

    df = df.rename(columns = {'OBS_VALUE':'field_obs_value'})  

## The newline-delimited Json

 A ndJSON is a collection of JSON objects, separated by `\n`. Thus, it is nothing else than one valid JSON object per line! There are a few ways to generate something like it: I could either use a library named jsonline, or I could only modify my json to get each entry line-by-line. I chose the second for three main reasons: 
 
<ol>
<li>I wanted to keep my script short;</li>
<li>It could have the same result using fewer libraries <em>(I didn't want to install a new library)</em>; and </li>
<li>I thought it was quite exciting to write a json without adopting a specific json library.</li>
</ol>

    df.to_json('JsonResult.json', orient = 'records', lines = True)

From the documentation of to_json:<em> "If ‘orient’ is ‘records’ write out line delimited json format. Will throw ValueError if incorrect ‘orient’ since others are not list like."</em>

There are many ways to get the same result in Python.


#Sources

https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html
https://gist.github.com/saluker/85c3edfe0b680a5325318aa9e80686b7
https://www.jodidata.org/gas/database/data-downloads-beta.aspx
https://www.jodidata.org/_resources/files/downloads/manuals/jodi-gas-manual.pdf
https://en.wikipedia.org/wiki/Time_series
