import time as pytime
from wlstModule import *

def getGCmetrics( serverlist ):
	server_profile = serverlist.split()
	# [0] = container , [1] = method , [2] = user , [3] = pass , [4] = url + [5] = appName , [6] contextRoot
	try:
		connect(server_profile[2],server_profile[3],server_profile[4])
		custom()
		cd('java.lang')
		cd('java.lang:type=GarbageCollector,name=G1 Old Generation')
		getCollectionTime = get('CollectionTime')
		getCollectionCount = get('CollectionCount')
		gcmetrics =  str(getCollectionTime) + ' ' + str(getCollectionCount)
		disconnect()
		return gcmetrics
	except WLSTException,e:
		# this typically means the server is not active, just ignore
		print "debug: getGCmetrics " + str(e)
		gcmetrics = "failed" 
		#pass
		disconnect()
		return gcmetrics

def getJVMmetrics( serverlist ):
	server_profile = serverlist.split()
	# [0] = container , [1] = method , [2] = user , [3] = pass , [4] = url + [5] = appName , [6] contextRoot
	try:
		connect(server_profile[2],server_profile[3],server_profile[4])
       		pwdstr = pwd()[:15]
       		getheapSize = ""
       		if pwdstr != 'domainRuntime:/':
			serverRuntime()
		ServerName = server_profile[0]
	#try:
		#cd("/ServerRuntimes/"+ServerName+"/JVMRuntime/"+ServerName)
		cd("/JVMRuntime/"+ServerName)
		heapSize = get('HeapSizeCurrent')
		getheapSize = str(heapSize)  + ' ' + getheapSize
		disconnect()
		return getheapSize
			
	except WLSTException,e:
		print "debug: getJVMmetrics " + str(e) 
		pass
		disconnect()
		#return  getheapSize
        
def getOpenSockets( serverlist ):
	server_profile = serverlist.split()
	# [0] = container , [1] = method , [2] = user , [3] = pass , [4] = url + [5] = appName , [6] contextRoot
	try:
		connect(server_profile[2],server_profile[3],server_profile[4])
		pwdstr = pwd()[:15]
		getOpenSocketsCurrentCount = ""
		if pwdstr != 'domainRuntime:/':
			serverRuntime()
	#	for name in serverlist:
		ServerName = server_profile[0]
		#cd("/ServerRuntimes/"+ServerName)
		OpenSocketsCurrentCount = get('OpenSocketsCurrentCount')	
		getOpenSocketsCurrentCount = str(OpenSocketsCurrentCount) + ' ' + getOpenSocketsCurrentCount
		disconnect()
		return getOpenSocketsCurrentCount
	except WLSTException,e:
                print "debug: getOpenSockets " + str(e)
                pass
                disconnect()
		#return getOpenSocketsCurrentCount


def getHTTPSessions( serverlist  ):
	server_profile = serverlist.split()
	# [0] = container , [1] = method , [2] = user , [3] = pass , [4] = url + [5] = appName , [6] contextRoot
	try:
		
		connect(server_profile[2],server_profile[3],server_profile[4])
		getOpenSessionsCurrentCount = ""
		pwdstr = pwd()[:15]
        	if pwdstr != 'domainRuntime:/':
                	serverRuntime()
		ServerName = server_profile[0]
		app = server_profile[5]
               	contextRoot = str(server_profile[6])
		appName = str(app)
               	serverName = str(ServerName)
               	pathName = '/ApplicationRuntimes/' + appName + '/ComponentRuntimes/' + serverName + '_/' + contextRoot
		cd(pathName)
               	OpenSessionsCurrentCount = get('OpenSessionsCurrentCount')
		getOpenSessionsCurrentCount = str(OpenSessionsCurrentCount) + ' ' + getOpenSessionsCurrentCount
		disconnect()
		return getOpenSessionsCurrentCount
	except WLSTException,e:
               	print "debug: getHTTPSessions " + str(e)
		pass
		disconnect()
		#return getOpenSessionsCurrentCount

	
def getTimeStamp():
	timestampNOW = pytime.strftime("%Y-%m-%d %H:%M:%S", pytime.gmtime())
	#timestampNOW = pytime.strftime("%b %d %Y %H:%M:%S", pytime.ctime())
	return timestampNOW
	
if __name__== "main":
#we are still working in progress
	#x = getJVMmetrics() + getOpenSockets() + getHTTPSessions() + getTimeStamp()
	#x = getGCmetrics()
	#print x	
#getHTTPSessions()
#getGCElapsedTime()
	disconnect()
