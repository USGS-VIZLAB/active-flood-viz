import re

from . import utils


def req_peak_data(site, end_date, url_prefix):
    """
    Call
    :param site: Site number on which to get peakflow data
    :param end_date: Date up to which data should be fetched
    :param url_prefix: NWIS endpoint prefix
    :return: List of dictionaries containing the date and values of peak streamflow for each water year.
    """
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
    """
    Get peak streamflow for a particular day from the daily values service
    :param site: Site number on which to get data
    :param date: Date for which to get the peak flow
    :param url_prefix: NWIS service endpoint
    :return: List of dictionaries containing the date and value of peak streamflow
    """
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
    Combine the peakflow information from the annual and daily values into a single list of dictionaries
    describing yearly peak streamflow.
    :param peak_data: Data from the NWIS peak flow service
    :param dv_data: Data from the NWIS daily values service
    :return: Data from peak flow service and daily value service combined into a single list.
    """
    all_data = []
    seen = set()
    if peak_data:
        for point in peak_data:
            # I am not worried about years that are not four digits long
            year = re.match(r'^(\d{4}).*', point['peak_dt']).group(1)
            if year not in seen:
                all_data.append({
                    'label': year,
                    'value': int(point['peak_va'])
                })
                seen.add(year)
            # If we have multiple points for a single cal. year, select the highest peak.
            elif all_data[-1]['label'] == year:
                later_val = int(point['peak_va'])
                if later_val > all_data[-1]['value']:
                    all_data[-1]['value'] = later_val

    if dv_data:
        for point in dv_data:
            year = re.match(r'^(\d{4}).*', point['datetime']).group(1)
            # below condition will favor the peak value retrieved from
            # peak value data opposed to daily value data if peak value data is available
            if year not in seen:
                all_data.append({
                    'label': year,
                    'value': int(point['discharge'])
                })

    return all_data
