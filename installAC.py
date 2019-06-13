##################### AMBARI CLUSTER INSTALLER ############
#!/usr/bin/python
#-*- coding: utf-8 -*-
## Author			: Mustafa YAVUZ 
## E-mail			: mustafa.yavuz
## Version			: 1.0
## Date				: 05.04.2017
## OS System 			: Redhat/Centos 6
##################PARAMETERS################################
from screenMenu import *
from config import *
from commonfunctions import *
import time
#global MenuState=0
def main():
	MenuState=0
	ans=True
	if(len(menuMainAPIPassive)==menuMainAPIMax):
		menuMainPassive.append('1')
	if(len(menuMainASIPassive)==menuMainASIMax):
		menuMainPassive.append('2')
	if(len(menuMainACIPassive)==menuMainACIMax):
		menuMainPassive.append('3')
	while ans:
		if(MenuState==0):
			menuMain()
			ans=raw_input("	What would you like to do? ") 
		if ans=="1" or  MenuState==1 : 
			MenuState=1		
			menuMainAPI()
			returnVAl=raw_input("	What would you like to do? ") 
			if returnVAl=="1" :  ### ssh keygen generation
				for aClient in ambari_clients:
					if(aClient[0]==ambari_server[0]):
						os.system("ssh-keygen")
						os.system("cp /root/.ssh/id_rsa /root/ambariKEY")
						sshKeyCopier(aClient[0])
					else:
						sshKeyGenetor(aClient[0])
						sshKeyCopier(aClient[0])
				menuMainAPIPassive.append('1')
			elif returnVAl=="2" : 		### SElinux disabled
				if(preRequiredSteps(menuMainAPIPassive,"1")==1):
					for aClient in ambari_clients:
						if(aClient[0]==ambari_server[0]):
							os.system('echo "SELINUX=disabled" > /etc/selinux/config')
							os.system('ssh setenforce 0')
						else:
							DisableSelinux(aClient[0])
					menuMainAPIPassive.append('2')
				else:
					logWrite(log_file,"!!!! SORRY : You must complete 'ssh keygen generation' step before this procces !!!!")
					
			elif returnVAl=="3" : 		### /etc/hosts configuration
				if(preRequiredSteps(menuMainAPIPassive,"1")==1 and preRequiredSteps(menuMainAPIPassive,"2")==1):
					hostFileUpdater()
					hostFileCoppier()
					menuMainAPIPassive.append('3')	
				else:
					logWrite(log_file,"!!!! SORRY : You must complete 'Ambari Pre-Installation (step 1 and 2) ' step before this procces !!!!")

			elif returnVAl=="4" : 		### Download repo Files
				if(preRequiredSteps(menuMainAPIPassive,"1")==1 and preRequiredSteps(menuMainAPIPassive,"3")==1):
					repoDownloader()
					for aClient in ambari_clients:
						repoCoppier(aClient[0],aClient[2])			
						time.sleep(10)
					os.system("rm -f *.repo")
					menuMainAPIPassive.append('4')
				else:
					logWrite(log_file,"!!!! SORRY : You must complete 'Ambari Pre-Installation (step 1 and 3) ' step before this procces !!!!")

			elif returnVAl=="5" : 		### Yum update
				if(preRequiredSteps(menuMainAPIPassive,"1")==1 and preRequiredSteps(menuMainAPIPassive,"3")==1 and preRequiredSteps(menuMainAPIPassive,"4")==1):
					for aClient in ambari_clients:
						if(aClient[0]==ambari_server[0]):
							yumUpdaterMaster()
						else:
							yumUpdater(aClient[0])
					menuMainAPIPassive.append('5')							
				else:
					logWrite(log_file,"!!!! SORRY : You must complete 'Ambari Pre-Installation (step 1,3 and 4) ' step before this procces !!!!")

			elif returnVAl=="6" : 		### Yum install
				if(preRequiredSteps(menuMainAPIPassive,"1")==1 and preRequiredSteps(menuMainAPIPassive,"3")==1 and preRequiredSteps(menuMainAPIPassive,"4")==1):
					for aClient in ambari_clients:
						if(aClient[0]==ambari_server[0]):
							yumInstallerMaster(yum_list)
						else:
							yumInstaller(aClient[0],yum_list)
					menuMainAPIPassive.append('6')
				else:
					logWrite(log_file,"!!!! SORRY : You must complete 'Ambari Pre-Installation (step 1,3 and 4) ' step before this procces !!!!")

			elif returnVAl=="7" : 		### Main Menu
				print "your Choise: "+returnVAl+" --- You are going to Main Menu ..."
				MenuState=0
			elif returnVAl=="8" : 		### Main Menu
				print "your Choise : "+returnVAl
				print("\n Goodbye") 
				exitControl()
			else :
				print(bcolors.WARNING +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC)
			time.sleep(3)
		elif ans=="2"  or  MenuState==2:
			MenuState=2
			menuMainASI() 
			returnVAl=raw_input("	What would you like to do? ") 
			if returnVAl=="1" :     ### Ambari Server Pre-Install 
				if(preRequiredSteps(menuMainAPIPassive,"6")==1):
					if(len(menuMainAPIPassive)==menuMainAPIMax):
						ambariServerFirewallPortOpener()
						ambariServerStartPreService()
						menuMainASIPassive.append('1')
					else:
						print "!!! Sorry You won't install Ambari Server until complete 'Ambari Pre-Installation proccess'  "
				else:
					logWrite(log_file,"!!!! SORRY : You must complete 'Ambari Pre-Installation ' step before this procces !!!!")

				time.sleep(5)
			elif returnVAl=="2" : 		### Install Ambari Server Database 
				if(preRequiredSteps(menuMainASIPassive,"1")==1):
					if(len(menuMainAPIPassive)==menuMainAPIMax):
						pgInstaller(postgres_version)
						time.sleep(10)
						menuMainASIPassive.append('2')					
					else:
						print "!!! Sorry You won't install Ambari Server until complete 'Ambari Pre-Installation proccess'  "
				else:
					logWrite(log_file,"!!!! SORRY : You must complete 'Ambari Server Pre-Install ' step before this procces !!!!")

				time.sleep(5)
			elif returnVAl=="3" : 		### Setup Ambari Server
				if(preRequiredSteps(menuMainASIPassive,"2")==1):
					if(len(menuMainAPIPassive)==menuMainAPIMax):
						ambariServerPackageInstaller()
						ambariServerConfigurator()
						time.sleep(10)
						menuMainASIPassive.append('3')
					else:
						print "!!! Sorry You won't install Ambari Server until complete 'Ambari Pre-Installation proccess'  "
					nodeListGenerator()
				else:
					logWrite(log_file,"!!!! SORRY : You must complete 'Install Ambari Server Database' step before this procces !!!!")

				time.sleep(5)
			elif returnVAl=="4" : 		### Main Menu
				print "your Choise :"+returnVAl+" --- You are going to Main Menu ..."
				MenuState=0
			elif returnVAl=="5" : 		### Main Menu
				print "your Choise : "+returnVAl
				print("\n Goodbye") 
				exitControl()
			else :
				print(bcolors.WARNING +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC)
				time.sleep(5)
			time.sleep(3)
		elif ans=="3"  or  MenuState==3:
			MenuState=3
			menuMainACI() 
			returnVAl=raw_input("	What would you like to do? ") 
			if returnVAl=="1" :     ### Install Ambari Clients
				if(preRequiredSteps(menuMainASIPassive,"3")==1):
					if(len(menuMainASIPassive)==menuMainASIMax):
						for aClient in ambari_clients:
							ambariAgentPackageInstaller(aClient[0])
						menuMainACIPassive.append('1')
					else:
						print "!!! Sorry You won't install Ambari Clients until complete 'Ambari Server Installation'  "
				else:
					logWrite(log_file,"!!!! SORRY : You must complete 'Install Ambari Server' step before this procces !!!!")

				time.sleep(5)
			elif returnVAl=="2" : 		### Configure Ambari Clients  
				if(preRequiredSteps(menuMainACIPassive,"1")==1):
					if(len(menuMainASIPassive)==menuMainASIMax):
						ambariAgentConfigurator()
						menuMainACIPassive.append('2')
					else:
						print "!!! Sorry You won't install Ambari Clients until complete 'Ambari Server Installation'  "
				else:
					logWrite(log_file,"!!!! SORRY : You must complete 'Install Ambari Clients' step before this procces !!!!")

				time.sleep(5)
			elif returnVAl=="3" : 		###  Start Ambari Clients
				if(preRequiredSteps(menuMainACIPassive,"2")==1):
					if(len(menuMainASIPassive)==menuMainASIMax):
						for aClient in ambari_clients:
							ambariAgentStartService(aClient[0],aClient[2])
						menuMainACIPassive.append('3')
					else:
						print "!!! Sorry You won't install Ambari Clients until complete 'Ambari Server Installation'  "
				else:
					logWrite(log_file,"!!!! SORRY : You must complete 'Configure Ambari Clients' step before this procces !!!!")
				time.sleep(5)
			elif returnVAl=="4" : 		### Main Menu
				print "your Choise : "+returnVAl+" --- You are going to Main Menu ..."
				MenuState=0
			elif returnVAl=="5" : 		### Main Menu
				print "your Choise :"+returnVAl
				print("\n Goodbye") 
				exitControl()
			else :
				print(bcolors.WARNING +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC)
				time.sleep(5)
			time.sleep(3)
		elif ans=="4"  or  MenuState==4:
			MenuState=4
			menuMainBC()
			returnVAl=raw_input("	What would you like to do? ") 
			if returnVAl=="1" :     ### open firewall port on ambari cluster
				if(preRequiredSteps(menuMainAPIPassive,"1")==1):
					try: 
						a=int(getPortNum(returnVAl))
						if(getPortPro(returnVAl)=="tcp" or getPortPro(returnVAl)=="udp"):
							ambariClusterFirewallPortOpener(returnVAl)
						else :
							print "!!! Sorry Invalid Protocol was entered !!! "
					except :
						print "!!! Sorry Invalid Syntax was entered !!! "
				else:
					logWrite(log_file,"!!!! WARNING : You must complete ssh-keygen installation step before this procces !!!!")
				time.sleep(5)
			elif returnVAl=="2" :     ### start firewall services on ambari cluster
				if(preRequiredSteps(menuMainAPIPassive,"1")==1):
					returnVAl=raw_input("		!!! Are You sure to stop ambari cluster firewall services ? (y/n)  ") 
					if(returnVAl=='y' or returnVAl=='Y'):
						ambariClusterFirewallCloser()
				else:
					logWrite(log_file,"!!!! WARNING : You must complete ssh-keygen installation step before this procces !!!!")
				time.sleep(5)
			elif returnVAl=="3" :     ### stop firewall services on ambari cluster
				if(preRequiredSteps(menuMainAPIPassive,"1")==1):
					returnVAl=raw_input("		!!! Are You sure to start ambari cluster firewall services ? (y/n)  ") 
					if(returnVAl=='y' or returnVAl=='Y'):
						ambariClusterFirewallStarter()
				else:
					logWrite(log_file,"!!!! WARNING : You must complete ssh-keygen installation step before this procces !!!!")

				time.sleep(5)
			elif returnVAl=="4" :     ### Yum Packet install on ambari cluster
				if(preRequiredSteps(menuMainAPIPassive,"1")==1):
					returnVAl=raw_input("!!! Please Enter packet name :  ") 
					for aClient in ambari_clients: 
						yumInstaller(aClient[0],returnVAl)
				else:
					logWrite(log_file,"!!!! WARNING : You must complete ssh-keygen installation step before this procces !!!!")

				time.sleep(5)
			elif returnVAl=="5" :     ### Config file generator
				returnVAl=raw_input("		!!! Are You sure to generate new config file (config.py) ? (y/n)  ") 
				if(returnVAl=='y' or returnVAl=='Y'):
					generateNewConfigFile()
				time.sleep(5)
			elif returnVAl=="6" :     ### Force Clear Menu states
				returnVAl=raw_input("		!!! Are You sure to Force Clear Menu states ? (y/n)  ") 
				if(returnVAl=='y' or returnVAl=='Y'):
					clearMenuStates()
				time.sleep(5)
			elif returnVAl=="7" :     ### Add New Ambari Agent
				if(preRequiredSteps(menuMainAPIPassive,"1")==1):
					returnVAl=raw_input("		!!! Are You sure to Adding New Ambari Agent ? (y/n)  ") 
					if(returnVAl=='y' or returnVAl=='Y'):
						addNewAmbariAgent()
				else:
					logWrite(log_file,"!!!! WARNING : You must complete ssh-keygen installation step before this procces !!!!")

				time.sleep(5)
			elif returnVAl=="8" : 		### Force Menu State Passive
				returnVAl=raw_input("		!!! Are You sure to some menu state to 'Done' ? (y/n)  ") 
				if(returnVAl=='y' or returnVAl=='Y'):
					forceMenuStatetoDone(0)
					returnVAl=raw_input("		!!! Please Select Menu : ") 
					if(returnVAl=="1"):
						forceMenuStatetoDone(1)
						returnVAl=raw_input("		!!! Please Select Sub Menu : ") 
						if(returnVAl=="1" or returnVAl=="2" or returnVAl=="3" or returnVAl=="4" or returnVAl=="5" or returnVAl=="6"):
							menuMainAPIPassive.append(returnVAl)
							print(bcolors.WARNING +"\n 	Menu state changed to 'Done'"+bcolors.ENDC)
						elif(returnVAl=="7"):
							menuMainAPIPassive.append("1")
							menuMainAPIPassive.append("2")
							menuMainAPIPassive.append("3")
							menuMainAPIPassive.append("4")
							menuMainAPIPassive.append("5")
							menuMainAPIPassive.append("6")
							menuMainPassive.append("1")
							print(bcolors.WARNING +"\n 	Menu state changed to 'Done'"+bcolors.ENDC)
						elif(returnVAl=="8"):
							MenuState=4
						else:
							print(bcolors.WARNING +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC)
							time.sleep(3)

					elif(returnVAl=="2"):
						forceMenuStatetoDone(2)
						returnVAl=raw_input("		!!! Please Select Sub Menu : ") 
						if(returnVAl=="1" or returnVAl=="2" or returnVAl=="3"):
							menuMainASIPassive.append(returnVAl)
							print(bcolors.WARNING +"\n 	Menu state changed to 'Done'"+bcolors.ENDC)
						elif(returnVAl=="4"):
							menuMainASIPassive.append("1")
							menuMainASIPassive.append("2")
							menuMainASIPassive.append("3")
							menuMainPassive.append("2")
							print(bcolors.WARNING +"\n 	Menu state changed to 'Done'"+bcolors.ENDC)
						elif(returnVAl=="5"):
							MenuState=4
						else:
							print(bcolors.WARNING +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC)
							time.sleep(3)

					elif(returnVAl=="3"):
						forceMenuStatetoDone(3)
						returnVAl=raw_input("		!!! Please Select Sub Menu : ") 
						if(returnVAl=="1" or returnVAl=="2" or returnVAl=="3"):
							menuMainACIPassive.append(returnVAl)
						elif(returnVAl=="4"):
							menuMainACIPassive.append("1")
							menuMainACIPassive.append("2")
							menuMainACIPassive.append("3")
							menuMainPassive.append("3")
						elif(returnVAl=="5"):
							MenuState=4
						else:
							print(bcolors.WARNING +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC)
							time.sleep(3)
					elif(returnVAl=="4"):
						MenuState=4
					else:
						print(bcolors.WARNING +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC)
						time.sleep(3)

			elif returnVAl=="9" : 		### Main Menu 
				listAmbariCluster() 
				MenuState=4

			elif returnVAl=="10" : 		### Main Menu 
				print "your Choise : "+returnVAl+" --- You are going to Main Menu ..." 
				MenuState=0
			elif returnVAl=="11" : 		### Exit
				print "your Choise : "+returnVAl
				print("\n Goodbye") 
				exitControl()
			else :
				print(bcolors.WARNING +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC)
				time.sleep(5)
			time.sleep(3)
		elif ans=="5":
			returnVAl=raw_input("		!!! Are You sure to Launch Rocket Installation ? (y/n)  ") 
			if(returnVAl=='y' or returnVAl=='Y'):
				if(len(menuMainAPIPassive)==0 and len(menuMainASIPassive)==0 and len(menuMainACIPassive)==0):
					print(bcolors.WARNING +"\n		!!!BE CAREFULL!!! THE ROCHET is LAUNCHING..."+bcolors.ENDC)
					sleep(3)
					print(bcolors.WARNING +"\n------------	STEP  1.1 : SSH Configurator  -----------"+bcolors.ENDC)
					sleep(2)
					for aClient in ambari_clients:
						if(aClient[0]==ambari_server[0]):
							os.system("ssh-keygen")
							os.system("cp /root/.ssh/id_rsa /root/ambariKEY")
							sshKeyCopier(aClient[0])
						else:
							sshKeyGenetor(aClient[0])
							sshKeyCopier(aClient[0])
					menuMainAPIPassive.append('1')

					print(bcolors.WARNING +"\n------------	STEP  1.2 : SELinux Configurator  -----------"+bcolors.ENDC)
					sleep(2)
					for aClient in ambari_clients:
						if(aClient[0]==ambari_server[0]):
							os.system('echo "SELINUX=disabled" > /etc/selinux/config')
							os.system('ssh setenforce 0')
						else:
							DisableSelinux(aClient[0])
					menuMainAPIPassive.append('2')

					print(bcolors.WARNING +"\n------------	STEP  1.3 : Host File Updater -----------"+bcolors.ENDC)
					sleep(2)
					hostFileUpdater()
					hostFileCoppier()
					menuMainAPIPassive.append('3')	

					print(bcolors.WARNING +"\n------------	STEP  1.4 : Ambari Repo Download  -----------"+bcolors.ENDC)
					sleep(2)
					repoDownloader()
					for aClient in ambari_clients:
						repoCoppier(aClient[0],aClient[2])			
						time.sleep(10)
					os.system("rm -f *.repo")
					menuMainAPIPassive.append('4')

					print(bcolors.WARNING +"\n------------	STEP  1.5 : Yum Update  ----------------------"+bcolors.ENDC)
					print(bcolors.WARNING +"\n------------------  !!! BE PATIENT !!! This process would be takes some times --------------------"+bcolors.ENDC)
					sleep(2)
					for aClient in ambari_clients:
						if(aClient[0]==ambari_server[0]):
							yumUpdaterMaster()
						else:
							yumUpdater(aClient[0])
					menuMainAPIPassive.append('5')	
					sleep(int(yum_update_wait_time))

					print(bcolors.WARNING +"\n------------	STEP  1.6 : Yum Installer  -----------"+bcolors.ENDC)
					sleep(2)
					for aClient in ambari_clients:
						if(aClient[0]==ambari_server[0]):
							yumInstallerMaster(yum_list)
						else:
							yumInstaller(aClient[0],yum_list)
					menuMainAPIPassive.append('6')

					print(bcolors.WARNING +"\n------------	PRE-INSTALLATION PROCESS WAS COMPLETED.  -----------"+bcolors.ENDC)
					sleep(10)

					print(bcolors.WARNING +"\n------------	STEP  2.1 : Ambari Server Pre-Installer  -----------"+bcolors.ENDC)
					sleep(2)
					if(len(menuMainAPIPassive)==menuMainAPIMax):
						ambariServerFirewallPortOpener()
						ambariServerStartPreService()
						menuMainASIPassive.append('1')
					else:
						print "!!! Sorry You won't install Ambari Server until complete 'Ambari Pre-Installation proccess'  "
					time.sleep(5)



					print(bcolors.WARNING +"\n------------	STEP  2.2 : Ambari Server Database Installer  -----------"+bcolors.ENDC)
					sleep(2)
					if(len(menuMainAPIPassive)==menuMainAPIMax):
						pgInstaller(postgres_version)
						time.sleep(10)
						menuMainASIPassive.append('2')					
					else:
						print "!!! Sorry You won't install Ambari Server until complete 'Ambari Pre-Installation proccess'  "
					time.sleep(5)

					print(bcolors.WARNING +"\n------------	STEP  2.3 : Ambari Server Installer   -----------"+bcolors.ENDC)
					sleep(2)
					if(len(menuMainAPIPassive)==menuMainAPIMax):
						ambariServerPackageInstaller()
						ambariServerConfigurator()
						time.sleep(10)
						menuMainASIPassive.append('3')
					else:
						print "!!! Sorry You won't install Ambari Server until complete 'Ambari Pre-Installation proccess'  "
					nodeListGenerator()
					time.sleep(5)

					print(bcolors.WARNING +"\n------------	AMBARI SERVER INSTALLATION PROCESS WAS COMPLETED.  -----------"+bcolors.ENDC)

					print(bcolors.WARNING +"\n------------	STEP  3.1 : Ambari Client Installer  -----------"+bcolors.ENDC)
					sleep(2)
					if(len(menuMainASIPassive)==menuMainASIMax):
						for aClient in ambari_clients:
							ambariAgentPackageInstaller(aClient[0])
						menuMainACIPassive.append('1')
					else:
						print "!!! Sorry You won't install Ambari Clients until complete 'Ambari Server Installation'  "
					time.sleep(5)

					print(bcolors.WARNING +"\n------------	STEP  3.2 : Ambari Agent Configurator  -----------"+bcolors.ENDC)
					sleep(2)
					if(len(menuMainASIPassive)==menuMainASIMax):
						ambariAgentConfigurator()
						menuMainACIPassive.append('2')
					else:
						print "!!! Sorry You won't install Ambari Clients until complete 'Ambari Server Installation'  "
					time.sleep(5)

					print(bcolors.WARNING +"\n------------	STEP  3.3 : Ambari Agent Service Start  -----------"+bcolors.ENDC)
					sleep(2)
					if(len(menuMainASIPassive)==menuMainASIMax):
						for aClient in ambari_clients:
							ambariAgentStartService(aClient[0],aClient[2])
						menuMainACIPassive.append('3')
					else:
						print "!!! Sorry You won't install Ambari Clients until complete 'Ambari Server Installation'  "
					time.sleep(5)
					print(bcolors.WARNING +"\n------------	AMBARI AGENTS INSTALLATION PROCESS WAS COMPLETED.  -----------"+bcolors.ENDC)

					print(bcolors.WARNING +"\n------------	ROCKET INSTALLATION WAS COMPLETED.  -----------"+bcolors.ENDC)
					print(bcolors.WARNING +"\n------------	GO Ambari web interface.  http://"+ambari_server[0]+":8080  -----------"+bcolors.ENDC)
				else:
					print(bcolors.WARNING +"\n		 !!! Sorry. For 'Launch Rocket Installation',you  have  to have started any installation process yet.  "+bcolors.ENDC)
					sleep(8)
			elif(returnVAl=='n' or returnVAl=='N'):
				print "your Choise : "+returnVAl
				sleep(3)
			else : 
				print "	!!!Wrong Coise!!!\n your Choise : "+returnVAl
			MenuState=0
		elif ans=="6":
			returnVAl=raw_input("		!!! do you want to run command for all cluster ? (y/n)  ")
			if(returnVAl=='y' or returnVAl=='Y'):
				returnCMD=raw_input("		Please enter command :")
				for aClient in ambari_clients:
					terminalCommand(str(aClient),returnCMD)
				returnCMD=raw_input("		Go Main Menu :")
			elif(returnVAl=='n' or returnVAl=='N'):
				returnCMD=raw_input("		Please enter command :  ")
				for aClient in ambari_clients:
					returnValSingle=raw_input("		!!! do you want to run this command for server "+str(aClient)+" ? (y/n - Default N) ")
					if(returnValSingle=='y' or returnValSingle=='Y'):
						terminalCommand(str(aClient),returnCMD)
				returnCMD=raw_input("	--> Go Main Menu ")
			else:				
				print "	!!!Wrong Coise!!!\n your Choise : "+returnVAl
			sleep(3)
			MenuState=0


		elif ans=="7":
			print("\n Goodbye") 
			exitControl()
		else:
			print(bcolors.WARNING +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC) 
		
main()

