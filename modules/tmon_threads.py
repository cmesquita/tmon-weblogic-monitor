from wlstModule import *
import lib.tmon_threaddump as extract
import lib.tmon_md5	as hash
import lib.tmon_elasticsearch as elasticsearch
import time as pytime

def getThreadStucksCount( serverlist ):
	try:
		threads_details = []
		thread_hogging = []
        	# [0] = container , [1] = method , [2] = user , [3] = pass , [4] = url , [5] = appName , [6] contextRoot
		j = serverlist.split()
        	connect(j[2],j[3],j[4])
		pwdstr = pwd()[:15]
		if pwdstr != 'serverRuntime:/':
			serverRuntime()
		cd('ThreadPoolRuntime/ThreadPoolRuntime' )
		threads = get('ExecuteThreads')
		hogging_count =  get('HoggingThreadCount')
		stuck_count = get('StuckThreadCount')
		thread_Throughput = get('Throughput')
		thread_ExecuteThreadTotalCount = get('ExecuteThreadTotalCount')
		thread_ExecuteThreadIdleCount = get('ExecuteThreadIdleCount')
		for thread in threads :
        		isHogging = thread.isHogger()
        		if isHogging > 0 :
				thread_hogging_elapsed = thread.currentRequest.split()
				thread_elapsed = thread_hogging_elapsed[8]
				thread_info = thread.getName().split()
				thread_hogging.append(thread_info[1] + ' ' + thread_info[2] + ' ' +  thread_elapsed)
		#[0] threads id list , [1] count threads hogging , [2] count threads stuck , [3] Throughput , [4] ExecuteThreadTotalCount , [5] ExecuteThreadIdleCount
		threads_details.append(thread_hogging)
		threads_details.append(hogging_count)
		threads_details.append(stuck_count)  
		threads_details.append(int(round(thread_Throughput)))
		threads_details.append(thread_ExecuteThreadTotalCount)
		threads_details.append(thread_ExecuteThreadIdleCount)
		disconnect()
		return threads_details
	
	except WLSTException,e:
		print "debug: getThreadStucksCount " + str(e)
		threads_details.append( "failed" )
		disconnect()
		return threads_details
		


def getThreadStackHash( serverlist , thread_id , es_url , es_indexname , es_type ):
	try:
		j = serverlist.split()
		# [0] = container , [1] = method , [2] = user , [3] = pass , [4] = url , [5] = appName , [6] contextRoot
		print "debug: " + j[2] + " - " + j[0]
		connect(j[2],j[3],j[4])
		threadDump()
		file = 'Thread_Dump_'+j[0]+'.txt'
		stacktrace = extract.extractStackTrace( file, thread_id )
		print "debug: getThreadStackHash " + str(stacktrace)
		stackmd5 = hash.genMD5(stacktrace)
		elasticsearch.InsertIndex(stackmd5 , es_url , es_indexname , es_type )
		disconnect()
		return stackmd5
	
	except WLSTException,e:
		print "debug: " + str(e)
		pass

def getTimeStamp():
        timestampNOW = pytime.strftime("%Y-%m-%d %H:%M:%S", pytime.gmtime())
        #timestampNOW = pytime.strftime("%b %d %Y %H:%M:%S", pytime.ctime())
        return timestampNOW

