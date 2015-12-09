import httplib, urllib
def InsertIndex( stacklist , paramESurl , paramESindexName , paramEStype ):
		for i in stacklist:
			try:
				#print i[0]
				x = str(i[1])
				newstr = x.replace("\'", "")
				newstr = newstr.replace("\"", "")
				newstr = newstr.replace("\n","")
				newstr = newstr.replace("\t","")	
				params = "{ \"hash\":\"" + i[0] + "\",\"stack\":\"" + str(newstr) + "\" }"
				print "elasticsearch:" + str(params) + "\n"
				#print newstr
				headers = {"Content-type": "application/json","Accept": "text/plain"}
				conn = httplib.HTTPConnection( paramESurl )
				conn.request("PUT", "/" + paramESindexName + "/" + paramEStype + "/" + i[0] , params, headers)
				response = conn.getresponse()
				print response.status, response.reason
				data = response.read()
				#this prints the elasticsearch response data		
				print "elasticsearch: http response " + str(data)
				conn.close()
			except Exception: 
				pass
				print "debug: connection to the elasticsearch failed. please check if ES daemon is up and running. \n"
				print "debug: stacktrace hash is being logged in however stacktrace - hash is not being mapped on ES index.\n"
if __name__ == "main":
	InsertIndex()
