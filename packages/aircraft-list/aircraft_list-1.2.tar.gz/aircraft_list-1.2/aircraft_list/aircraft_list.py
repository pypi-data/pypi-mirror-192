import csv

def split_string(stringa):
    return stringa.split(',')

def aircraft_models():
    with open('aircraft_model_list.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        aircrafts = []
        for row in reader:
            aircrafts.append(row)
        print(aircrafts)
        data = [dict(zip(['manufacturer', 'model', 'icao', 'type', 'engine',
                     'engine_number', 'wake'], split_string(sublist[0] for sublist in aircrafts)))]
        return data

