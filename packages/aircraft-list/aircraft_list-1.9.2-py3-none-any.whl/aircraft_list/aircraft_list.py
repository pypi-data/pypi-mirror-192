import csv

def split_string(stringa):
    return stringa.split(',')

def aircraft_models():
    import pkg_resources
    data_file = pkg_resources.resource_filename(__name__, 'aircraft_model_list.csv')
    with open(data_file, 'r') as f:
        # reader = csv.reader(f, delimiter=';')
        # aircrafts = []
        # for row in reader:
        #     aircrafts.append(row)
        # data = [dict(zip(['manufacturer', 'model', 'icao', 'type', 'engine',
        #              'engine_number', 'wake'], split_string(sublist[0]))) for sublist in aircrafts]
        # return data
        reader = csv.reader(f, delimiter=';')
        aircrafts = []
        for row in reader:
            aircrafts.append(row)
        data = []
        for sublist in aircrafts:
            fields = split_string(sublist[0])
            data.append({
                'manufacturer': fields[0],
                'model': fields[1],
                'icao': fields[2],
                'type': fields[3],
                'engine': fields[4],
                'engine_number': fields[5],
                'wake': fields[6]
            })
        return data