import csv
import json


with open("data/states.txt", "r") as f:
    states = f.read().splitlines()

state_names = []
for state in states:
    state_names.append(state.split(',')[0].strip())

#####################################################################
################# GET HEADERS FOR CSV FILE ##########################
#####################################################################
def get_headers():
    headers = []
    headers.append("Y_(s,t)")
    headers.append("State")
    headers.append("Week")
    headers.append("COVID_(s,t)")
    headers.append("State_i x t")

    # Percentage data for unemployment claims by industry
    name = "data/industry_percentage"
    with open(f"{name}.json") as json_file: 
        data = json.load(json_file) 

    header_keys = list(data[list(data.keys())[0]].keys()) # Industry types
    for key in header_keys[1:]: # ignore Industry column
        if key.startswith("Industry"):
            break
        headers.append(key.split('_')[0] + ' %')    

    # Actual data for unemployment claims by industry
    name = "data/industry"
    with open(f"{name}.json") as json_file: 
        data = json.load(json_file) 

    header_keys = list(data[list(data.keys())[0]].keys()) # Industry types
    for key in header_keys[1:]: # ignore Industry column
        if key.startswith("Industry"):
            break
        headers.append(key.split('_')[0])

    return headers


#####################################################################
################# LOAD CSV DATA TO FILE #############################
#####################################################################
headers = get_headers()
print(headers)
result = []
test_data = []
# Start with UI claims
with open('data/UI.csv', newline='') as csvfile:
    UI_data = list(csv.reader(csvfile))

with open('data/US_new_weekly_cases.csv', newline='') as csvfile:
    cases_data = list(csv.reader(csvfile))

with open('data/industry.csv', newline='') as csvfile:
    sector_data = list(csv.reader(csvfile))

with open('data/industry_percentage.csv', newline='') as csvfile:
    sector_percentage_data = list(csv.reader(csvfile))

week_to_month_map = {"Jan": [1,2], "Feb": [3,4,5,6], "Mar": [7,8,9,10], "Apr": [11,12,13,14,15], "May": [16,17,18,19], "Jun": [20,21,22,23], "Jul": [24,25,26,27,28]}

for state_data in UI_data[1:]: # ignore header
    # find corresponding row in cases_data
    for i, row in enumerate(cases_data):
        if row[0] == state_data[0]:
            cases_row = cases_data[i]
            break
    for i, row in enumerate(sector_data):
        if row[0] == state_data[0]:
            sector_row = sector_data[i]
            break
    for i, row in enumerate(sector_percentage_data):
        if row[0] == state_data[0]:
            sector_percentage_row = sector_percentage_data[i]
            break           
    for i, claim in enumerate(state_data[1:]): # ignore state
        result.append([])
        result[-1] = [0] * len(headers)
        result[-1][0] = int(claim) # get UI claim count
        result[-1][1] = state_data[0] # State name
        result[-1][2] = i+1 # week index from 1 to 19
        result[-1][3] = cases_row[i+1] # COVID19_(s,t)
        result[-1][4] = i+1 # state_i x t from 1 to 19

        for key in week_to_month_map.keys():
            if i+1 in week_to_month_map[key]:
                month = key
        
        sector_percentage_header = sector_percentage_data[0]
        for j, h in enumerate(sector_percentage_header):
            if h.endswith(month) and not h.startswith("Industry"):
                sector = h.split('_')[0]
                header_idx = headers.index(sector + ' %')
                result[-1][header_idx] = sector_percentage_row[j]

        sector_header = sector_data[0]
        for j, h in enumerate(sector_header):
            if h.endswith(month) and not h.startswith("Industry"):
                sector = h.split('_')[0]
                header_idx = headers.index(sector)
                result[-1][header_idx] = sector_row[j]

        if 24 <= i+1 <= 28:
            test_data.append(result.pop())

data_file = open(f"data/panelols_data.csv", 'w') 
csv_writer = csv.writer(data_file) 
csv_writer.writerow(headers) 

for row in result: 
    csv_writer.writerow(row)

data_file.close() 

data_file = open(f"data/panelols_test_data.csv", 'w') 
csv_writer = csv.writer(data_file) 
csv_writer.writerow(headers) 

for row in test_data: 
    csv_writer.writerow(row)

data_file.close()