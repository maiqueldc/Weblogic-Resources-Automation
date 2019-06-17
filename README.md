# Weblogic-Resources-Automation<p>
 This script were deployed with assistance from Rafael Guterres, Vinicius Cagnini & Maiquel Oliveira<br>
 This script can run and create principal Weblogic Resources, avoiding operational steps. It was used to create recoursive objects<br>
 It's very nice when you need create > 10 resources on some Weblogic Domain. This scripts can help in DevOps initiatives.<br>
 The Weblogic 'hierarchy' should be understood for correctly runs.<br>
 First version was copied from internet and improved new features<br>

	JMSServer
	JMSModule
	JMSSubdeployment
	ConnectionFactory
	MinThreadsConstraints
	MaxThreadsConstraints
	WorkManagers
	DistributedQueue
	Queue

<p>#Applyed for:<br>
•	Oracle WebLogic Server 11g<br>
•	Oracle WebLogic Server 12cR1<br>
•	Oracle WebLogic Server 12cR2<br>

<p>#Usage:      <br>
export WL_HOME<br> or run setDomainEnv.sh at weblogic domain/bin folder<br>
           Then, type:  Weblogic-binaries-folder/common/bin/wlst.sh CreateWeblogicResources.py<br>
