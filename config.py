#-*- coding: utf-8 -*-
import sys
import string
from time import *
import os
import re
import commands
##################PARAMETERS################################
######## for Redhat6/Centos6 = C6, for Redhat7/Centos7  = C7
silent_mode = "false"
domain_name = "test"
ambari_server = ["172.16.196.132","acimaster","C6"]
ambari_clients= [["172.16.196.132","acimaster","C6"],["172.16.196.133","acic1","C6"],["172.16.196.134","acic2","C6"]]
java_rpm = "http://download.oracle.com/otn-pub/java/jdk/8u112-b15/jdk-8u112-linux-x64.rpm"
ambari_repo6 = "http://public-repo-1.hortonworks.com/ambari/centos6/2.x/updates/2.4.0.1/ambari.repo"
hdp_repo6 = "http://public-repo-1.hortonworks.com/HDP/centos6/2.x/updates/2.5.0.0/hdp.repo"
ambari_repo7 = "http://public-repo-1.hortonworks.com/ambari/centos7/2.x/updates/2.4.2.0/ambari.repo"
hdp_repo7 = "http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.4.2.0/hdp.repo"
isEmbeddedPostgres = "True"
postgres_repo_rpm = "pgdg-centos96-9.6-3.noarch.rpm"
postgres_repo = "https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-6-x86_64/"+postgres_repo_rpm
postgres_version = "96" 
pg_bindir = "/usr/pgsql-9.6/bin/"
pg_service = "postgresql-9.6"
pg_hba_file = "/var/lib/pgsql/9.6/data/pg_hba.conf"
pg_conf_file = "/var/lib/pgsql/9.6/data/postgresql.conf"
pg_data_dir = "/var/lib/pgsql/9.6/data/"
pg_ambari_preScript = "ambariPG.sql"
pg_ambari_Dir =  "/var/lib/ambari-server/resources/"
pg_ambari_Script = "Ambari-DDL-Postgres-CREATE.sql"
log_file = "/var/log/ACI.log"
yum_list = " mlocate wget php ntpdate ntp firewalld "
aServer_open_tcp_port_list =["8080/tcp","8040/tcp","8041/tcp","8440/tcp","8441/tcp","8670/tcp","123/udp"]
aAgent_open_tcp_port_list =["8080/tcp","8040/tcp","8041/tcp","8670/tcp","50111/tcp"]
control_file = "/etc/ACI.wait"
req_python_version = "2.7"
req_java_version = "1.8"
yum_update_wait_time ="350"
FQDN_file = "/root/FQDNList.txt"
