import  lib.tmon_configparser as configparser
import  modules.tmon_metrics as metrics
import	modules.tmon_threads as threads

def tmonMetricsMonitor():
		# parameter from tmon3.0.conf
		paramServerList = configparser.getServerList()
		paramAdminUser 	= configparser.getAdminUser()
		paramAdminPass	= configparser.getAdminPass()
		paramConnectString = configparser.getConnectString()
		tmonLog = []	
	
		# tmonLog variable which has the data to be printed in the log file
		for args in paramServerList:
			try:
				profile_server = args.split()
				server_name = profile_server[0]
				app_name = profile_server[5]
				gc_metrics = str(metrics.getGCmetrics( args ) )
				heap_usage =  str(metrics.getJVMmetrics( args , paramAdminUser , paramAdminPass , paramConnectString  )) 
				http_sessions =  str(metrics.getHTTPSessions( args , paramAdminUser , paramAdminPass , paramConnectString ))
				open_sockets =  str(metrics.getOpenSockets( args , paramAdminUser , paramAdminPass , paramConnectString  ))
				current_ts =  str(metrics.getTimeStamp() )
				if gc_metrics != "failed":
					tmonLog.append( [ server_name , app_name , gc_metrics , heap_usage , http_sessions , open_sockets , current_ts ])
					#container || app || gc time || gc count || heap usage || http sessions cnt || open sockets cnt || timestamp 
				else:
					print "debug: tmonMetricsMonitor - there is an issue to get attribute value, please check if server is available. \n"
			except WLSTException,e:
				print "debug: tmonMetricsMonitor " + str(e) 		
		return tmonLog
	


def tmonStackMonitor():
	try:
		paramServerList = configparser.getServerList()
		paramESurl =  configparser.getESurl() 
		paramESindexName =  configparser.getESindexName()
		paramEStype = configparser.getEStype()

		tmonLog2 = []
		for i in paramServerList:
			j = i.split()
			check =  threads.getThreadStucksCount( i )[0]
			current_ts =  str(threads.getTimeStamp() )
			if check != "failed":
				hogging_cnt = threads.getThreadStucksCount( i )[1]
				stuck_cnt = threads.getThreadStucksCount( i )[2]
				for z in threads.getThreadStackHash( i ,  threads.getThreadStucksCount( i )[0] , paramESurl , paramESindexName , paramEStype ):
					tmonLog2.append( [ j[0] , j[5] , hogging_cnt , stuck_cnt , z[0] , current_ts] )
			else:
				print "debug: tmonStackMonitor - there is an issue to get attribute value, please check if server is available. \n"
		return tmonLog2
	
	except WLSTException,e:
                # this typically means the server is not active, just ignore
		print "debug: tmonStackMonitor " + str(e)
		pass	
		

if __name__== "main": 

	file = open("tmon.log","a")
	log = ''
	for content_tmon in tmonMetricsMonitor():
		log = ''
		for log_entry in content_tmon:
			log += str(log_entry) + ' '
		file.write( log )
		file.write( "\n")
	file.close()	

	file = open("tmon2.log","a")
	log = ''
	for content_tmon2 in tmonStackMonitor():
		log = ''
		for log_entry in content_tmon2:
			log += str(log_entry) + ' '
		file.write(  log )
		file.write( "\n")
	file.close()
