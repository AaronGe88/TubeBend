from Springback import *
class TubeSP(Springback):
	def setModel(self):
		a = self.model.rootAssembly
		a.deleteFeatures(('Part-Insert-1', 'Part-RecifyClamp-1', 'Part-BendDie-1', 
			'Part-Wiper-1', 'Part-RecifyPress-1', ))
		self.model.interactions.delete(('Int-0', 'Int-1', 'Int-2', 
			'Int-3', 'Int-4', ))
		self.model.constraints.delete(('RIGID-Part-BendDie', 
			'RIGID-Part-RecifyClamp', 'RIGID-Part-Insert', 'RIGID-Part-RecifyPress', 
			'RIGID-Part-Wiper', 'Tie-1', ))
		del self.model.loads['Load-1']
		self.model.boundaryConditions.delete(('BC-Bend', 'BC-Press', 
			'BC-Wiper','BC-Clamp' ))
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

		
