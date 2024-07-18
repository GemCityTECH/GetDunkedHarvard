import sys, urllib, urllib2, json, base64, hashlib, hmac, time

#Change the directory HERE for the input file
#(!!! must be a tab-delimited text file without headers, and only has 5 fields: ID, origin X, origin Y, destination X, and destination Y)
inputfile = r"C:\Temp\input_file.txt"
#Change the directory HERE for the output file
outputfile = r"C:\Temp\output_file.txt"
#sample input syntax that works
#https://maps.googleapis.com/maps/api/distancematrix/json?origins=-27.149887%2C-51.746696&destinations=-27.131781%2C-51.464321&key=AIzaSyBlCbsavDJZc61KcTGAgw3tzBhNdlzWm4o 


google_url = "https://maps.googleapis.com"
distance_endpoint = "/maps/api/distancematrix/json?"
#API key from Google Maps API Premium
#enter your API Key between the quotes on the line below
Key = ""
#specifies the mode of transport to use when calculating directions. Valid values are: driving, walking, transit, or bicycling
mode = "driving"

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
   encodedParams = urllib.urlencode({"origins":origin,"destinations":destination,"mode":mode,"sensor":"false","key":Key});
   #encodedParams = urllib.urlencode("origins=%s&destinations=%s&mode=%s&client=%s") % (origin, destination, mode, client)
   #decode the private key into its binary format
   url = google_url + distance_endpoint + encodedParams
   result = urllib.urlopen(url)
   result_json = json.loads(result.read())
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
