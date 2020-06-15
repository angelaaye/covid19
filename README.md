# COVID-19 Project

## Dependencies

Make sure you have python 3.7 installed. Run `pipenv install` to install all dependencies.

## Get Unemployment Insurance Data

First run `scrapy runspider get_states.py` to get a list of all the states, which will be stored in `states.txt`. Then run `python scraper.py` to get all the weekly unemployment related information from the [Deparment of Labor](https://oui.doleta.gov/unemploy/wkclaims/report.asp), which will be saved as a json named `UI.json`. 


