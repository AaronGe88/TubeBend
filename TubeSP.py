from Springback import *
class TubeSP(Springback):
	def setModel(self):
		a = self.model.rootAssembly
		features = a.features.keys()
		for ii in features:
			if ii != 'Part-Tube-1':
				a.deleteFeatures((ii,))
		inter = self.model.interactions.keys()
		self.model.interactions.delete(inter)
		cons = self.model.constraints.keys()
		self.model.constraints.delete(cons)
		
		loads = self.model.loads.keys()
		for ii in loads:
			del self.model.loads[ii]
		bound = self.model.boundaryConditions.keys()
		self.model.boundaryConditions.delete(bound)
		
		sects = len(a.sectionAssignments)
		for ii in range(sects):
			del a.sectionAssignments[sects-1-ii]
	def stepSetup(self):
		del self.model.steps['Step-2']
		self.model.StaticStep(name='Step-1', previous='Initial', 
			maintainAttributes=True, nlgeom=ON)
	
	def setLoadBC(self):
		a = self.model.rootAssembly
		e1 = a.instances['Part-Tube-1'].edges
		edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
		region = a.Set(edges=edges1, name='Set-TubeEnd')
		self.model.EncastreBC(name='BC-1', createStepName='Initial', 
			region=region, localCsys=None)
		instances=(self.model.rootAssembly.instances['Part-Tube-1'], )
		jobname = 'Job-'+self.modelname
		self.model.InitialState(updateReferenceConfiguration=ON, 
			fileName=jobname, endStep=LAST_STEP, endIncrement=STEP_END, 
			name='Predefined Field-1', createStepName='Initial', 
			instances=instances)

		
