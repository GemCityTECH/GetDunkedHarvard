import requests
import time
import json

#Change the directory HERE for the input file
#(!!! must be a tab-delimited text file without headers, and only has 5 fields: ID, origin X, origin Y, destination X, and destination Y)
inputfile = r"./test_input.txt"
#Change the directory HERE for the output file
outputfile = r"./output_file.txt"

## Pull config
with open('config.json') as f:
   config = json.load(f)

# Load the configuration from 'config.json' and access the API key
api_key = config['g_api_key']

gdm_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"

field1 = "ID"
field2 = "origin_x"
field3 = "origin_y"
field4 = "destination_x"
field5 = "destination_y"
field6 = "distance_meters"
field7 = "duration_seconds"

f_in = open(inputfile, 'r')
f_out = open(outputfile, 'w')
f_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (field1, field2, field3, field4, field5, field6, field7))
f_in_line = f_in.readlines()

for line in f_in_line:
   fields = line.strip().replace("\"", "").split('\t')
   #assign x/y coordinates array to origin and destination
   origin = "%s,%s" % (fields[1], fields[2])
   destination = "%s,%s" % (fields[3], fields[4])
   #Generate valid signature
   query_params = {
      "origins": origin,
      "destinations": destination,
      "mode": "driving",
      "units": "imperial",
      "key": api_key
   }
   result_json = requests.get(gdm_url, params=query_params).json()
   print(result_json)
   check_status = result_json["rows"][0]["elements"][0]["status"]
   print ("Processing ID: " + fields[0])
   try:
      f_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (fields[0], fields[1], fields[2], fields[3], fields[4], result_json["rows"][0]["elements"][0]["distance"]["value"], result_json["rows"][0]["elements"][0]["duration"]["value"]))
   except:
      f_out.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (fields[0], fields[1], fields[2], fields[3], fields[4], result_json["rows"][0]["elements"][0]["status"]))
print ("Finished!")
print ("Process Ends: %s" % time.asctime( time.localtime(time.time()) ))
f_in.close()
f_out.close()
