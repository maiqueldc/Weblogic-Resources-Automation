import os
from inspect import getsourcefile
from java.io import FileInputStream
from java.util import Properties
 
### Begin WLST Functions ###
def loadProperties(fileName):
	myProperties = Properties()
	input = FileInputStream(fileName)
	myProperties.load(input)
	input.close()
	myProperties = removeWhiteSpace(myProperties)
	result = {}
	level = 1
	tag1 = ''
	tag2 = ''
	tag3 = ''
	for entry in myProperties.entrySet():
		arrKey = entry.key.split('.')
		qtdKey = len(arrKey)
		for key in arrKey:
			if level == 1:
				if level == qtdKey:
					result[key] = entry.value
				elif key not in result.keys():
					result[key] = {}
				tag1 = key
				pass
			elif level == 2:
				if level == qtdKey:
					result[tag1][key] = entry.value
				elif key not in result[tag1].keys():
					result[tag1][key] = {}
				tag2 = key
				pass
			elif level == 3:
				if level == qtdKey:
					result[tag1][tag2][key] = entry.value
				elif key not in result[tag1][tag2].keys():
					result[tag1][tag2][key] = {}
				tag3 = key
				pass
			level += 1
		level = 1
	print ''
	return result
	
# trim (remove white spaces, tabs, CR e LF do inicio e fim da linha)
def removeWhiteSpace(myProperties):
    row = 0
    for entry in myProperties.entrySet():
		row = row + 1
		strKey = str(entry.key)
		trimKey = strKey.strip(' \t\n\r')
		if len(strKey) != len(trimKey):
				print '  @row ' + str(row) + ': KEY trim(\"' + strKey + '\") = \"' + trimKey + '\"'
				entry.key = trimKey
		strValue = str(entry.value)
		trimValue = strValue.strip(' \t\n\r')
		if len(strValue) != len(trimValue):
				print '  @row ' + str(row) + ': VALUE trim(\"' + strValue + '\") = \"' + trimValue + '\"'
				entry.value = trimValue
    return myProperties
 
def getTargets(targetList):
	targetStrArray = targetList.split(',')
	targetArray = jarray.zeros(len(targetStrArray), ObjectName)
	for i in range(len(targetArray)):
		targetInfo = targetStrArray[i].split(':')
		try:
			targetName = targetInfo[0]
			if targetName.find('UCDSIC') > 0:
				targetName = 'AdminServer'
		except IndexError:
			targetName = 'AdminServer'
		try:
			targetType = targetInfo[1]
		except IndexError:
			targetType = 'Server'
		targetArray[i] = ObjectName('com.bea:Name=' + targetName + ',Type=' + targetType)
	return targetArray
 
def createJMSModule(resource):
	try:
		cd('/JMSSystemResources/' + resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' already exists.'
	except:	
		cd('/')
		cmo.createJMSSystemResource(resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' created.'
 
	### Targets ###
	cd('/JMSSystemResources/' + resource['Name'])
	print '# Setting Targets: ' + resource['Targets']
	set('Targets', getTargets(resource['Targets']))
	return
	
def createJMSServer(resource):
	try:
		cd('/JMSServers/' + resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' already exists.'
	except:
		cd('/')
		cmo.createJMSServer(resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' created.'
	
	### Targets ###
	cd('/JMSServers/' + resource['Name'])
	print '# Setting Targets: ' + resource['Targets']
	set('Targets', getTargets(resource['Targets']))
	return
 
def createJMSSubdeployment(resource):
	try:
		cd('/JMSSystemResources/' + resource['JMSModule'] + '/SubDeployments/' + resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' already exists.'
	except:	
		cd('/JMSSystemResources/' + resource['JMSModule'])
		cmo.createSubDeployment(resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' created.'
	
	### Targets ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/SubDeployments/' + resource['Name'])
	print '# Setting Targets: ' + resource['JMSServer']
	set('Targets', getTargets(resource['JMSServer']))
	return
 
def createConnectionFactory(resource):
	try:
		cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/ConnectionFactories/' + resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' already exists.'
	except:
		cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'])
		cmo.createConnectionFactory(resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' created.'
 
	### JNDI ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/ConnectionFactories/' + resource['Name'])
	print '# Setting JNDI: ' + resource['JNDI']
	cmo.setJNDIName(resource['JNDI'])
 
	### SecurityParams ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/ConnectionFactories/' + resource['Name'] + '/SecurityParams/' + resource['Name'])
	cmo.setAttachJMSXUserId(false)
 
	### ClientParams ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/ConnectionFactories/' + resource['Name'] + '/ClientParams/' + resource['Name'])
	cmo.setClientIdPolicy('Restricted')
	cmo.setSubscriptionSharingPolicy('Exclusive')
	cmo.setMessagesMaximum(1)
 
	### TransactionParams ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/ConnectionFactories/' + resource['Name'] + '/TransactionParams/' + resource['Name'])
	print '# Setting XAConnectionFactoryEnabled: ' + resource['XAConnectionFactoryEnabled']
	if resource['XAConnectionFactoryEnabled'] == 'true':
		cmo.setXAConnectionFactoryEnabled(true)
	else:
		cmo.setXAConnectionFactoryEnabled(false)
		
	### Targets ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/SubDeployments/' + resource['JMSSubdeployment'])
	print '# Setting Targets: ' + resource['JMSServer']
	set('Targets', getTargets(resource['JMSServer']))
	
	### Subdeployment ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/ConnectionFactories/' + resource['Name'])
	print '# Setting Subdeployment: ' + resource['JMSSubdeployment']
	cmo.setSubDeploymentName(resource['JMSSubdeployment'])
	return
 
def createQueue(resource):
	try:
		cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/Queues/' + resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' already exists.'
	except:
		cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'])
		cmo.createQueue(resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' created.'	
 
	### JNDI ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/Queues/' + resource['Name'])
	print '# Setting JNDI: ' + resource['JNDI']
	cmo.setJNDIName(resource['JNDI'])
 
	### DeliveryParamsOverrides ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/Queues/' + resource['Name'] + '/DeliveryParamsOverrides/' + resource['Name'])
	if 'RedeliveryDelay' in resource.keys() and len(resource['RedeliveryDelay']) > 0:
		print '# Setting RedeliveryDelay: ' + resource['RedeliveryDelay']
		cmo.setRedeliveryDelay(int(resource['RedeliveryDelay']))
	if 'TimeToDeliver' in resource.keys() and len(resource['TimeToDeliver']) > 0:
		print '# Setting TimeToDeliver: ' + resource['TimeToDeliver']
		cmo.setTimeToDeliver(resource['TimeToDeliver'])
	if 'TimeToLive' in resource.keys() and len(resource['TimeToLive']) > 0:
		print '# Setting TimeToLive: ' + resource['TimeToLive']
		cmo.setTimeToLive(int(resource['TimeToLive']))
 
	### DeliveryFailureParams ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/Queues/' + resource['Name'] + '/DeliveryFailureParams/' + resource['Name'])
	if 'RedeliveryLimit' in resource.keys() and len(resource['RedeliveryLimit']) > 0:
		print '# Setting RedeliveryLimit: ' + resource['RedeliveryLimit']
		cmo.setRedeliveryLimit(int(resource['RedeliveryLimit']))
	if 'ExpirationPolicy' in resource.keys() and len(resource['ExpirationPolicy']) > 0:
		print '# Setting ExpirationPolicy: ' + resource['ExpirationPolicy']
		cmo.setExpirationPolicy(resource['ExpirationPolicy'])
	if 'ErrorDestinationName' in resource.keys() and len(resource['ErrorDestinationName']) > 0:
		print '# Setting ErrorDestinationName: ' + resource['ErrorDestinationName']
		try:
			cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/Queues/' + resource['ErrorDestinationName'])
			err = getMBean('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/Queues/' + resource['ErrorDestinationName'])
		except:
			cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/Queues/')
			err = create(resource['ErrorDestinationName'], resource['Type'])
			err.JNDIName = resource['ErrorDestinationJNDI']
			err.subDeploymentName = resource['JMSSubdeployment']
		cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/Queues/' + resource['Name'] + '/DeliveryFailureParams/' + resource['Name'])
		cmo.setErrorDestination(err)
 
	### Targets ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/SubDeployments/' + resource['JMSSubdeployment'])
	set('Targets',jarray.array([ObjectName('com.bea:Name=' + resource['JMSServer'] + ',Type=JMSServer')], ObjectName))
	
	### Subdeployment ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/Queues/' + resource['Name'])
	cmo.setSubDeploymentName(resource['JMSSubdeployment'])
	return
 
def createDistributedQueue(resource):
	try:
		cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/UniformDistributedQueues/' + resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' already exists.'
	except:
		cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'])
		cmo.createUniformDistributedQueue(resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' created.'	
 
	### JNDI ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/UniformDistributedQueues/' + resource['Name'])
	print '# Setting JNDI: ' + resource['JNDI']
	cmo.setJNDIName(resource['JNDI'])
 
	### DeliveryParamsOverrides ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/UniformDistributedQueues/' + resource['Name'] + '/DeliveryParamsOverrides/' + resource['Name'])
	if 'RedeliveryDelay' in resource.keys() and len(resource['RedeliveryDelay']) > 0:
		print '# Setting RedeliveryDelay: ' + resource['RedeliveryDelay']
		cmo.setRedeliveryDelay(int(resource['RedeliveryDelay']))
	if 'TimeToDeliver' in resource.keys() and len(resource['TimeToDeliver']) > 0:
		print '# Setting TimeToDeliver: ' + resource['TimeToDeliver']
		cmo.setTimeToDeliver(resource['TimeToDeliver'])
	if 'TimeToLive' in resource.keys() and len(resource['TimeToLive']) > 0:
		print '# Setting TimeToLive: ' + resource['TimeToLive']
		cmo.setTimeToLive(int(resource['TimeToLive']))
 
	### DeliveryFailureParams ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/UniformDistributedQueues/' + resource['Name'] + '/DeliveryFailureParams/' + resource['Name'])
	if 'RedeliveryLimit' in resource.keys() and len(resource['RedeliveryLimit']) > 0:
		print '# Setting RedeliveryLimit: ' + resource['RedeliveryLimit']
		cmo.setRedeliveryLimit(int(resource['RedeliveryLimit']))
	if 'ExpirationPolicy' in resource.keys() and len(resource['ExpirationPolicy']) > 0:
		print '# Setting ExpirationPolicy: ' + resource['ExpirationPolicy']
		cmo.setExpirationPolicy(resource['ExpirationPolicy'])
	if 'ErrorDestinationName' in resource.keys() and len(resource['ErrorDestinationName']) > 0:
		print '# Setting ErrorDestinationName: ' + resource['ErrorDestinationName']
		try:
			cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/UniformDistributedQueues/' + resource['ErrorDestinationName'])
			err = getMBean('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/UniformDistributedQueues/' + resource['ErrorDestinationName'])
		except:
			cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/UniformDistributedQueues/')
			err = cmo.createUniformDistributedQueue(resource['ErrorDestinationName'])
			err.JNDIName = resource['ErrorDestinationJNDI']
			err.subDeploymentName = resource['JMSSubdeployment']
		cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/UniformDistributedQueues/' + resource['Name'] + '/DeliveryFailureParams/' + resource['Name'])
		cmo.setErrorDestination(err)
 
	### Targets ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/SubDeployments/' + resource['JMSSubdeployment'])
	print '# Setting Targets: ' + resource['JMSServer']
	set('Targets', getTargets(resource['JMSServer']))
 
	### Subdeployment ###
	cd('/JMSSystemResources/' + resource['JMSModule'] + '/JMSResource/' + resource['JMSModule'] + '/UniformDistributedQueues/' + resource['Name'])
	cmo.setSubDeploymentName(resource['JMSSubdeployment'])
	return
	
def createJMSSystemResource(resource):
	print '# Creating ' + resource['Type'] + ' with name ' + resource['Name'] + '.'
	
	### JMS Server ###
	if resource['Type'] == 'JMSServer':
		createJMSServer(resource)
 
	### JMS Module ###
	if resource['Type'] == 'JMSModule':
		createJMSModule(resource)
 
	### JMS Subdeployment ###
	if resource['Type'] == 'JMSSubdeployment':
		createJMSSubdeployment(resource)
 
	### Connection Factory ###
	if resource['Type'] == 'ConnectionFactory':
		createConnectionFactory(resource)
	
	### Queue ###
	if resource['Type'] == 'Queue':
		createQueue(resource)
 
	### DistributedQueue ###
	if resource['Type'] == 'DistributedQueue':
		createDistributedQueue(resource)
		
	print '# ' + resource['Type'] + ' with name ' + resource['Name'] + ' has been updated successfully.'
	return
 
def createJMSSystemResources(resources):
	try:
		for index in resources:
			resource = resources[index]
			if len(resource['Type']) > 0 and len(resource['Name']) > 0:
				createJMSSystemResource(resource)
				print ''
	except (Exception), e:
		print '#=== Error: ', e
		dumpStack()
		cancelEdit('y')
	return
 
def createSelfTuningResource(resource):
	cd('/')
	domainName = get('Name')
	print '# Creating resource with name ' + resource['Name'] + '.'
	try:
		cd('/SelfTuning/' + domainName + '/' + resource['Type'] + '/' + resource['Name'])
		print '# Resource with name ' + resource['Name'] + ' already exists.'
	except (Exception), e:
		cd('/SelfTuning/' + domainName + '/' + resource['Type'])
		create(resource['Name'], resource['Type'])
		print '# Resource with name ' + resource['Name'] + ' created.'
 
	### Targets ###
	cd('/SelfTuning/' + domainName + '/' + resource['Type'] + '/' + resource['Name'])
	print '# Setting Targets: ' + resource['Targets']
	set('Targets', getTargets(resource['Targets']))
 
	if 'Count' in resource.keys():
		print '# Setting Count: ' + resource['Count']
		set('Count', resource['Count'])
 
	if 'MinThreadsConstraint' in resource.keys():
		if len(resource['MinThreadsConstraint']) > 0 and resource['MinThreadsConstraint'] != 'None':
			print '# Setting MinThreadsConstraint: ' + resource['MinThreadsConstraint']
			min = getMBean('/SelfTuning/' + domainName + '/MinThreadsConstraints/' + resource['MinThreadsConstraint'])
			cmo.setMinThreadsConstraint(min)
		else:
			print '# Setting MinThreadsConstraint: None'
			cmo.setMinThreadsConstraint(None)
 
	if 'MaxThreadsConstraint' in resource.keys():
		if len(resource['MaxThreadsConstraint']) > 0 and resource['MaxThreadsConstraint'] != 'None':
			print '# Setting MaxThreadsConstraint: ' + resource['MaxThreadsConstraint']
			max = getMBean('/SelfTuning/' + domainName + '/MaxThreadsConstraints/' + resource['MaxThreadsConstraint'])
			cmo.setMaxThreadsConstraint(max)
		else:
			print '# Setting MaxThreadsConstraint: None'
			cmo.setMaxThreadsConstraint(None)
			
	if 'Capacity' in resource.keys():
		if len(resource['Capacity']) > 0 and resource['Capacity'] != 'None':
			print '# Setting Capacity: ' + resource['Capacity']
			capacity = getMBean('/SelfTuning/' + domainName + '/Capacities/' + resource['Capacity'])
			cmo.setCapacity(capacity)
		else:
			print '# Setting Capacity: None'
			cmo.setCapacity(None)
			
	if 'IgnoreStuckThreads' in resource.keys():
		if len(resource['IgnoreStuckThreads']) > 0 and resource['IgnoreStuckThreads'] == 'true':
			print '# Setting IgnoreStuckThreads: ' + resource['IgnoreStuckThreads']
			cmo.setIgnoreStuckThreads(1)
		else:
			print '# Setting IgnoreStuckThreads: false'
			cmo.setIgnoreStuckThreads(0)
	print '# Resource with name ' + resource['Name'] + ' has been updated successfully.'
	return
 
def createSelfTuningResources(resources):
	try:
		for index in resources:
			resource = resources[index]
			if len(resource['Type']) > 0 and len(resource['Name']) > 0:
				createSelfTuningResource(resource)
				print ''
	except (Exception), e:
		print '#=== Error: ', e
		dumpStack()
		cancelEdit('y')
	return
 
### End WLST Functions ###
### Begin Credentials ###
credentialsProperties = loadProperties('credentials.properties')
adminUrl = credentialsProperties['adminUrl']
username = credentialsProperties['username']
password = credentialsProperties['password']
 
### End Credentials ### 
### Begin Load Properties ###
 component = os.path.split(getsourcefile(lambda:0))[1].split('.')[0]
properties = '${p:component.name}'+'.properties'
resourcesProperties = loadProperties(properties)
 
## JMS Resources ##
 
if 'JMSServer' in resourcesProperties.keys():
	jmsServers = resourcesProperties['JMSServer']
 
if 'JMSModule' in resourcesProperties.keys():
	jmsModules = resourcesProperties['JMSModule']
 
if 'JMSSubdeployment' in resourcesProperties.keys():
	jmsSubdeployments = resourcesProperties['JMSSubdeployment']
 
if 'ConnectionFactory' in resourcesProperties.keys():
	connectionFactories = resourcesProperties['ConnectionFactory']
 
if 'Queue' in resourcesProperties.keys():
	queues = resourcesProperties['Queue']
 
if 'DistributedQueue' in resourcesProperties.keys():
	distributedQueues = resourcesProperties['DistributedQueue']
 
if 'DistributedQueue' in resourcesProperties.keys():
	distributedQueues = resourcesProperties['DistributedQueue']
 
## SelfTunning Resources ##
 
if 'MinThread' in resourcesProperties.keys():
	minThreads = resourcesProperties['MinThread']
 
if 'MaxThread' in resourcesProperties.keys():
	maxThreads = resourcesProperties['MaxThread']
 
if 'Capacity' in resourcesProperties.keys():
    capacities = resourcesProperties['Capacity']
 
if 'WorkManager' in resourcesProperties.keys():
	workmanagers = resourcesProperties['WorkManager']
 ### End Load Properties ###
 
 ### Begin WLST Edit Commands ###
try:
	connect(username, password, adminUrl)
	edit()
	startEdit()
 
	if 'jmsServers' in locals():
		createJMSSystemResources(jmsServers)
	if 'jmsModules' in locals():
		createJMSSystemResources(jmsModules)
	if 'jmsSubdeployments' in locals():
		createJMSSystemResources(jmsSubdeployments)
	if 'connectionFactories' in locals():
		createJMSSystemResources(connectionFactories)
	if 'queues' in locals():
		createJMSSystemResources(queues)
	if 'distributedQueues' in locals():
		createJMSSystemResources(distributedQueues)
 
	if 'minThreads' in locals():
		createSelfTuningResources(minThreads)
	if 'maxThreads' in locals():
		createSelfTuningResources(maxThreads)
	if 'capacities' in locals():
		createSelfTuningResources(capacities)
#    if 'capacities' in locals():
#        createSelfTuningResources(capacities)
	if 'workmanagers' in locals():
		createSelfTuningResources(workmanagers)
 
	validate()
	save()
	activate(block='true')
except:
	dumpStack()
	undo('true', 'y')
	stopEdit('y')
	sys.exit(1)
 
sys.exit(0)

### End of WLST ###"