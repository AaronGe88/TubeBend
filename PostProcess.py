# -*- coding: utf-8 -*- 
_metaclass_ = type
class PostProcess:
	def _init_(self):
		self.odb=None
		self.part = None
	def setOdb(self,jobname):
		from odbAccess import *
		self.odb=openOdb(path=jobname+'.odb')
	def setPart(self,partname):
		from abaqus import *
		from abaqusConstants import *
		self.part=self.odb.rootAssembly.instances[partname]
		
	def output(self,args):
		from abaqus import *
		from abaqusConstants import *
		pass
	
	
		
		