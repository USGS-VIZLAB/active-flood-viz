import re

from . import utils


def req_peak_data(site, end_date, url_prefix):

    # peak value historical data #
    params = {
        'agency_cd': 'USGS',
        'format': 'rdb',
        'site_no': site,
        'end_date': end_date
    }
    raw_peaks = utils.parse_rdb(url_prefix, params)
    if raw_peaks is None:
        print('rdb parser has returned no data to peakflow util req_peak_data')
        peaks = None

    else:
        keep_keys = [
            'peak_dt',
            'peak_va'
        ]
        peaks = []
        for raw in raw_peaks:
            peak = {k: raw[k] for k in keep_keys}
            peaks.append(peak)

    return peaks


def req_peak_dv_data(site, date, url_prefix):

    url_prefix += 'dv/'

    params = {
        'format': 'rdb',
        'siteStatus': 'all',
        'sites': site,
        'startDT': date,
        'endDT': date

    }
    content = utils.parse_rdb(url_prefix, params)
    if content is None:
        print('rdb parser has returned no data to peakflow util req_peak_dv_data')
        peaks = None

    else:
        # Find the name of that column whose name changes
        for k in content[0].keys():
            colname = re.match(r'\d+_00060_00003$', k)
            # if a match has been found
            if colname is not None:
                colname = colname.string
                break
        # (no break) means that this column has not been found
        else:
            # I'd rather base my guess on what the thing looks like than on where it is
            colname = content[0].keys()[3]

        keep_keys = [
            colname,
            'datetime'
        ]
        peaks = []
        for raw in content:
            peak = {k: raw[k] for k in keep_keys}
            # rename that weird column to 'discharge'
            peak['discharge'] = peak.pop(colname)
            peaks.append(peak)

    return peaks



def parse_peak_data(peak_data, dv_data):

    """ 
    Parses peak flow water data peak_data and constructs a dictionary 
    appropriately formated for D3 charting library. 

    ARGS: 
        peak_data - list of lines from peak flow data requested from NWIS waterdata service.
        dv_data - list of lines from daily value data requested from NWIS waterdata service.
    
    RETURNS:
        peak_data - A list holding the peak flow data points
        (each as a dict) for a specific site 
    """
    
    all_data = []
    seen = set()
    if peak_data:
        for peak in peak_data:
            # I am not worried about years that are not four digits long
            year = re.match(r'^(\d{4}).*', peak['peak_dt']).group(1)
            seen.add(year)

    if dv_data:    
        # parse daily_value data
        for line in dv_data:
            if not line.startswith('USGS'):
                continue
            line = line.split('\t')
            year = line[2].split('-')[0]
            # below conditon will favor the peak value retrieved from
            # peak value data opposed to daily value data if peak value data is available
            if year in seen:
                break
            if line[3]:
                peak_val = float(line[3])
                all_data.append({'label': year, 'value': peak_val})

    return all_data
