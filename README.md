#tmon-3.0 a WEBLOGIC script monitor
## features
### (a) collects a wide range of servers metrics:
###### Tmon connects to either admin console and remote servers runtime to obtain many  performance metrics. It possible to configure which weblogic servers must be analyzed.

###### The log file will be use the following format:
######[server name, application name,  garbage collector time , garbage collector count , heap mem usage , http sessions cnt ,  open sockets cnt , hogging threads cnt ,  stuck threads cnt , server throughput  ,  server ExecuteThreadTotalCount , server ExecuteThreadIdleCount ,  current timestamp] 
### (b) puts these metrics in a log file to be analyzed
###### configuration file tmon3.0.conf can be used to set a custom log files location and name.

### (c) creates a log file containing a hash value of the stack trace for each HOGGING thread.  
###### Tmon is able to log any stack trace of hogging threads it also has the skills to insert these information in the ELASTIC SEARCH. Allowing further analysis.   

######[sever name , application name , thread id , hash value , current timestamp]
###### configuration file tmon3.0.conf can be used to set the elastic search destination to create a FROM: TO: index 

### (d) creates a HASH VALUE of the current STACK TRACE to avoid unnecessary data manipulation. 
###### Once tmon insert hash values and stack traces into elastic search , OPERATION TEAM is able to perform any kind of data correlation and checking. 
###### For instance: check the most popular hash, the worst hash and so on.  
        
## how to use:
#####1) set up weblogic environment variables . $ORACLE_HOME/wlserver/server/bin/setWLSEnv.sh 
#####2) go to tmon-3.0 directory 
######cd /home/oracle/tmon-weblogic-monitor 
#####3) configure tmon3.0.conf with the environment infos
#####4) run tmon-3.0 
######java weblogic.WLST tmon-3.0.py 

Author: Cesar Mesquita
Email: cmesquita00@hotmail.com
linkdin: https://br.linkedin.com/in/cmesquita00
