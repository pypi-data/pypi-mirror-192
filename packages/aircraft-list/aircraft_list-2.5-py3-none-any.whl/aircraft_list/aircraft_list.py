def aircraft_models():
    import csv
    import pkg_resources
    data_file = pkg_resources.resource_filename(
        __name__, 'aircraft_model_list.csv')
    data = []
    with open(data_file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for i, row in enumerate(reader):
            row_dict = {}
            for r in row:
                row_dict['manufacturer'] = r.split(',')[0]
                row_dict['model'] = r.split(',')[1]
                row_dict['icao'] = r.split(',')[2]
                row_dict['type'] = r.split(',')[3]
                row_dict['engine'] = r.split(',')[4]
                row_dict['engine_number'] = r.split(',')[5]
                row_dict['wake'] = r.split(',')[6]
                row_dict['id'] = i
                data.append(row_dict)
        data.pop(0)
        return data