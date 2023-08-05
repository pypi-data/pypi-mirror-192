import csv

def split_string(stringa):
    return stringa.split(',')

def aircraft_models():
    import pkg_resources
    data_file = pkg_resources.resource_filename(__name__, 'aircraft_model_list.csv')
    with open(data_file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        aircrafts = []
        for row in reader:
            aircrafts.append(row)
        data = [dict(zip(['manufacturer', 'model', 'icao', 'type', 'engine',
                     'engine_number', 'wake'], split_string(sublist[0]))) for sublist in aircrafts]
        return data


