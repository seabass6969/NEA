import csv
import json
import xml.etree.ElementTree as ET

tree = ET.parse("data_parsing/stations.xml")

# stations = {}
stations = []
root = tree.getroot()
item_to_include = ["CrsCode", "Name", "StationOperator"]

tiploc = json.load(open("data_parsing/TiplocPublicExport_2025-04-03_20-16.json", "r"))

tiplocs = {}
for tip in tiploc["Tiplocs"]:
    if tip["Details"]["CRS"] != None:
        tiplocs[tip["Details"]["CRS"]] = tip["Tiploc"]

tiploc_file = open("data_parsing/cif_tiplocs.csv", "r")
tiploc_file_csv = list(csv.reader(tiploc_file))[1:]
# CRS,Tiploc,Description,Stannox

for row in tiploc_file_csv:
    if row[0] not in tiplocs:
        tiplocs[row[0]] = row[1]

for station in root:
    station_info = {}
    for child in station:
        tag_name = child.tag.replace("{http://nationalrail.co.uk/xml/station}","")
        if tag_name in item_to_include:
            station_info[tag_name] = child.text.replace("\n", "")
        match tag_name:
            case "Latitude":
                station_info[tag_name] = float(child.text.replace("\n", ""))
            case "Longitude":
                station_info[tag_name] = float(child.text.replace("\n", ""))

            case "Address":
                address = [a.text for a in child[0][0]]
                postcode = child[0][0].find("{http://www.govtalk.gov.uk/people/AddressAndPersonalDetails}PostCode")
                station_info["Address"] = address
                station_info["Postcode"] = postcode.text
                
    if station_info["CrsCode"] in tiplocs:
        station_info["Tiploc"] = tiplocs[station_info["CrsCode"]]
        stations.append(station_info)

with open("stations.json", "w") as f:
    json.dump(stations, f)

    
