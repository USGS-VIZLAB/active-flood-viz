import json

with open('floodviz/static/reference/reference.json', 'r') as f:
    data = json.load(f)

    # print(data)
    epsg = data['target_epsg'][5:]
    site_ids = data['site_ids']
    display_sites = data['display_sites']
    bbox = data['bbox']
    start_date = data['startDate']
    end_date = data['endDate']
    peak_dv_date = data['endDate']
    peak_site = data['peak']['site']
    # peak_start_date = data['peak']['startDate']
    # peak_end_date = data['peak']['endDate']
    # print(data['reference']['features'][0])
    reference_data = []
    for i in range(0, len(data['reference']['features'])):
        if data['reference']['features'][i]['properties']['reftype'] == 'city':
            reference_data.append(data['reference']['features'][i])


    # with open('instance/config.py', 'a') as config:
    #     config.write('SITE_IDS = ' + str(site_ids) + '\n' + '\n')
    #     config.write('HYDRO_DISPLAY_IDS = ' + str(display_sites) + '\n' + '\n')
    #     config.write('EVENT_START_DT = ' + '\'' + start_date + '\'' + '\n' + '\n')
    #     config.write('EVENT_END_DT = ' + '\'' + end_date + '\'' + '\n' + '\n')
    #     config.write('PROJECTION_EPSG_CODE = ' + '\'' + epsg + '\'' + '\n' + '\n')
    #     config.write('BOUNDING_BOX = ' + str(bbox) + '\n' + '\n')
    #     config.write('PEAK_SITE = ' + '\'' + peak_site + '\'' + '\n' + '\n')
    #     config.write('PEAK_DV_DT = ' + '\'' + end_date + '\'' + '\n' + '\n')
    #     config.write('REFERENCE_DATA = { \"type\": \"FeatureCollection\",' + '\n' + '\"features\": ' + str(
    #         reference_data) + '} \n')


        # for i in range(0, len(data['reference']['features'])):
        #     if data['reference']['features'][i]['properties']['reftype'] == 'city':
        #         print(data['reference']['features'][i])
        #     if data['reference']['features'][i]['properties']['reftype'] == 'city':
        #         print('city')
        #     if data['reference']['features'][i]['properties']['reftype'] == 'politicalBoundaries':
        #         print('border')