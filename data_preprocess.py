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
    headers.append("COVID_(s,t)")
    headers.extend(state_names)

    # From 01/25 to 05/30 there are 19 weeks
    # From 01/25 to 06/27 there are 23 weeks (train data)
    # from 06/27 to 08/01 there are 5 weeks (test data)
    for i in range(1, 29):
        headers.append(f"WEEK{i}")

    for state in state_names:
        headers.append(f"{state} x t")

    # name = "data/industry"
    # with open(f"{name}.json") as json_file: 
    #     data = json.load(json_file) 

    # header_keys = list(data[list(data.keys())[0]].keys()) # Industry types
    # for key in header_keys[1:]: # ignore Industry column
    #     if key.startswith("Industry"):
    #         break
    #     headers.append(key.split('_')[0])

    # Percentage data for unemployment claims by industry
    name = "data/industry_percentage"
    with open(f"{name}.json") as json_file: 
        data = json.load(json_file) 

    header_keys = list(data[list(data.keys())[0]].keys()) # Industry types
    for key in header_keys[1:]: # ignore Industry column
        if key.startswith("Industry"):
            break
        headers.append(key.split('_')[0] + ' %')  
    return headers


#####################################################################
################# LOAD CSV DATA TO FILE #############################
#####################################################################
headers = get_headers()
# print(headers)
result = []
test_data = []
# Start with UI claims
with open('data/UI.csv', newline='') as csvfile:
    UI_data = list(csv.reader(csvfile))

with open('data/US_new_weekly_cases.csv', newline='') as csvfile:
    cases_data = list(csv.reader(csvfile))

# with open('data/industry.csv', newline='') as csvfile:
#     sector_data = list(csv.reader(csvfile))

with open('data/industry_percentage.csv', newline='') as csvfile:
    sector_percentage_data = list(csv.reader(csvfile))

week_to_month_map = {"Jan": [1,2], "Feb": [3,4,5,6], "Mar": [7,8,9,10], "Apr": [11,12,13,14,15], "May": [16,17,18,19], "Jun": [20,21,22,23]}#, "Jul": [24,25,26,27,28]}

for state_data in UI_data[1:]: # ignore header
    # find corresponding row in cases_data
    for i, row in enumerate(cases_data):
        if row[0] == state_data[0]:
            cases_row = cases_data[i]
            break
    # for i, row in enumerate(sector_data):
    #     if row[0] == state_data[0]:
    #         sector_row = sector_data[i]
    #         break      
    for i, row in enumerate(sector_percentage_data):
        if row[0] == state_data[0]:
            sector_percentage_row = sector_percentage_data[i]
            break      
    for i, claim in enumerate(state_data[1:-5]): # ignore state and last 5 weeks (test data)
        result.append([])
        result[-1] = [0] * len(headers)
        result[-1][0] = int(claim) # get UI claim count
        state_idx = headers.index(state_data[0])
        result[-1][state_idx] = 1
        week_idx = headers.index("WEEK1")
        result[-1][week_idx+i] = 1
        state_week_idx = headers.index(f"{state_data[0]} x t")
        result[-1][state_week_idx] = i+1
        if i == 0: # first week
            result[-1][1] = 1 if int(cases_row[i+1]) > 0 else 0
        if i > 0: # check if # of cases is greater than last week
            if int(cases_row[i+1]) > int(cases_row[i]):
                result[-1][1] = 1
        for key in week_to_month_map.keys():
            if i+1 in week_to_month_map[key]:
                month = key
        # sector_header = sector_data[0]
        # for i, h in enumerate(sector_header):
        #     if h.endswith(month) and not h.startswith("Industry"):
        #         sector = h.split('_')[0]
        #         header_idx = headers.index(sector)
        #         if int(sector_row[i]) > 0:
        #             result[-1][header_idx] = 1
        sector_percentage_header = sector_percentage_data[0]
        for j, h in enumerate(sector_percentage_header):
            if h.endswith(month) and not h.startswith("Industry"):
                sector = h.split('_')[0]
                header_idx = headers.index(sector + ' %')
                result[-1][header_idx] = sector_percentage_row[j]

data_file = open(f"data/data.csv", 'w') 
csv_writer = csv.writer(data_file) 
csv_writer.writerow(headers) 

for row in result: 
    csv_writer.writerow(row)

data_file.close()