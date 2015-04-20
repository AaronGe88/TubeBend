# -*- coding: utf-8 -*- 
from PostProcess import *
class TBPost(PostProcess):
	def _init_(self):
		PostProcess._init_(self)
		self.wrArea ={}
		self.elements ={}
	def output(self,args):
		zBound = (0,100)
		bendR = args['bendR']
		outDiameter = args['outDiameter']
		xBound = [-bendR+outDiameter/2-20,-bendR+outDiameter/2+20]
		for node in self.part.nodes:
			if zBound[0]<node.coordinates[2]<zBound[1] \
				and xBound[0]<node.coordinates[0]<xBound[1]\
				and -1.7<node.coordinates[1]<1.7:
				self.wrArea[node.label]=[node.coordinates[0],node.coordinates[1],node.coordinates[2]]
		print self.wrArea
shapes={'bendR':220,'outDiameter':40}			
tb = TBPost()
tb._init_()
tb.setOdb('Job-1')
tb.setPart('PART-TUBE-1')
tb.output(shapes)		