# -*- coding: utf-8 -*-
from FEA import * 
_metaclass_ = type
class TBFEA(FEA):
	def setParameter(self,shapes,materials,positions,inits,\
		steps,BCs,Loads,meshSize,args):	
		self.shapes = shapes#{'bendR':220.0,'outDiameter':40.0,'thick':1.0,'mandralGap':.8,'toolGap':0.1,'ballThick':10.0,}
		self.positions = positions#{'insert':(0,0,-200),'tube':(0,0,-240),'ball':(-shapes['bendR'],0,-12),'mandral':(0,0,0),'wiper':0.5}
		self.material=materials
		self.meshSize = meshSize
		self.inits=inits
		self.arg=args
		self.Load=Loads
		self.BCs=BCs
		self.steps = steps
	def setModels(self):
		from BendAssembly import BendAssembly
		from TubeSP import TubeSP
		self.assembly = BendAssembly(self.modelname)
		self.assembly.makeIt(self.shapes,self.material,self.positions,self.inits,\
			1,self.BCs,self.Load,self.meshSize,self.arg)
		self.springback = TubeSP(self.modelname)
		self.springback.makeIt()
	def doJobs(self):
		pass
	def getResults(self):
		from TBPost import *
		
tools = [7.85e-9,210000.0,.3]
parts = [7.85e-9,210000.0,.3,750.0,.06,.24,1.0]		
shapes = {'bendR':220.0,'outDiameter':40.0,'thick':1.0,'mandralGap':.8,'toolGap':0.1,'ballThick':10.0,}
positions = {'insert':(0,0,-200),'tube':(0,0,-240),'ball':(-shapes['bendR'],0,-12),'mandral':(0,0,0),'wiper':0.5}
material={'tool':tools,'part':parts}
meshSize = {'pressDie':3.0/0.6,'tube':1.0/0.6 * 2}
inits={'0.5':.5,'0.125':.125}
arg={'assist':.8}
Load={'Press':30000}
BCs={'angle':1.2}
t = TBFEA('Model-2')
t.setParameter(shapes,material,positions,inits,\
		1,BCs,Load,meshSize,arg)
t.setModels()
t.doJobs()