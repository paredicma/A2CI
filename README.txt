
##################### AMBARI AUTO CLUSTER INSTALLER ############
## Author			: Mustafa YAVUZ 
## E-mail			: mustafa.yavuz
## Version			: 1.0
## Date				: 27.04.2017
## OS System 			: Redhat/Centos 6 and 7
## Software Requirement		: Python 2.6 for Centos 6, Python 2.7 for Centos 7, sshd 
##################### AMBARI AUTO CLUSTER INSTALLER ############

This program is developed for Ambari server and agents installation to make faster and easier. With This program , You can also make some configuration settings (Such as yum installation,firewall configuration).  This program was tested for Hortonworks ambari installation proccess. This program also  require to internet connection or local repo connection.

It is be required to  be installed Centos/Redhat 6 linux and be arranged ip address on entire cluster servers.

Note : You can use only postgresql database for ambari server. If you set ' Embedded Postgres = "True" ' You must choose embedded database installation ( option:  1) while ambari server installation process. Otherwise, you must chose postgresql installltion (option :4 ) while ambari server installation process.


## Getting Started

Download ambariAutoClusterLinux.tar.gz file only ambari server machine. And you must use this server for all installation step.


## Installation :

# 1 - Connect ambari server :

# 2 - Extract ambari gzip file

root# tar -xvf ambariAutoClusterLinux7.tar.gz

# 3 - go directory

root# cd ambariAutoClusterRHEL6

# 4 - Configure ambari cluster paramaters or use "Change ACI Config file parameter" option on the program (Main menu option: 4, Sub menu option: 5 )

root# vi config.py

# 5 - run program

root# python installAC.py

