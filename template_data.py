# Parsing the latest.xml data into the format that the paper recommaned
# Delling, D., Pajor, T., Werneck, R.F., n.d. Round-Based Public Transit Routing.

import json

import xml.etree.ElementTree as ET

# OR: Origin Location
# IP: Passenger Calling point
# DT: Passenger Destination Calling point
# OPIP: Intermediate operational calling location
tag_include_journey = ["OR", "IP", "OPIP", "DT"]

stationfile = open("data_parsing/stations.json", "r")
stations = json.load(stationfile)["stations"]

tocfile = open("data_parsing/tocs.json", "r")
toc_code = json.load(tocfile)["tocs"]

tiplocs_file = open("pushport/stations_tiplocs.json")
tiplocs = json.load(tiplocs_file)


tree = ET.parse("pushport/latest.xml")
root = tree.getroot()


for journey in root:
    print()
    print(journey.attrib["toc"])
    for passby in journey:
        passby_tag_name = passby.tag.replace(
            "{http://www.thalesgroup.com/rtti/XmlTimetable/v8}", ""
        )
        if passby_tag_name in tag_include_journey:
            print(passby.attrib)
            print(tiplocs[passby.attrib["tpl"]]["Name"])
