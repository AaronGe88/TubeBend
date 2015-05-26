# -*- coding: utf-8 -*-
from FEA import * 
from TubeSP import TubeSP
from BendAssembly import *
from ProfileFit import *

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
		self.assembly = BendAssembly(self.modelname)
		self.assembly.makeIt(self.shapes,self.material,self.positions,self.inits,\
			2,self.BCs,self.Load,self.meshSize,self.arg)
		# self.springback = TubeSP(self.modelname)
		# self.springback.makeIt()
	def doJobs(self):
		pass
	def getResults(self):
		pass
		
		
tools = [7.85e-9,210000.0,.3]
parts = [7.85e-9,210000.0,.3,750.0,.06,.24,1.0]		

paramFile = open('result.txt','a+')
paramFile.write('Out R Thick E K n angle springback\n')
paramFile.close()
for jj in range(65,67,2):
	for ii in range (1,2):
		modelname='Model-'+str(jj)+'-'+str(ii)
		t = TBFEA(modelname)
		inits={'0.5':.5,'0.125':.125}
		arg={'assist':1.0,'mandralOut':3.,'ball2ball':20.}
		Load={'Press':30000}
		out = float(jj)
		shapes = {'bendR':200.0,'outDiameter':out,'thick':3.5,'toolGap':0.1,'ballGap':1.0,'ballThick':20.}
		BCs={'angle':ii * 15.0/180.0*pi,'close':shapes['outDiameter']/2}
		
		positions = {'clamp':(-BCs['close'],0,-shapes['bendR']+shapes['outDiameter']/2),'insert':(.0,0.,-shapes['bendR']+shapes['outDiameter']/2),\
			'press':(-BCs['close'],0.,0.),\
			'tube':(0,0,-shapes['bendR']-shapes['outDiameter']/2),'ball':(-shapes['bendR'],0,-arg['ball2ball']-arg['mandralOut']-shapes['ballThick']/2),\
			'mandral':(0,0,-arg['mandralOut']),'wiper':0.5}
		material={'tool':tools,'part':parts}
		meshSize = {'pressDie':shapes['thick']*3/0.6,'tube':shapes['thick']/0.6 * 2}
		t.setParameter(shapes,material,positions,inits,\
			2,BCs,Load,meshSize,arg)
		t.setModels()
		#t.doJobs()
		# modelsp=modelname+'-SP'
		# init=solveArray(modelname,0)
		# springback=solveArray(modelsp,0)
		# strR =str(int(shapes['bendR']))
		# strOut=str(int(shapes['outDiameter']))
		# strThick=str(int(shapes['thick']*100))
		# strA=str(int(arg['assist']*10))
		# strK=str(int(parts[3]))
		# strN=str(int(parts[5]*100))
		# paramFile = open('result.txt','a+')
		# paramFile.write('%10.6E %10.6E %10.6E %10.6E %10.6E %10.6E %10.6E %10.6E\n'%(shapes['bendR'],shapes['outDiameter'],shapes['thick']\
			# ,parts[1],parts[3],parts[5],init,springback))
		# paramFile.close()