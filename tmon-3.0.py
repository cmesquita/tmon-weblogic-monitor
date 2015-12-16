import  lib.tmon_configparser as configparser
import  modules.tmon_metrics as metrics
import	modules.tmon_threads as threads
import time as pytime
import datetime

def tmonMetricsMonitor():
		# parameter from tmon3.0.conf
		paramServerList = configparser.getServerList()
		#paramAdminUser 	= configparser.getAdminUser()
		#paramAdminPass	= configparser.getAdminPass()
		#paramConnectString = configparser.getConnectString()
		tmonLog = []	
	
		# tmonLog variable which has the data to be printed in the log file
		for args in paramServerList:
			try:
				start = datetime.datetime.now()
				profile_server = args.split()
				server_name = profile_server[0]
				app_name = profile_server[5]
				gc_metrics = str(metrics.getGCmetrics( args ) )
				heap_usage =  str(metrics.getJVMmetrics( args )) 
				http_sessions =  str(metrics.getHTTPSessions( args ))
				open_sockets =  str(metrics.getOpenSockets( args ))
				current_ts =  str(metrics.getTimeStamp() )

				check =  threads.getThreadStucksCount( args )[0]

				if check != "failed":
					threads_info =  threads.getThreadStucksCount( args )
					 #[0] threads id list , [1] count threads hogging , [2] count threads stuck , [3] Throughput , [4] ExecuteThreadTotalCount , [5] ExecuteThreadIdleCount
					print "debug: elapsed" + str(threads_info[0])
					hogging_cnt  = threads_info[1]
					stuck_cnt    = threads_info[2] 
					thread_Throughput =  threads_info[3]
					thread_ExecuteThreadTotalCount = threads_info[4]
					thread_ExecuteThreadIdleCount = threads_info[5]
				else:
					print "debug: tmonStackMonitor - there is an issue to get attribute value, please check if server is available. \n"

				if gc_metrics != "failed":
					tmonLog.append( [ server_name , app_name , gc_metrics , heap_usage , http_sessions , open_sockets , hogging_cnt , stuck_cnt , thread_Throughput , thread_ExecuteThreadTotalCount  , thread_ExecuteThreadIdleCount ,  current_ts ])
					#container || app || gc time || gc count || heap usage || http sessions cnt || open sockets cnt || hogging cnt || stuck cnt|| Throughput || ExecuteThreadTotalCount || ExecuteThreadIdleCount || timestamp 
				else:
					print "debug: tmonMetricsMonitor - there is an issue to get attribute value, please check if server is available. \n"
				end = datetime.datetime.now()
				diff = end - start
				print "function (tmonMetricsMonitor) container: " + server_name +  " tooks about: " + str(int(round(diff.microseconds / 1000))) + " to finish."
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
		for args in paramServerList:
			profile_server = args.split()
			threads_stucks = threads.getThreadStucksCount( args )
			#check =  threads.getThreadStucksCount( i )[0]
			check =  threads_stucks[0]
			current_ts =  str(threads.getTimeStamp() )
			if check != "failed":
				hogging_cnt = threads_stucks[1]
				stuck_cnt = threads_stucks[2]
				thread_list = threads_stucks[0]
				for threads_hash in threads.getThreadStackHash( args ,  thread_list , paramESurl , paramESindexName , paramEStype ):
					tmonLog2.append( [ profile_server[0] , profile_server[5],  threads_hash[0],  threads_hash[2] , current_ts] )
			else:
				print "debug: tmonStackMonitor - there is an issue to get attribute value, please check if server is available. \n"
		return tmonLog2
	
	except WLSTException,e:
                # this typically means the server is not active, just ignore
		print "debug: tmonStackMonitor " + str(e)
		pass	
		

if __name__== "main": 

	tmonLogMetrics = configparser.getTmonLogMetrics()
	tmonLogThreads = configparser.getTmonLogThreads()
	tmonLogRotate =  configparser.getTmonLogRotate()
	timestampNOW = pytime.strftime("%Y-%m-%d", pytime.gmtime())
	
	if tmonLogRotate == 'Y':
		file = open( tmonLogMetrics + timestampNOW  , "a" )
	else:
		file = open(tmonLogMetrics , "a" )

	log = ''
	
	for content_tmon in tmonMetricsMonitor():
		log = ''
		for log_entry in content_tmon:
			log += str(log_entry) + ' '
		file.write( log )
		file.write( "\n")
	file.close()	
				




	if tmonLogRotate == 'Y':
		file = open(tmonLogThreads + timestampNOW  , "a" )
	else:
		file = open(tmonLogThreads , "a" )

	log = ''

	for content_tmon2 in tmonStackMonitor():
		log = ''
		for log_entry in content_tmon2:
			log += str(log_entry) + ' '
		file.write(  log )
		file.write( "\n")
	file.close()
