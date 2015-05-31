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
		#firstFrame = self.step.frames[0]
		#firstCoords = firstFrame.fieldOutputs['COORD']
		nodes = []
		bendR = args['bendR']
		outDiameter = args['outDiameter']
		meshSize = args['meshSize']
		
		instance = self.odb.rootAssembly.instances['PART-TUBE-1']
		coords=self.frame.fieldOutputs['COORD']
		ends=self.part.nodeSets['SET-END']
		heads=self.part.nodeSets['SET-HEAD']
		end=coords.getSubset(region=ends)
		head=coords.getSubset(region=heads)
		tubeCoords = coords.getSubset(region=instance)
		
		for v in end.values:
			self.endSection[v.nodeLabel]=[v.data[0],v.data[1],v.data[2]]
		for v in head.values:
			self.headSection[v.nodeLabel]=[v.data[0],v.data[1],v.data[2]]
		sth = args['thickness']
		minTh = None
		
		thickness = self.frame.fieldOutputs['STH']
		tubeTh = thickness.getSubset(region=instance)
		for t in tubeTh.values:
			if not minTh or minTh.data > t.data:
				minTh = t
		for cc in tubeCoords.values:
			if cc.data[1] > - meshSize/2 and cc.data[1]< meshSize/2 and cc.data[0] > -bendR and cc.data[2] > 0:		
				nodes.append(cc)
		xs = []
		for ii in nodes:
			xs.append(ii.data[0])

		xs.sort()
		wrinkle = None
		if xs[-1] - xs[0] > sth/2:
			wrinkle = True
		else:
			wrinkle = False
		return self.endSection,self.headSection,minTh.data,wrinkle
# shapes={'bendR':220,'outDiameter':40}		
# BC = {'angle':0.5}	
# tb = TBPost('Model-40-1')
# tb.setPart('PART-TUBE-1')
# tb.output(BC)		