import json 
import csv 
  
def industry_json_to_csv():
    name = "data/Industry"
    with open(f"{name}.json") as json_file: 
        data = json.load(json_file) 
    
    header_keys = list(data[list(data.keys())[0]].keys()) # Industry types
    header_keys.insert(0, "State")
    
    data_file = open(f"{name}.csv", 'w') 
    csv_writer = csv.writer(data_file) 
    csv_writer.writerow(header_keys) 
    
    for key in data: 
        values = data[key].values()
        row = [key] # State
        for v in values:
            row.append(int(v.replace(',', ''))) # Remove , from 12,345 
        csv_writer.writerow(row)
    
    data_file.close() 


def industry_percentage_json_to_csv():
    name = "data/industry_percentage"
    with open(f"{name}.json") as json_file: 
        data = json.load(json_file) 
    
    header_keys = list(data[list(data.keys())[0]].keys()) # Industry types
    header_keys.insert(0, "State")
    
    data_file = open(f"{name}.csv", 'w') 
    csv_writer = csv.writer(data_file) 
    csv_writer.writerow(header_keys) 
    
    for key in data: 
        values = data[key].values()
        row = [key] # State
        for v in values:
            if v == "\u00a0":
                row.append(0)
            else:
                row.append(v[:-1])
        csv_writer.writerow(row)
    
    data_file.close() 


def UI_json_to_csv():
    name = "data/UI"
    with open(f"{name}.json") as json_file: 
        data = json.load(json_file) 
    
    dummy_state = list(data.keys())[0]
    dummy_records = data[dummy_state] # List of dictionaries
    header_keys = []
    for rec in dummy_records[3:-2]: # only get data from 01/25 to 05/30
        header_keys.append(rec["Filed Week Ended"])
    header_keys.insert(0, "State")
    
    data_file = open(f"{name}.csv", 'w') 
    csv_writer = csv.writer(data_file) 
    csv_writer.writerow(header_keys) 
    
    for key in data: 
        records = data[key]
        row = [key.strip()] # State
        for rec in records[3:-2]:
            row.append(int(rec["Initial Claims"].replace(',', '')))
        csv_writer.writerow(row)
    
    data_file.close() 


if __name__ == "__main__":
    industry_json_to_csv()
    industry_percentage_json_to_csv()
    UI_json_to_csv()