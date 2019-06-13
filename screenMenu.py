from menuState import *
import os
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def isPassive(menuName,numVal):
	returnText=numVal+" -"
	if(menuName=="menuMain"):
		for menuMainP in menuMainPassive:
			if(menuMainP==numVal):
				returnText=bcolors.OKGREEN+"OK "+bcolors.ENDC
	elif(menuName=="menuMainAPI"):
		for menuMainAPIP in menuMainAPIPassive:
			if(menuMainAPIP==numVal):
				returnText=bcolors.OKGREEN+"OK "+bcolors.ENDC
	elif(menuName=="menuMainASI"):
		for menuMainASIP in menuMainASIPassive:
			if(menuMainASIP==numVal):
				returnText=bcolors.OKGREEN+"OK "+bcolors.ENDC
	elif(menuName=="menuMainACI"):
		for menuMainACIP in menuMainACIPassive:
			if(menuMainACIP==numVal):
				returnText=bcolors.OKGREEN+"OK "+bcolors.ENDC
	elif(menuName=="menuMainBC"):
		for menuMainBCP in menuMainBCPassive:
			if(menuMainBCP==numVal):
				returnText=bcolors.OKGREEN+"OK "+bcolors.ENDC
	return returnText
	
def deneme():
	print bcolors.OKGREEN + "OK" + bcolors.ENDC

def menuMainAPI():
	os.system("clear")
	currentMenu='menuMainAPI'
	print (	bcolors.HEADER+'''
	            Pre-Installation                
	------------------------------------------------'''+bcolors.ENDC)
	print '	  '+isPassive(currentMenu,'1')+' install ssh-keygen                       '
	print '	  '+isPassive(currentMenu,'2')+' disable Selinux                          '
	print '	  '+isPassive(currentMenu,'3')+' copy host file                           '
	print '	  '+isPassive(currentMenu,'4')+' download repo files                      '
	print '	  '+isPassive(currentMenu,'5')+' yum update                               '
	print '	  '+isPassive(currentMenu,'6')+' yum install                              '
	print ('''	  7 - Main Menu                      
	  8 - Exit''')    
	print (bcolors.HEADER+'''	------------------------------------------------'''+ bcolors.ENDC)
def menuMainASI():
	os.system("clear")
	currentMenu='menuMainASI'
	print (	bcolors.HEADER+'''
	            Ambari Server Installation               
	------------------------------------------------'''+bcolors.ENDC)
	print '	  '+isPassive(currentMenu,'1')+' Ambari Server Pre-Install                '
	print '	  '+isPassive(currentMenu,'2')+' Install Ambari Server Database           '
	print '	  '+isPassive(currentMenu,'3')+' Setup Ambari Server                      '
	print ('''	  4 - Main Menu                      
	  5 - Exit''')                                      
	print (bcolors.HEADER+'''	------------------------------------------------'''+ bcolors.ENDC)
def menuMainACI():
	os.system("clear")
	currentMenu='menuMainACI'
	print (	bcolors.HEADER+'''
	            Ambari Clients Installation               
	------------------------------------------------'''+bcolors.ENDC)
	print '	  '+isPassive(currentMenu,'1')+' Install Ambari Clients                    '
	print '	  '+isPassive(currentMenu,'2')+' Configure Ambari Clients                  '
	print '	  '+isPassive(currentMenu,'3')+' Start Ambari Clients                      '
	print ('''	  4 - Main Menu                      
	  5 - Exit''')                                      
	print (bcolors.HEADER+'''	------------------------------------------------'''+ bcolors.ENDC)
def menuMainBC():
	os.system("clear")
	currentMenu='menuMainBC'
	print (	bcolors.HEADER+'''
	            Configure Ambari Cluster
	------------------------------------------------'''+bcolors.ENDC)
	print '	  1 - open firewall port on ambari cluster            '
	print '	  2 - stop firewall services on ambari cluster        '
	print '	  3 - start firewall services on ambari cluster       '
	print '	  4 - Yum Packet install on ambari cluster            '
	print '	  5 - Change ACI Config file parameter                '
	print '	  6 - Force Clear Menu States                         '
	print '	  7 - Add New Ambari Agent                            '
	print '	  8 - Force Menu State to "Done"                      '
	print '	  9 - List Ambari Cluster Nodes                       '
	print ('''	  10 - Main Menu                      
	  11 - Exit''')                                      
	print (bcolors.HEADER+'''	------------------------------------------------'''+ bcolors.ENDC)
def menuMain():
	os.system("clear")
	currentMenu='menuMain'
	print (bcolors.HEADER+'''
	            Installation Options                
	------------------------------------------------'''+ bcolors.ENDC)
	print '	  '+isPassive(currentMenu,'1')+' Ambari Pre-Installation proccess     '
	print '	  '+isPassive(currentMenu,'2')+' Install Ambari Server                    '
	print '	  '+isPassive(currentMenu,'3')+' Install Ambari Clients                   '
	print '	  4 - ACI Configuration                  '
	print '	  5 - LAUNCH  ROCKET ( Install Everything )                  '
	print ('''	  6 - Run Terminal Command On Cluster Nodes                    
	  7 - Exit  	''')                                   
	print (bcolors.HEADER+'''	------------------------------------------------'''+ bcolors.ENDC)
def forceMenuStatetoDone(menuNumber):
	if(menuNumber==0):
		currentMenu='menuMain'
		os.system("clear")
		print (bcolors.HEADER+'''
		            Please Select Menu, which you want to change its state to "done state"                
		------------------------------------------------'''+ bcolors.ENDC)
		print '	  '+isPassive(currentMenu,'1')+' Ambari Pre-Installation proccess     '
		print '	  '+isPassive(currentMenu,'2')+' Install Ambari Server                    '
		print '	  '+isPassive(currentMenu,'3')+' Install Ambari Clients                   '
		print '	  4 - Change Nothing                                                      '
		print (bcolors.HEADER+'''	------------------------------------------------'''+ bcolors.ENDC)
	elif(menuNumber==1):
		os.system("clear")
		currentMenu='menuMainAPI'
		print (	bcolors.HEADER+'''
		            Please Select Sub Menu, which you want to change its state to "done"                
		------------------------------------------------'''+bcolors.ENDC)
		print '	  '+isPassive(currentMenu,'1')+' install ssh-keygen                       '
		print '	  '+isPassive(currentMenu,'2')+' disable Selinux                          '
		print '	  '+isPassive(currentMenu,'3')+' copy host file                           '
		print '	  '+isPassive(currentMenu,'4')+' download repo files                      '
		print '	  '+isPassive(currentMenu,'5')+' yum update                               '
		print '	  '+isPassive(currentMenu,'6')+' yum install                              '
		print '	  '+isPassive(currentMenu,'7')+' Change All Sub Menu "Done"               '
		print '	  8 - Change Nothing                                                      '
		print (bcolors.HEADER+'''	------------------------------------------------'''+ bcolors.ENDC)
	elif(menuNumber==2):
		os.system("clear")
		currentMenu='menuMainASI'
		print (	bcolors.HEADER+'''
		            Please Select Sub Menu, which you want to change its state to "done state"                
		------------------------------------------------'''+bcolors.ENDC)
		print '	  '+isPassive(currentMenu,'1')+' Ambari Server Pre-Install                '
		print '	  '+isPassive(currentMenu,'2')+' Install Ambari Server Database           '
		print '	  '+isPassive(currentMenu,'3')+' Setup Ambari Server                      '
		print '	  '+isPassive(currentMenu,'4')+' Change All Sub Menu "Done"               '
		print '	  5 - Change Nothing                                                      '
		print (bcolors.HEADER+'''	------------------------------------------------'''+ bcolors.ENDC)
	elif(menuNumber==3):
		os.system("clear")
		currentMenu='menuMainACI'
		print (	bcolors.HEADER+'''
		            Please Select Sub Menu, which you want to change its state to "done state"                          
		------------------------------------------------'''+bcolors.ENDC)
		print '	  '+isPassive(currentMenu,'1')+' Ambari Server Pre-Install                '
		print '	  '+isPassive(currentMenu,'2')+' Install Ambari Server Database           '
		print '	  '+isPassive(currentMenu,'3')+' Setup Ambari Server                      '
		print '	  '+isPassive(currentMenu,'4')+' Change All Sub Menu "Done"               '
		print '	  5 - Change Nothing                                                      '
		print (bcolors.HEADER+'''	------------------------------------------------'''+ bcolors.ENDC)

