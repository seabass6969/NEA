import json
import xml.etree.ElementTree as ET

tree = ET.parse("toc.xml")

tocs = []
root = tree.getroot()
item_to_include = ["AtocCode", "Name"]


for toc in root:
    toc_info = {}
    for child in toc:
        tag_name = child.tag.replace("{http://nationalrail.co.uk/xml/toc}","")
        if tag_name in item_to_include:
            toc_info[tag_name] = child.text.replace("\n", "")
    tocs.append(toc_info)

with open("tocs.json", "w") as f:
    json.dump({"tocs": tocs}, f)