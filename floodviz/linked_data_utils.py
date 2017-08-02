from datetime import date


class LinkedData:
    """
    Generates JSON-LD based on gages and the flood event.
    """
    def __init__(self):
        self.ld = self._blank_thing("WebSite")
        self.ld.update({
            "name": "Active flood visualization placeholder name",
            "datePublished": str(date.today()),
            "publisher": {
                "@context": "http://schema.org",
                "@type": "Organization",
                "name": "U.S. Geological Survey",
                "alternateName": "USGS"
            },
        })

        self.gages = []
        self.dates = {}
        self.location = []

    @staticmethod
    def _blank_thing(typename):
        """
        Make a blank thing of a type
        :param typename: Typename for the thing
        :return: Dict representing a blank thing
        """
        return {
            "@context": "http://schema.org",
            "@type": typename,
        }

    def _location_str(self):
        """
        Convert the bounding box for the event into a string.
        :return: String representing the bounding box for the event
        """
        l = "{},{} {},{}".format(self.location[0], self.location[1], self.location[2], self.location[3])
        return l

    def _assemble_event(self):
        """
        Wrap the data on the event into a dictionary
        :return: JSON-LD-like dict representing the event
        """
        event = self._blank_thing("Event")
        if self.location and self.dates:
            event.update({
                "@context": "http://schema.org",
                "@type": "Event",
                "name": "FLOOD EVENT NAME",
                "startDate": self.dates['start'],
                "endDate": self.dates['end'],
                "location": {
                    "@context": "http://schema.org",
                    "@type": "Place",
                    "address": "null",
                    "geo": {
                        "@context": "http://schema.org",
                        "@type": "GeoShape",
                        "box": self._location_str(),
                    },
                },
            })
        return event

    def _assemble_gage(self, gage):
        """
        Wrap an individual gage in a place
        :param gage: the gage to be wrapped
        :return: A dict representing the gage in json-ld format as a place
        """
        g = self._blank_thing('Place')
        geo = self._blank_thing('geoCoordinates')
        geo.update({
            "longitude": gage['dec_long_va'],
            "latitude": gage['dec_lat_va']
        })
        g.update({
            "address": "HUC:" + gage['huc_cd'],
            "name": gage['station_nm'],
            "branchCode": "SITE:"+gage['site_no'],
            "geo": geo,
            "additionalProperty": {
                "huc_cd": gage['huc_cd'],
                "site_no": gage['site_no']
            }
        })
        return g

    def _assemble_all_gages(self):
        """
        Wrap up all the gages as places
        :return: A list of dicts describing the gages
        """
        gages_ld = []
        if self.gages:
            for gage in self.gages:
                gages_ld.append(self._assemble_gage(gage))
        return gages_ld

    def set_page_name(self, name):
        self.ld['name'] = name

    def set_gages(self, gages):
        """
        Sets the gages to be used
        :param gages: list of dicts describing gages as output by `site_dict` in map_utils.
        :return: None
        """
        self.gages = gages

    def set_dates(self, start, end):
        """
        Sets the start and end dates of the flood event
        :param start: Start date
        :param end: End date
        :return: None
        """
        self.dates = {
            "start": start,
            "end": end
        }

    def set_location(self, bbox):
        """
        Sets the bounding box of the event
        :param bbox: array containing two pairs of coordinates
        :return: None
        """
        lon = [bbox[0], bbox[2]]
        lat = [bbox[1], bbox[3]]
        minlat = min(lat)
        maxlat = max(lat)
        minlon = min(lon)
        maxlon = max(lon)

        self.location = [minlat, minlon, maxlat, maxlon]

    def assemble(self):
        """
        Put together all data
        :return: return a JSON-LD-like dictionary
        """
        self.ld['about'] = self._assemble_event()
        self.ld['gages'] = []
        if self.gages:
            gages = self._assemble_all_gages()
            for g in gages:
                self.ld['gages'].append(g)

        return self.ld
