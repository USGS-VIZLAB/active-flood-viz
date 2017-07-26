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
        self.ld["about"] = self._assemble_event()
        return self.ld
