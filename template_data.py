# Parsing the latest.xml data into the format that the paper recommaned
# Delling, D., Pajor, T., Werneck, R.F., n.d. Round-Based Public Transit Routing.

import json

import xml.etree.ElementTree as ET


def timeparser(time: str | None):
    # example 23:04
    if time is not None:
        times = [int(i) for i in time.split(":")]
        return (times[0] * 60 + times[1]) * 60
    else:
        return None


# OR: Origin Location
# IP: Passenger Calling point
# DT: Passenger Destination Calling point
# OPIP: Intermediate operational calling location
tag_include_journey = ["OR", "IP", "DT"]

stationfile = open("data_parsing/stations.json", "r")
stations = json.load(stationfile)["stations"]

tocfile = open("data_parsing/tocs.json", "r")
toc_code = json.load(tocfile)["tocs"]

tiplocs_file = open("pushport/stations_tiplocs.json")
tiplocs = json.load(tiplocs_file)


tree = ET.parse("latest.xml")
root = tree.getroot()


# data initalised for it
stops = {}  # "Tiploc": {"CrsCode": string, "Name": string ...}
routes = {}
routes_existed = []
trips = {}
trip_id = 0
route_id = 0
# round_id = 0
period_of_operation = 86400


def find_route_id(route_f):
    for id, route in routes.items():
        if route["route"] == route_f:
            return id


for journey in root:
    if "toc" in journey.attrib:
        toc_code_journey = journey.attrib["toc"]
        # only include Northern Train
        if toc_code_journey != "":
            route = []
            trip = []
            for passby in journey:
                passby_tag_name = passby.tag.replace(
                    "{http://www.thalesgroup.com/rtti/XmlTimetable/v8}", ""
                )
                if passby_tag_name in tag_include_journey:
                    # print(passby.attrib)
                    tpl = passby.attrib["tpl"]
                    if "wta" in passby.attrib:
                        arrival = passby.attrib[
                            "wta"
                        ]  # working scheduled time of departure
                    else:
                        arrival = None

                    if "wtd" in passby.attrib:
                        departure = passby.attrib[
                            "wtd"
                        ]  # working scheduled time of departure
                    else:
                        departure = None

                    if tpl in tiplocs and tpl not in stops:
                        stops[tpl] = tiplocs[tpl]
                        route.append(tpl)
                        trip.append(
                            {
                                "tiploc": tpl,
                                "arrival": timeparser(arrival),
                                "departure": timeparser(departure),
                            }
                        )
            trips[trip_id] = trip
            if len(trip) > 1:
                trips[trip_id] = trip
                if route not in routes_existed:
                    routes[route_id] = {"route": route, "trip": [trip_id]}
                    routes_existed.append(route)
                    route_id += 1
                else:
                    routes[find_route_id(route)]["trip"].append(trip_id)
                trip_id += 1

print(trips)
print()
print(routes)

for id, router in routes.items():
    if len(router["trip"]) > 1:
        print(id)
# print()
# print(stops)
