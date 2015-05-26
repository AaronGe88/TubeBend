# -*- coding: utf-8 -*- 
from PostProcess import *
from part import *
from odbAccess import *
from abaqus import *
from abaqusConstants import *
class TBPost(PostProcess):
	def __init__(self,modelname):
		self.part = None
		self.modelname = modelname
		self.odb=openOdb(path='Job-'+modelname+'.odb')
		self.step=self.odb.steps.values()[-1]
		self.frame=self.step.frames[-1] 
		self.elements ={}
		self.endSection={}
		self.headSection={}
	def output(self,args):
		coords=self.frame.fieldOutputs['COORD']
		ends=self.part.nodeSets['SET-END']
		heads=self.part.nodeSets['SET-HEAD']
		end=coords.getSubset(region=ends)
		head=coords.getSubset(region=heads)
		for v in end.values:
			self.endSection[v.nodeLabel]=[v.data[0],v.data[1],v.data[2]]
		for v in head.values:
			self.headSection[v.nodeLabel]=[v.data[0],v.data[1],v.data[2]]
		
		return self.endSection,self.headSection
# shapes={'bendR':220,'outDiameter':40}		
# BC = {'angle':0.5}	
# tb = TBPost('Model-40-1')
# tb.setPart('PART-TUBE-1')
# tb.output(BC)		