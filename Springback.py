# -*- coding: utf-8 -*-
from part import *
from section import *
from regionToolset import *
from displayGroupMdbToolset import *
from part import *
from material import *
from assembly  import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from xyPlot import *
from connectorBehavior import * 
_metaclass_ = type
class Springback:
	def __init__(self,modelname):
		from part import *
		from section import *
		from regionToolset import *
		from displayGroupMdbToolset import *
		from part import *
		from material import *
		from assembly  import *
		from step import *
		from interaction import *
		from load import *
		from mesh import *
		from optimization import *
		from job import *
		from sketch import *
		from visualization import *
		from xyPlot import *
		from connectorBehavior import *
		self.modelname = modelname
		spmodel = self.modelname+'-SP'
		self.model=mdb.Model(name=spmodel, objectToCopy=mdb.models[modelname])
	def setModel(self):
		pass
	def stepSetup(self):
		pass
	def setLoadBC(self):
		pass
		
	def submitjob(self):
		from job import *
		jobname = 'Job-'+self.modelname+'-SP'
		mdb.Job(name=jobname, model=self.modelname+'-SP', description='', type=ANALYSIS, 
			atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
			memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, 
			nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
			contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
			resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=1, 
			activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)
		mdb.jobs[jobname].submit(consistencyChecking=OFF)
		mdb.jobs[jobname].waitForCompletion()
	def makeIt(self):
		self.setModel()
		self.stepSetup()
		self.setLoadBC()
		self.submitjob()