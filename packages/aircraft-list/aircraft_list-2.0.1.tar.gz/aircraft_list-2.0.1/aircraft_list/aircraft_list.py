import csv


def split_string(stringa):
    return stringa.split(',')


def aircraft_models():
    import pkg_resources
    data_file = pkg_resources.resource_filename(
        __name__, 'aircraft_model_list.csv')
    data = []
    with open(data_file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            row_dict = {}
            if len(row) >= 7:
                row_dict['manufacturer'] = row[0]
                row_dict['model'] = row[1]
                row_dict['icao'] = row[2]
                row_dict['type'] = row[3]
                row_dict['engine'] = row[4]
                row_dict['engine_number'] = row[5]
                row_dict['wake'] = row[6]
                data.append(row_dict)
        data.pop(0)
        return data