import csv

def split_string():
    return ['manufacturer', 'model', 'icao', 'type', 'engine', 'engine_number', 'wake']

def aircraft_models():
    with open('aircraft_list/aircraft_model_list.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        aircrafts = []
        for row in reader:
            aircrafts.append(row)
        data = [dict(zip(split_string(), sublist)) for sublist in aircrafts]
        return data

