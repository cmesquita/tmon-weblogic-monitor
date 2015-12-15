import time as pytime
import md5
import ConfigParser, os

def genMD5( stacktrace ):
	hexoutput = []
	stacklist = []
	for i in stacktrace:
		stack = str(i[0])
		print "debug: stack " + stack
		elapsed = str(i[1])
		print "debug: elapsed " + elapsed
		m=md5.new()
		m.update( stack )
		output = m.digest()
		print "debug: time " + elapsed
		print "debug: stack " + m.hexdigest() 
		stacklist.append ( [m.hexdigest() , stack , elapsed ] )
	return stacklist
