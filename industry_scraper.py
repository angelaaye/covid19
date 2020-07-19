import json
import requests
from bs4 import BeautifulSoup


def get_weekly_state_data(state, url, result, month):
    response = requests.post(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())

    table = soup.find("table", id=f"{state.replace(' ', '_')}_Characteristics")
    # print(table)  
    
    data = {}
    rows = table.find_all("tr")
    found = False

    if state not in result:
        result[state] = {}

    for row in rows[2:]:
        industry = row.find("th")
        columns = row.find_all("td")
        if industry and industry.text == "Industry":
            found = True
        if found: 
            data[f"{industry.text}_{month}"] = columns[0].text
    result[state].update(data)


if __name__ == "__main__":
    with open("data/states.txt", "r") as f:
        states = f.read().splitlines()

    result = {}
    months = ["Jan", "Feb", "Mar", "Apr", "May"]
    for month in months:
        url = f'https://oui.doleta.gov/unemploy/content/chariu2020/2020{month}.html'
        
        for state in states:
            state = state.split(',')
            get_weekly_state_data(state[0].strip(), url, result, month) # Because Oklahoma has a space after it in states.txt

    with open("data/Industry.json", "w") as f:
        json.dump(result, f)