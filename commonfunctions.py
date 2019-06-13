from config import *
from  screenMenu import *
#import ipaddress
networkRestartCMD = "systemctl restart network.service"
ambariServerStartCMD = "systemctl start ambari-server.service"
ambariServerStopCMD = "systemctl stop ambari-server.service"
ambariServerOnCMD = "systemctl enable ambari-server.service"
ambariServerOffCMD = "systemctl disable ambari-server.service"
ambariAgentStartCMD = "systemctl start ambari-agent.service"
ambariAgentStopCMD = "systemctl stop ambari-agent.service"
ambariAgentOnCMD = "systemctl enable ambari-agent.service"
ambariAgentOffCMD = "systemctl disable ambari-agent.service"
firewallRestartCMD = "systemctl restart firewalld.service"
firewallStartCMD = "systemctl start firewalld.service"
firewallStopCMD = "systemctl stop firewalld.service"
firewallOnCMD = "systemctl enable firewalld.service"
firewallOffCMD = "systemctl disable firewalld.service"
NTPStartCMD = "systemctl start ntpd.service"
NTPStopCMD = "systemctl stop ntpd.service"
NTPOnCMD = "systemctl enable ntpd.service"
NTPOffCMD = "systemctl disable ntpd.service"
pgServiceInitDB = pg_bindir+"postgresql"+postgres_version+"-setup initdb"
pgServiceStart = "systemctl start "+pg_service+".service "	
pgServiceStop = "systemctl stop "+pg_service+".service "	
pgServiceOn = "systemctl enable "+pg_service+".service "	
pgServiceOff = "systemctl disable "+pg_service+".service "
if(ambari_server[2]=="C6"):
	networkRestartCMD = "service network restart"
	ambariServerStartCMD = "service ambari-server start"
	ambariServerStopCMD = "service ambari-server stop"
	ambariServerOnCMD = "chkconfig ambari-server on"
	ambariServerOffCMD = "chkconfig ambari-server off"
	ambariAgentStartCMD = "service ambari-agent start"
	ambariAgentStopCMD = "service ambari-agent stop"
	ambariAgentOnCMD = "chkconfig ambari-agent on"
	ambariAgentOffCMD = "chkconfig ambari-agent off"
	firewallRestartCMD = "service iptables restart"
	firewallStartCMD = "service iptables start"
	firewallStopCMD = "service iptables stop"
	firewallOnCMD = "chkconfig iptables on"
	firewallOffCMD = "chkconfig iptables off"
	NTPStartCMD = "service ntpd start"
	NTPStopCMD = "service ntpd stop"
	NTPOnCMD = "chkconfig ntpd on"
	NTPOffCMD = "chkconfig ntpd off"
	pgServiceInitDB = "service "+pg_service+" initdb"
	pgServiceStart = "service "+pg_service+" start"	
	pgServiceStop = "service "+pg_service+" stop"	
	pgServiceOn = "chkconfig "+pg_service+" on"	
	pgServiceOff = "chkconfig "+pg_service+" off"		
def get_datetime():
	mounth=str(localtime()[1])
	my_hour=str(localtime()[3])
	my_min=str(localtime()[4])
	if(len(str(localtime()[1]))==1):
		mounth="0"+str(localtime()[1])
	day=str(localtime()[2])
	if(len(str(localtime()[2]))==1):
		day="0"+str(localtime()[2])
	return str(localtime()[0])+"_"+mounth+"_"+day+"_"+my_hour+"_"+my_min
def fileAppendWrite(file, writeText):
	try :
		fp=open(file,'ab')
		fp.write(writeText+'\n')
		fp.close()
	except :
		print '!!! An error is occurred while writing file !!!'
def fileRead(file):
	returnTEXT=""
	try :
		fp=open(file,'r')
		returnTEXT=fp.readlines()
		fp.close()
		return returnTEXT
	except :
		print '!!! An error is occurred while reading file !!!'
		return ""
def fileReadFull(file):
	returnTEXT=""
	try :
		fp=open(file,'r')
		returnTEXT=fp.read()
		fp.close()
		return returnTEXT
	except :
		print '!!! An error is occurred while reading file !!!'
		return ""
def fileClearWrite(file, writeText):
	try :
		fp=open(file,'w')
		fp.write(writeText+'\n')
		fp.close()
	except :
		print '!!! An error is occurred while writing file !!!'
def logWrite(logFile,logText):
	if(silent_mode!="true"):
		print logText
	logText='* ('+get_datetime()+') '+logText
	fileAppendWrite(logFile,logText)
def getPortNum(portNumPro):
	charPoint=portNumPro.find("/")
	return portNumPro[:charPoint]
def getPortPro(portNumPro):
	charPoint=portNumPro.find("/")
	return portNumPro[charPoint+1:]
def sshKeyGenetor(clientIP):
	try:	
		os.system("ssh "+clientIP+" -C 'ssh-keygen'")
		logWrite(log_file,"OK : ssh-keygen was generated for : "+clientIP)	
	except:
		logWrite(log_file,"ERROR : An error has occurred while ssh-keygen generate processing for : "+clientIP+" !!!")
def sshKeyCopier(clientIP):
	try:	
		os.system("ssh-copy-id -i /root/.ssh/id_rsa.pub root@"+clientIP)
		logWrite(log_file,"OK : ssh-keygen was copied for : "+clientIP)	
	except:
		logWrite(log_file,"ERROR : An error has occurred while ssh-keygen copy processing for : "+clientIP+" !!!")
def ambariServerPackageInstaller():
	try:	
		if(commands.getoutput('ls '+control_file+'')!=control_file):
			os.system("yum install -y ambari-server ")
			logWrite(log_file,"OK : ambari server package installation is completed. \n" )	
		else:
			logWrite(log_file,"Warning : Ambari server package installation  was canceled because of yum update process has not ended yet !!!! \n" )				
	except:
		logWrite(log_file,"ERROR : An error has occurred while ambari server package installation processing!!!")
def ambariServerConfigurator():
	try:	
		if(isEmbeddedPostgres=='false'):
			os.system("cp "+pg_ambari_Dir+pg_ambari_Script+" /tmp/")
			os.system("sudo -u postgres psql -U ambari ambari < /tmp/"+pg_ambari_Script)
		os.system("ambari-server setup")
		logWrite(log_file,"OK : ambari server configuration is completed. \n" )	
		if(aClient[2]=="C6"):
			os.system("sed -i -s  's/HOSTNAME=localhost.localdomain/HOSTNAME="+ambari_server[1]+"."+domain_name+"/g' /etc/sysconfig/network")
			os.system(networkRestartCMD)
		os.system(ambariServerStartCMD)
		logWrite(log_file,"OK : ambari server started. \n" )	
	except:
		logWrite(log_file,"ERROR : An error has occurred while ambari server configuration processing!!!")

def ambariAgentPackageInstaller(clientIP):
	try:	
		if(clientIP==ambari_server[0]):
			if(commands.getoutput("ls  "+control_file+"")!=control_file):
				os.system("yum install -y ambari-agent ")
				logWrite(log_file,"OK : Target IP: SERVER  ambari-agent installation is completed. \n" )	
			else:
				logWrite(log_file,"Warning : Target IP:  ambari installation  was canceled because of yum update process has not ended yet !!!! \n")				
		else:
			if(commands.getoutput('ssh '+clientIP+'  -C "ls  '+control_file+'"')!=control_file):
				os.system('ssh '+clientIP+' -C "yum install -y ambari-agent "')
				logWrite(log_file,"OK : Target IP: "+clientIP+" ambari-agent installation is completed. \n" )	
			else:
				logWrite(log_file,"Warning : Target IP: "+clientIP+" ambari installation  was canceled because of yum update process has not ended yet !!!! \n")				
	except:
		logWrite(log_file,"ERROR : An error has occurred while ambari install  process!!! Target IP: "+clientIP)

def ambariAgentConfigurator():
##sed -i -s  's/hostname=/hostname=127.12.21.22 ##/g' /etc/ambari-agent/conf/ambari-agent.ini
	try:	
		hostList=ambari_server[0]+" "+ambari_server[1]+" "+ambari_server[1]+"."+domain_name+"\n"		
		for aClient in ambari_clients: 
			if(aClient[0]==ambari_server[0]):
				print "  test "
				os.system("sed -i -s  's/hostname=localhost/hostname="+ambari_server[1]+"."+domain_name+"/g' /etc/ambari-agent/conf/ambari-agent.ini")
			else:
				os.system('scp /etc/ambari-agent/conf/ambari-agent.ini '+aClient[0]+':/etc/ambari-agent/conf/')
				if(aClient[2]=="C6"):
					os.system("ssh "+aClient[0]+" -C ' sed -i -s  ''s/HOSTNAME=localhost.localdomain/HOSTNAME="+ambari_server[1]+"."+domain_name+"/g'' /etc/sysconfig/network'")
					os.system("ssh "+aClient[0]+" -C '"+networkRestartCMD+"'")
			logWrite(log_file,"OK : "+aClient[0]+" ambari agent configuration file is updated \n ")	
	except:
		logWrite(log_file,"ERROR : An error has occurred while ambari agent configuration process !!!\n")

def ambariServerFirewallPortOpener():
	try:	
		os.system(firewallStartCMD)
		for portNumber in aServer_open_tcp_port_list: 
			if(ambari_server[2]=="C6"):
				setIpTables(ambari_server[0],getPortNum(portNumber),getPortPro(portNumber))
			else:
				os.system('firewall-cmd --permanent --zone=public --add-port='+portNumber+';firewall-cmd --reload')
		logWrite(log_file,"OK : ambari server firewall configuration is completed \n ")	
	except:
		logWrite(log_file,"ERROR : An error has occurred while ambari server firewall configuration process !!!\n")

def ambariClusterFirewallPortOpener(portNum):
	try:	
		for aClient in ambari_clients: 
			if(aClient[2]=="C6"):
				setIpTables(aClient[0],getPortNum(portNumber),getPortPro(portNumber))
			else:
				os.system('ssh '+aClient[0]+'  -C "firewall-cmd --permanent --zone=public --add-port='+getPortNum(portNum)+'/'+getPortPro(protocolNum)+'; firewall-cmd --reload"')
			logWrite(log_file,"OK : ambari cluster  server : "+aClient[0]+"  "+portNum+" firewall port is opened \n ")	
	except:
		logWrite(log_file,"ERROR : An error has occurred while ambari cluster "+portNum+" firewall port  opener process !!!\n")
		sleep(10)
def ambariClusterFirewallCloser():
	try:	
		for aClient in ambari_clients: 
			if(aClient[2]=="C6"):
				os.system('ssh '+aClient[0]+'  -C "service iptables stop;chkconfig iptables off"')
			else:
				os.system('ssh '+aClient[0]+'  -C "systemctl stop firewalld.service;systemctl disable firewalld.service"')
			logWrite(log_file,"OK : ambari cluster  server : "+aClient[0]+"  iptables service stoped \n ")	
	except:
		logWrite(log_file,"ERROR : An error has occurred while ambari cluster iptables service stop process !!!\n")

def ambariClusterFirewallStarter():
	try:	
		for aClient in ambari_clients: 
			if(aClient[2]=="C6"):
				os.system('ssh '+aClient[0]+'  -C "service iptables start;chkconfig iptables on"')
			else:
				os.system('ssh '+aClient[0]+'  -C "systemctl start firewalld.service;systemctl enable firewalld.service"')
			logWrite(log_file,"OK : ambari cluster  server : "+aClient[0]+"  iptables service started \n ")	
	except:
		logWrite(log_file,"ERROR : An error has occurred while ambari cluster iptables service start process !!!\n")

def ambariServerStartPreService():
##firewall-cmd --permanent --zone=public --add-port=8080/tcp
	try:	
		os.system('ulimit  -n 10000')
		setFQDNListFile(FQDN_file)
		os.system(firewallOnCMD)
		os.system(firewallStartCMD)
		os.system(NTPOnCMD)
		os.system(NTPStartCMD)
		for portNumber in aServer_open_tcp_port_list: 
			if(ambari_server[2]=="C6"):
				setIpTables(ambari_server[0],getPortNum(portNumber),getPortPro(portNumber))
			else:
				os.system('firewall-cmd --permanent --zone=public --add-port='+portNumber+';firewall-cmd --reload')
		logWrite(log_file,"OK : ambari server pre Service start is completed \n ")	
	except:
		logWrite(log_file,"ERROR : An error has occurred while ambari server pre Service start process !!!\n")

def ambariAgentStartService(clientIP,clientVersion):

	try:	
		if(clientIP==ambari_server[0]):
			os.system("sh /var/lib/ambari-agent/ambari-env.sh; "+ambariAgentOnCMD+";"+ambariAgentStartCMD+"")
			logWrite(log_file,"OK : MASTER ambari agent service start is completed \n ")	
		else:
			if(clientVersion=="C6"):
				os.system('ssh '+clientIP+' -C "sh /var/lib/ambari-agent/ambari-env.sh;chkconfig ambari-agent on; start ambari-agent "')
			else:
				os.system('ssh '+clientIP+' -C "sh /var/lib/ambari-agent/ambari-env.sh; systemctl enable ambari-agent; systemctl start ambari-agent "')
			logWrite(log_file,"OK : "+clientIP+" ambari agent service start is completed \n ")	
	except:
		logWrite(log_file,"ERROR : An error has occurred while ambari agent service start processing !!!\n")


def yumUpdater(clientIP):
	try:	
		if(commands.getoutput('ssh '+clientIP+'  -C "ls  '+control_file+'"')!=control_file):
			os.system('nohup ssh '+clientIP+' -C "touch '+control_file+';yum update -y; rm -f '+control_file+' " & >> /dev/null')
			logWrite(log_file,"OK : Target IP: "+clientIP+" yum update is processing... \n" )	
		else:
			logWrite(log_file,"Warning : Target IP: "+clientIP+" yum update conflict is occurred!!!! \n" )				
	except:
		logWrite(log_file,"ERROR : An error has occurred while yum update processing!!!\n Target IP: "+clientIP)
def yumUpdaterMaster():
	try:	
		if(commands.getoutput( "ls  "+control_file+"")!=control_file):
			os.system("touch "+control_file+";yum update -y; rm -f "+control_file+" & >> /dev/null")
			logWrite(log_file,"OK : Target IP:   for master server, yum update is processing ... \n" )	
		else:
			logWrite(log_file,"Warning : Target IP:   for master server, yum update conflict is occurred!!!! \n" )				
	except:
		logWrite(log_file,"ERROR : An error has occurred while yum update processing!!!\n Target IP:  master server")
##def ntpdStarter(clientIP):
def yumInstaller(clientIP,yumList):
	try:	
		if(commands.getoutput('ssh '+clientIP+'  -C "ls  '+control_file+'"')!=control_file):
			os.system('ssh '+clientIP+' -C "touch '+control_file+';yum install -y '+yumList+'; rm -f '+control_file+'"')
			logWrite(log_file,"OK : Target IP: "+clientIP+" yum install is completed \n" )	
		else:
			logWrite(log_file,"Warning : Target IP: "+clientIP+" yum install conflict is occurred!!!! \n" )				
	except:
		logWrite(log_file,"ERROR : An error has occurred while yum install processing!!!\n Target IP: "+clientIP)
def yumInstallerMaster(yumList):
	try:	
		if(commands.getoutput("ls  "+control_file+"")!=control_file):
			os.system("touch "+control_file+";yum install -y "+yumList+"; rm -f "+control_file+"")
			logWrite(log_file,"OK :  yum install is completed  for master server\n" )	
		else:
			logWrite(log_file,"Warning : Target IP: master server : yum install conflict is occurred!!!! \n" )				
	except:
		logWrite(log_file,"ERROR : An error has occurred while yum install processing!!!\n Target IP: master server")

def hostFileUpdater():  
	try:	
		hostList=ambari_server[0]+" "+ambari_server[1]+" "+ambari_server[1]+"."+domain_name+"\n"		
		for aClient in ambari_clients: 
			if(aClient[0]!=ambari_server[0]):
				hostList=hostList+aClient[0]+" "+aClient[1]+" "+aClient[1]+"."+domain_name+"\n"
		fileClearWrite("/etc/hosts", hostList)
		logWrite(log_file,"OK :  /etc/hosts file is updated for server \n ")	
	except:
		logWrite(log_file,"ERROR : An error has occurred while server /etc/hosts file  update processing !!!\n")
def hostFileCoppier():  
	try:	
		for aClient in ambari_clients: 
			if(aClient[0]!=ambari_server[0]):
				os.system("scp /etc/hosts "+aClient[0]+":/etc/hosts ")
		logWrite(log_file,"OK :  /etc/hosts file is updated. ")	
	except:
		logWrite(log_file,"ERROR : An error has occurred while /etc/hosts file  update processing!!!\n")

def nodeListGenerator():  
	try:	
		nodeList=""		
		for aClient in ambari_clients: 
			nodeList=nodeList+str(aClient[1])+"."+domain_name+"\n"
		fileClearWrite("/root/nodeList.txt", hostList)
		logWrite(log_file,"OK :  /root/nodeList.txt file is generated for ambari cluster \n ")	
	except:
		logWrite(log_file,"ERROR : An error has occurred while /root/nodeList.txt file  generate processing !!!\n")

def DisableSelinux(clientIP):  
	try:	
		os.system("ssh "+clientIP+" -C 'echo \"SELINUX=disabled\" > /etc/selinux/config'")
		os.system('ssh '+clientIP+' -C "setenforce 0"')
		logWrite(log_file,"OK :  SElinux disabled \n Target IP: "+clientIP)	
	except:
		logWrite(log_file,"ERROR : An error has occurred while SElinux disabled processing!!!\n Target IP: "+clientIP)

def pythonVersionController(clientIP): ## 1 python version Ok. 0 python version wrong. 
	rVersion=commands.getoutput("ssh "+clientIP+" -C 'python --version'")
	rVal=rVersion.find(req_python_version)
	if (rVal>-1):
		return 1
	else:
		return 0
def javaVersionController(clientIP): ## 1 python version Ok. 0 python version wrong. 
	rVersion=commands.getoutput("ssh "+clientIP+" -C 'java --version'")
	rVal=rVersion.find(req_java_version)
	if (rVal>-1):
		return 1
	else:
		return 0
##def javaInstaller(clientIP):


def repoDownloader():
	try:	
		os.system('wget -nv '+ambari_repo6+' -O ambariC6.repo')
		os.system('wget -nv '+ambari_repo7+' -O ambariC7.repo')
		os.system('wget -nv '+hdp_repo6+' -O hdpC6.repo')
		os.system('wget -nv '+hdp_repo7+' -O hdpC7.repo')
		if(ambari_server[2]=="C7"):
			os.system('cp *C7.repo /etc/yum.repos.d/')
		elif(ambari_server[2]=="C6"):
			os.system('cp *C6.repo /etc/yum.repos.d/')
		logWrite(log_file,"OK :  Repo file was download \n ")	
	except:
		logWrite(log_file,"ERROR : An error has occurred while repo download processing!!!\n ")	
def repoCoppier(clientIP,clientVersion):
	try:	
		if(clientIP!=ambari_server[0]):
			if(clientVersion=="C7"):
				os.system("scp *C7.repo "+clientIP+":/etc/yum.repos.d/")
				logWrite(log_file,"OK :  Repo file was coppied... \nTarget IP: "+clientIP+"")
			elif(clientVersion=="C6"):
				os.system("scp *C6.repo "+clientIP+":/etc/yum.repos.d/")
				logWrite(log_file,"OK :  Repo file was coppied... \nTarget IP: "+clientIP+"")

	except:
		logWrite(log_file,"ERROR : An error has occurred while repo download processing!!!\n Target IP: "+clientIP+" **** Repo Name: "+repoAddress)

def pgInstaller(pgVer):
	try:	
		if(isEmbeddedPostgres=='false'):
			errState=0
			errState=errState+int(os.system('wget -nv '+postgres_repo+' .'))
			errState=errState+int(os.system('rpm -ivh '+postgres_repo_rpm+''))
			errState=errState+int(os.system("yum install -y  postgresql"+pgVer+".x86_64 postgresql"+pgVer+"-contrib.x86_64 postgresql"+pgVer+"-libs.x86_64 postgresql"+pgVer+"-devel.x86_64 postgresql"+pgVer+"-python.x86_64 postgresql"+pgVer+"-server.x86_64"))
			errState=errState+int(os.system(pgServiceInitDB))
			errState=errState+int(os.system("sed -i -s  s/\"#listen_addresses = 'localhost'\"/\"listen_addresses = '*'\"/g "+pg_conf_file))
			fileClearWrite(pg_hba_file,"local   all   ambari      trust\nlocal   all   all   peer\nhost    ambari ambari "+ambari_server[0]+"/24 trust \nhost    all   all    127.0.0.1/32  ident\nhost    all   all    ::1/128  ident")
			errState=errState+int(os.system(pgServiceOn))
			errState=errState+int(os.system(pgServiceStart))
			errState=errState+int(os.system("cp "+pg_ambari_preScript+" /tmp/"))
			errState=errState+int(os.system("sudo -u postgres psql < /tmp/"+pg_ambari_preScript))
			if(errState==0):
				logWrite(log_file," OK : Ambari database Installation and configuration was completed.")		
				return 1
			else:
				logWrite(log_file," ERROR : While Ambari database Installation and configuration processing...")		
				return 0
	except :
		logWrite(log_file,"ERROR : An error has occurred while ambari database installation processing!!!")	
		return 0
def preRequiredSteps(menuList,stepValue):
	returnVal=0
	for menuVal in menuList:
		if(menuVal.find(stepValue)!=-1):
			returnVal=1
	return returnVal

def clearMenuStates():
	textVal="menuMainPassive=[]\nmenuMainAPIPassive=[]\nmenuMainASIPassive=[]\nmenuMainACIPassive=[]\nmenuMainAPIMax=6\nmenuMainASIMax=3\nmenuMainACIMax=3"
	fileClearWrite("menuState.py", textVal)
	logWrite(log_file,"OK : Menu state force clear is completed. You must restart this program !!!")	
	exit(0)
def exitControl():
	textValMainHeader="menuMainPassive=["
	textValMainAPIHeader="menuMainAPIPassive=["
	textValMainASIHeader="menuMainASIPassive=["
	textValMainACIHeader="menuMainACIPassive=["
	textValMain=""
	textValMainAPI=""
	textValMainASI=""
	textValMainACI=""
	for valMenuMainPassive  in menuMainPassive:
		textValMain=textValMain+'"'+valMenuMainPassive+'",'
	textValMain=textValMainHeader+textValMain+"]"
	for valMenuMainAPIPassive  in menuMainAPIPassive:
		textValMainAPI=textValMainAPI+'"'+valMenuMainAPIPassive+'",'
	textValMainAPI=textValMainAPIHeader+textValMainAPI+"]"
	for valMenuMainASIPassive  in menuMainASIPassive:
		textValMainASI=textValMainASI+'"'+valMenuMainASIPassive+'",'
	textValMainASI=textValMainASIHeader+textValMainASI+"]"
	for valMenuMainACIPassive  in menuMainACIPassive:
		textValMainACI=textValMainACI+'"'+valMenuMainACIPassive+'",'
	textValMainACI=textValMainACIHeader+textValMainACI+"]"
	
	textValRaw=textValMain+"\n"+textValMainAPI+"\n"+textValMainASI+"\n"+textValMainACI
	textVal=textValRaw.replace(",]", "]")
	textValTail="\nmenuMainAPIMax=6\nmenuMainASIMax=3\nmenuMainACIMax=3"
	fileClearWrite("menuState.py", textVal+textValTail)
	exit(0)
def generateNewConfigFile():
	print "		!!! BE CAREFULL !!!\N	 DON'T ANY MISTAKE WHILE YOU ARE CHANGING CONFIG FILE "
	fileHEADER = "#-*- coding: utf-8 -*-\nimport sys\nimport string\nfrom time import *\nimport os\nimport re\nimport commands\n##################PARAMETERS################################\n######## for Redhat6/Centos6 = C6, for Redhat7/Centos7  = C7\n"
	fileBODY = ""
	oldFILE=fileRead("config.py")
	for oldLINE in oldFILE:
		equalPoint=oldLINE.find("=")
		if(equalPoint!=-1):
			print "	"+bcolors.BOLD+oldLINE[:equalPoint-1]+"= "+bcolors.ENDC+oldLINE[equalPoint:]
			returnVAl=raw_input("	Do you want to change this parameter? Default No (y/n ) = ") 
			if(returnVAl=='y' or returnVAl=='Y'):
				newConfig=raw_input("	Please Enter new value \n 	"+oldLINE[:equalPoint-1]+"= ") 
				fileBODY=fileBODY+oldLINE[:equalPoint-1]+'= '+newConfig+'\n'
			else:
				fileBODY=fileBODY+oldLINE
	print "---------------------------------------------------------------------------------------"
	print fileBODY
	print "---------------------------------------------------------------------------------------"
	returnConfAnswer=raw_input("	Do you want to use this configuration, which is above? Default No (y/n ) = ") 
	if(fileBODY != ""):
		if(returnConfAnswer=='y' or returnConfAnswer=='Y'):
			fileClearWrite("config.py", fileHEADER+fileBODY)
			logWrite(log_file,"OK : New config file generation is completed. You must restart this program !!!")	
	else :
		logWrite(log_file,"!!! ERROR : An error has occurred while new config file generating !!!")	
	sleep(5)
	exitControl(0)
def updateAgentlist(agentIpAdd,agentHostName,agentVersion):
	fileHEADER = "#-*- coding: utf-8 -*-\nimport sys\nimport string\nfrom time import *\nimport os\nimport re\nimport commands\n##################PARAMETERS################################\n######## for Redhat6/Centos6 = C6, for Redhat7/Centos7  = C7\n"
	fileBODY = ""
	oldFILE=fileRead("config.py")
	for oldLINE in oldFILE:
		if(oldLINE.find("=")!=-1):
			equalPoint=oldLINE.find("ambari_clients")
			if(equalPoint!=-1):
				fileBODY=fileBODY+oldLINE.replace(']]', '],["'+agentIpAdd+'","'+agentHostName+'","'+agentVersion+'"]]')
			else:
				fileBODY=fileBODY+oldLINE
	if(fileBODY != ""):
		fileClearWrite("config.py", fileHEADER+fileBODY)
		logWrite(log_file,"OK : Update Agent list is completed. You must restart this program !!!")	
	else :
		logWrite(log_file,"!!! ERROR : An error has occurred while Update Agent list procces !!!")	
	sleep(5)
	exitControl(0)	

def addNewAmbariAgent():
	ipAdd=""
	returnHostName=""
	returnHostVersion=""
	returnIP=raw_input("	Please enter New Agent ip : ") 
	try :
#orgFunction#		ipAdd=ipaddress.ip_address(unicode(returnIP))
		ipAdd=returnIP
	except :
		print  "	"+bcolors.WARNING+"!!! ERROR : INVALID IP NUMBER !!! "+bcolors.ENDC
		sleep(5)
	returnHostName=raw_input("	Please enter Hostname : ") 
	if(returnHostName!=""):	
		returnHostVersion=raw_input("	Please enter Host Operating System Version ( Centos6/Redhat6 = C6,Centos7/Redhat7 = C7) : ") 	
		try :
			if(returnHostVersion=="C6" or returnHostVersion=="C7"):
				logWrite(log_file,"OK : New Ambari Agent Adding proccess is starting !!!\n")
				sshKeyGenetor(returnIP)
				sshKeyCopier(returnIP)
				DisableSelinux(returnIP)
				try:	
					newHost=returnIP+" "+returnHostName+" "+returnHostName+"."+domain_name+"\n"
					fileAppendWrite("/etc/hosts", newHost)
					logWrite(log_file,"OK :  /etc/hosts file is updated for server \n ")	
				except:
					logWrite(log_file,"ERROR : An error has occurred while server /etc/hosts file  update processing !!!\n")	

				try:	
					os.system("scp /etc/hosts "+returnIP+":/etc/hosts ")
					for aClient in ambari_clients: 
						if(aClient[0]!=ambari_server[0]):
							os.system("scp /etc/hosts "+aClient[0]+":/etc/hosts ")
					logWrite(log_file,"OK :  /etc/hosts file is updated. ")	
				except:
					logWrite(log_file,"ERROR : An error has occurred while /etc/hosts file  update processing!!!\n")

				os.system('wget -nv '+ambari_repo+' .')
				os.system('wget -nv '+hdp_repo+' .')
				repoCoppier(returnIP)
				os.system("rm -f *.repo")
				yumUpdater(returnIP)
				yumInstaller(returnIP,yum_list)
				ambariAgentPackageInstaller(returnIP)
				try : 	
					os.system('scp /etc/ambari-agent/conf/ambari-agent.ini '+returnIP+'.'+domain_name+':/etc/ambari-agent/conf/')
					logWrite(log_file,"OK : "+returnIP+" ambari agent configuration file is updated \n ")	
	
				except :
					logWrite(log_file,"ERROR : An error has occurred while ambari agent configuration process !!!\n")
				ambariAgentStartService(returnIP)	
				logWrite(log_file,"OK : New Ambari Agent Adding proccess is completed. You must restart program.\n")
				updateAgentlist(returnIP,returnHostName,returnHostVersion)
			else:
				logWrite(log_file,"!!! ERROR : Wrong operating system version !!!\n")				
			exitControl(0)
		except :
			logWrite(log_file,"!!! ERROR : An error has occurred while Adding New ambari agent process !!!\n")
	else:
		print  "	"+bcolors.WARNING+"!!! ERROR : INVALID HOSTNAME !!! "+bcolors.ENDC
		sleep(5)	
def listAmbariCluster():
	os.system("clear")
	print  "	"+bcolors.OKGREEN+" -------AMBARI CLUSTER COMPONENTS----------- "+bcolors.ENDC
	print  "	"+bcolors.OKGREEN+" ------------------------------------------- "+bcolors.ENDC
	print  "	"
	print  "	Cluster Domain Name : "+domain_name+""
	print  "	Ambari Server  Name : "+ambari_server[1]+"	IP : "+ambari_server[0]+"	OS version : "+ambari_server[2]
	print  "	"
	print  "	"+bcolors.OKGREEN+" ------------------------------------------- "+bcolors.ENDC
	print  "	"
	for aClient in ambari_clients: 
		print  "	Ambari Agent  Name : "+aClient[1]+"	IP : "+aClient[0]+"	OS version : "+aClient[2]
	print  "	"
	print  "	"+bcolors.OKGREEN+" ------------------------------------------- "+bcolors.ENDC
	returnVAl=raw_input("	 Please Enter for Go to Menu ") 
#def setNetworkFile():
##	/etc/sysconfig/network

def setIpTables(clientIP,targetPort,targetProtocol):
#	fileTextRaw=""
	try:	
		if(clientIP==ambari_server[0]):
##-A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
#			fileTextRaw=fileReadFull("/etc/sysconfig/iptables")
#			fileTextNew=fileTextRaw.replace(":OUTPUT ACCEPT [0:0]",":OUTPUT ACCEPT [0:0]\n-A INPUT  -m state --state NEW -m "+targetProtocol+" -p "+targetProtocol+" --dport "+targetPort+" -j ACCEPT")
#			fileClearWrite("/etc/sysconfig/iptables", fileTextNew)
#			os.system(firewallRestartCMD)
			os.system("iptables -I INPUT -p "+targetProtocol+" -m "+targetProtocol+"   --dport "+targetPort+" -j ACCEPT;service iptables save")
			logWrite(log_file,"OK :  iptables setting was completed... \nTarget IP: "+clientIP+"")
		else:
			os.system("ssh "+clientIP+"  -C 'iptables -I INPUT -p "+targetProtocol+" -m "+targetProtocol+"   --dport "+targetPort+" -j ACCEPT;service iptables save'")
			os.system("ssh "+clientIP+"  -C '"+firewallRestartCMD+"'")
			logWrite(log_file,"OK :  iptables setting was completed... \nTarget IP: "+clientIP+"")

	except:
		logWrite(log_file,"ERROR : An error has occurred while iptables setting processing!!!\n Target IP: "+clientIP+" **** target Port: "+targetPort)
def terminalCommand(clientIP,terCommand):
	try:	
		if(clientIP!=ambari_server[0]):
			os.system(terCommand)
			logWrite(log_file,"OK : command '"+terCommand+"' is executed. \nTarget IP: "+clientIP+"\n")
		else:
			os.system("ssh "+clientIP+"  -C '"+terCommand+"'")
			logWrite(log_file,"OK : command '"+terCommand+"' is executed. \nTarget IP: "+clientIP+"\n")

	except:
		logWrite(log_file,"ERROR : An error has occurred while iptables setting processing!!!\n Target IP: "+clientIP+" **** target Port: "+targetPort)
def setFQDNListFile(fName):
	try:	
		for aClient in ambari_clients:
			fileAppendWrite(fName, aClient[1]+"."+domain_name)
		logWrite(log_file,"OK : FQDN list file is created. \n")
	except:
		logWrite(log_file,"ERROR : An error has occurred while FQDN list file writing!!!\n ")

