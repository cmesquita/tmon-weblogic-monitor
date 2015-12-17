def extractStackTrace( file, threadid ):
	inFile = open( file )
	keepCurrentSet = False
	stack_list = []
	for thread in threadid:
		thread_id = thread.split()[0]  + ' ' + thread.split()[1]
		thread_elapsed = thread.split()[2]
		print "debug: elapsed time " + thread_elapsed
		print "debug: thread id " + thread_id.split()[1]
		print "debug: extract " + str(thread)
		keepCurrentSet = False
		inFile = open( file )
		buffer = ""
		for line in inFile:
			if thread_id in line:
        			#---- starts a new data set
				#buffer += line
				keepCurrentSet = True
			else:
				if ( line == '\n' and keepCurrentSet == True ):
					buffer += line
					break
				elif keepCurrentSet:
					buffer += line
		inFile.close()
		stack_list.append( [ buffer , thread_elapsed , thread_id.split()[1].replace("'","") ] )
	return stack_list
	#inFile.close()
