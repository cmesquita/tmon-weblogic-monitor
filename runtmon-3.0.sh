TMON3_HOME=/home/oracle/git/tmon-weblogic-monitor
WL_HOME=/u01/app/Oracle/Middleware/Oracle_Home/wlserver/server
. $WL_HOME/bin/setWLSEnv.sh
cd $TMON3_HOME
ps -ef | grep tmon-3.0.py | grep -v grep
if [ $? == 1 ]; then
	java weblogic.WLST $TMON3_HOME/tmon-3.0.py | grep -i debug
else
	echo "Tmon-3.0 is already running."
fi
