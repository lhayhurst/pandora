#!/usr/bin/python
import fileinput, sys, os, random

#mapSizes = ['400','800','1600']
mapSizes = ['1600']

numExecutions = 2
numHGs = ['100']
controllers = ['DecisionTree']
#controllers = ['DecisionTree', 'MDP', 'Random']
#biomassDistributions = ['standard', 'logDecayFromWater', 'linDecayFromWater']
biomassDistributions = ['linDecayFromWater']

xmlTemplate = 'templates/config_template_local.xml'

mapSizeKey = 'MAPSIZE'
numHGKey = 'NUMHG'
controllerKey = 'CTYPE'

indexKey = 'INDEX'
initialDirKey = 'INITIALDIR'
numExecutionKey = 'NUMEXEC'

climateKey = 'CLIMATESEED'
biomassDistributionKey = 'BIOMASS_DISTRIBUTION'


def replaceKey( fileName, key, value ):
	for line in fileinput.FileInput(fileName,inplace=1):
		if key in line:
			line = line.replace(key, value)
		sys.stdout.write(line)
	fileinput.close()

os.system('rm -rf results_*')

index = 0
print 'creating test workbench'

random.seed()

for numExecution in range(0,numExecutions):
	# each n.execution  has the same seed in all parameter space
	randomValue = str(random.randint(0,10000000))
	for mapSize in mapSizes:
		for numHG in numHGs:
			for controller in controllers:
				for biomassDistribution in biomassDistributions:
					print 'creating gujarat instance: ' + str(index) + ' for map: ' + mapSize + ' numHG: ' + numHG + ' with controller: ' + controller + ' biomass distribution: ' + biomassDistribution + ' and execution: ' + str(numExecution)
					dirName = 'results_size'+mapSize+'_numHG'+numHG+'_controller_'+controller+'_biodist_'+biomassDistribution+'_ex'+str(numExecution)
					os.system('mkdir '+dirName)
					configName = dirName + '/config.xml'			
					os.system('cp '+xmlTemplate+' '+configName)
					replaceKey(configName, mapSizeKey, mapSize)
					replaceKey(configName, biomassDistributionKey, biomassDistribution)
					replaceKey(configName, numHGKey, numHG)
					replaceKey(configName, controllerKey, controller)
					replaceKey(configName, climateKey, randomValue)
					replaceKey(configName, numExecutionKey, str(numExecution))

					index += 1

print 'workbench done, submitting tasks'
index = 0
for mapSize in mapSizes:
	for numHG in numHGs:
		for controller in controllers:
			for biomassDistribution in biomassDistributions:
				for numExecution in range(0,numExecutions):
					print 'submitting gujarat instance: ' + str(index) + ' for map: ' + mapSize + ' numHG: ' + numHG + ' with controller: ' + controller + ' and execution: ' + str(numExecution)
					dirName = 'results_size'+mapSize+'_numHG'+numHG+'_controller_'+controller+'_biodist_'+biomassDistribution+'_ex'+str(numExecution)
					os.system('../gujarat '+dirName+'/config.xml >'+dirName+'/gujarat.log 2>'+dirName+'/gujarat.err &')
					index += 1

