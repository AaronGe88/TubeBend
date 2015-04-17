# -*- coding: utf-8 -*- 
_metaclass_ = type
INDEX = 0
class Assembly:
	def _init_(self):
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
		Mdb()
		global INDEX
		self.modelname = 'Model-' +str(INDEX)
		mdb.models.changeKey(fromName='Model-1', toName='Model-'+str(INDEX))
		model = mdb.models[self.modelname]
		self.model = model
		self.tools = []
		self.innertools=[]
		self.parts = []
	def setupShapes(self,shapes):
		self.shapes = shapes
		
	def setupMaterials(self,materials):
		pass
	def addInstance(self):
		pass
	def setPositions(self,positions,args):
		pass
	
	def toolsRigid(self,args):
		for instance in self.tools:
			a = self.model.rootAssembly
			region2=a.instances[instance.partName+'-1'].sets['Set-Body']
			a = self.model.rootAssembly
			region1=a.instances[instance.partName+'-1'].sets['Set-RP']
			self.model.RigidBody(name='RIGID-'+ instance.partName, refPointRegion=region1, 
				bodyRegion=region2)
				
		for instance in self.innertools:
			a = self.model.rootAssembly
			region2=a.instances[instance.partName+'-1'].sets['Set-Body']
			a = self.model.rootAssembly
			region1=a.instances[instance.partName+'-1'].sets['Set-RP']
			self.model.RigidBody(name='RIGID-'+ instance.partName, refPointRegion=region1, 
				bodyRegion=region2)
				
	def interactions(self,inits,args):
		pass
	
	def stepSetup(self, steps,args):
		from step import *
		self.model.ExplicitDynamicsStep(name='Step-1', previous='Initial', 
			massScaling=((SEMI_AUTOMATIC, MODEL, AT_BEGINNING, 10000.0, 0.0, None, 
			0, 0, 0.0, 0.0, 0, None), ))
		self.model.fieldOutputRequests['F-Output-1'].setValues(variables=(
			'S', 'SVAVG', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 'V', 'A', 
			'RF', 'CSTRESS', 'EVF', 'STH', 'COORD'))
		for ii in range(2,steps+1):
			self.model.ExplicitDynamicsStep(name='Step-'+str(ii), previous='Step-'+str(ii-1))

	def setBC(self,BCs):
		pass
		
	def setLoads(self,loads):
		pass
		
	def makeAssembly(self,shapes,materials,positions,inits,steps,BCs,Loads,args):
		self._init_()
		self.setupShapes(shapes)
		self.setupMaterials(tools[0],parts[1])
		self.setPositions(positions)
		self.interactions(inits)
		self.stepSetup(steps)
		self.setBC(BCs,args[0])
		self.setLoads(Loads)
	def submitJob(self):
		from job import *
		jobname = 'Job-'+self.modelname
		mdb.Job(name=jobname, model=self.modelname, description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, 
        nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
        contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
        resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=1, 
        activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)
		mdb.jobs[jobname].submit(consistencyChecking=OFF)
		mdb.jobs[jobname].waitForCompletion()
		global INDEX
		INDEX = INDEX + 1