# COVID-19 Project

## About
In this repo, the impact of the COVID-19 spreading speed on unemployment claims for each state in the U.S. across various sectors is investigated using a difference-in-differences (DID) approach with state-specific time trend techniques. Data forecasting is performed using machine learning methods including linear regression and neural networks. We use panel data concerning the weekly unemployment claims and cumulative cases in each state since the inception of the coronavirus outbreak. This paper strives to investigate the causal effect of the spreading speed of COVID-19 in the U.S. on weekly unemployment claims in different states across sectors as well as forecast of unemployment insurance (UI) claims patterns. We hope the thesis will provide guidance on the implementation of Central Bank's economy revival policy. 

## Dependencies

This repository supports python 3.7. Install `pipenv` and create a virtual environment using `pipenv shell`. Run `pipenv install` to install all dependencies.

## Get Unemployment Insurance Data

First run `scrapy runspider get_states.py` to get a list of all the states, which will be stored in `states.txt`. Then run `python UI_scraper.py` to get all the weekly unemployment related information from the [Deparment of Labor](https://oui.doleta.gov/unemploy/claims.asp), which will be saved as a json named `UI.json`. 


## Get Weekly COVID-19 Cases Data

Run `python covid_cases_preprocess.py` to process daily US COVID-19 data by state to weekly data. The original data is found in the repo [here](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) in the csv file `time_series_covid19_confirmed_US.csv`.


## Get Monthly Industry Data

Run `python industry_scraper.py` to get monthly number of unemployment insurance claimants by industry. The information is collected from [Deparment of Labor](https://oui.doleta.gov/unemploy/chariu.asp), and will be stored as `industry.json` for months January to July.


## Get CSV Data

Run `python json_to_csv.py` to convert `UI.json` and `industry.json` to `UI.csv` and `industry.csv`, respectively.


## Get Preprocessed Data Input

Run the script `data_preprocess.py` to get the csv data input to the linear regression model, which is saved as `data.csv`. For test data on UI claims in July, run `test_data_preprocess.py`. For PanelOLS analysis, run the scripts `panelols_data_preprocess.py` to get the data in the desired panel data format. 