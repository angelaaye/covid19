"""
Take daily US COVID-19 cases data by county and process it to be a weekly-based data by state.
Output US_total_weekly_cases.csv:
State, Total cases by end of first week, Total cases by end of second week,  ...

Output US_new_weekly_cases.csv:
State, New cases by end of first week, New cases by end of second week, ...

Since the unemployment claims data is also weekly and each week ends on a Saturday, we will follow the same format here.
Therefore, we will save the data by 01/25, 02/01, 02/08, ... since the data starts from 01/22.
"""

import csv
from collections import defaultdict

with open("states.txt", "r") as f:
    states = f.read().splitlines()

state_names = set()
for state in states:
    state_names.add(state.split(',')[0].strip()) # Because Oklahoma has a space after it in states.txt

total_data = {}
new_data = {}
with open('US_daily_cases.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        curr_state = row['Province_State']
        if curr_state in state_names:
            if curr_state not in total_data:
                total_data[curr_state] = defaultdict(int)
                new_data[curr_state] = defaultdict(int)
            days = 0
            prev_week = 0
            for key in row.keys():
                if not key.endswith('20'): # not daily cases
                    continue
                days += 1
                if key.startswith('1/25') or days == 7:
                    total_data[curr_state][key] += int(row[key])
                    new_data[curr_state][key] += (int(row[key]) - prev_week)
                    days = 0
                    prev_week = int(row[key])

dummy_state = list(total_data.keys())[0]
fields = [week for week in total_data[dummy_state]]
fields.insert(0, "State")

with open("US_total_weekly_cases.csv", "w") as f:
    w = csv.DictWriter(f, fields)
    w.writeheader()
    for key, val in total_data.items():
        row = {'State': key}
        row.update(val)
        w.writerow(row)

with open("US_new_weekly_cases.csv", "w") as f:
    w = csv.DictWriter(f, fields)
    w.writeheader()
    for key, val in new_data.items():
        row = {'State': key}
        row.update(val)
        w.writerow(row)