import boto3

# aws s3 ls s3://darwin.xmltimetable/PPTimetable/
s3 = boto3.client('s3')
s3.download_file('darwin.xmltimetable','PPTimetable/20250430020500_v8.xml.gz', "latest.xml.gz")
