from datetime import date


class LinkedData:
    def __init__(self):
        self.ld = self._blank_thing("WebSite")
        self.ld.update({
            "name": "Active flood visualization",
            "about": "Visualization of a flood event based on USGS streamgage readings",
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
        return {
            "@context": "http://schema.org",
            "@type": typename,
        }

    def _location_str(self):
        l = "{},{} {},{}".format(self.location[0], self.location[1], self.location[2], self.location[3])
        return l

    def _assemble_event(self):
        event = self._blank_thing("Event")
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
        g = self._blank_thing('Place')
        g.update({
            "address": "HUC:" + gage['huc_cd'],
            "name": gage['station_nm'],
            "branchCode": "SITE:"+gage['site_no'],
            "geo": {
                self._blank_thing('geoCoordinates').update({
                    "longitude": gage['dec_long_va'],
                    "latitude": gage['dec_lat_va']

                })
            },
            "additionalProperty": {
                "huc_cd": gage.huc_cd,
                "site_no": gage.site_no
            }
        })
        return g

    def _assemble_all_gages(self):
        gages_ld = []
        for gage in self.gages:
            gages_ld.append(self._assemble_gage(gage))

        return gages_ld

    def set_gages(self, gages):
        self.gages = gages

    def set_dates(self, start, end):
        self.dates = {
            "start": start,
            "end": end
        }

    def set_location(self, bbox):
        lon = [bbox[0], bbox[2]]
        lat = [bbox[1], bbox[3]]
        minlat = min(lat)
        maxlat = max(lat)
        minlon = min(lon)
        maxlon = max(lon)

        self.location = [minlat, minlon, maxlat, maxlon]
        str(self.location)

    def assemble(self):
        self.ld['about'] = self._assemble_event()
        self.ld['about'].update({

        })
        return self.ld
