# COVID-19 Project

## Dependencies

This repository supports python 3.7. Install `pipenv` and create a virtual environment using `pipenv shell`. Run `pipenv install` to install all dependencies.

## Get Unemployment Insurance Data

First run `scrapy runspider get_states.py` to get a list of all the states, which will be stored in `states.txt`. Then run `python UI_scraper.py` to get all the weekly unemployment related information from the [Deparment of Labor](https://oui.doleta.gov/unemploy/claims.asp), which will be saved as a json named `UI.json`. 


## Get Weekly COVID-19 Cases Data

Run `python covid_cases_preprocess.py` to process daily US COVID-19 data by state to weekly data. The original data is found in the repo [here](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series).


## Get Monthly Industry Data

Run `python industry_scraper.py` to get monthly number of unemployment insurance claimants by industry. The information is collected from [Deparment of Labor](https://oui.doleta.gov/unemploy/chariu.asp), and will be stored as `Industry.json` for months January to May.


## Get CSV Data

Run `python json_to_csv.py` to convert `UI.json` and `Industry.json` to `UI.csv` and `Industry.csv`, respectively.


## Get Preprocessed Data Input

Run `python data_preprocess.py` to get the csv data input to the linear regression model, which is saved as `data.csv`.