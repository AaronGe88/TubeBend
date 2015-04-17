# -*- coding: utf-8 -*- 
from PartRoot import *
_metaclass_ = type
class Insert(Tool):
	def _init_(self):
		Tool._init_(self)
		self.partName = 'Part-Insert'
		self.friction = .5
	
	def geometry(self):
		from part import CLOCKWISE
		from part import THREE_D
		from part import DEFORMABLE_BODY
		
		bendR = self.shape['bendR']
		outDiameter = self.shape['outDiameter']
		toolGap=self.shape['toolGap']
		self.model.ConstrainedSketch(name='__profile__', sheetSize=200.0)
		self.model.sketches['__profile__'].ArcByCenterEnds(center=(-bendR, 
			0.0), direction=CLOCKWISE, point1=(-bendR, outDiameter/2+toolGap), point2=(-bendR, 
			-outDiameter/2-toolGap))
		self.model.Part(dimensionality=THREE_D, name=self.partName, type=
			DEFORMABLE_BODY)
		self.model.parts[self.partName].BaseShellExtrude(depth=bendR-outDiameter/2, sketch=
			self.model.sketches['__profile__'])
		del self.model.sketches['__profile__']
		
	def outerSurface(self):
		p = self.model.parts[self.partName]
		s = p.faces
		side1Faces = s.getSequenceFromMask(mask=('[#1 ]', ), )
		p.Surface(side1Faces=side1Faces, name='Surf-Outer')

class Clamp(Tool):
	def _init_(self):
		Tool._init_(self)
		self.partName = 'Part-Clamp'
		self.friction = .5
	def geometry(self):
		from part import CLOCKWISE
		from part import THREE_D
		from part import DEFORMABLE_BODY
		bendR = self.shape['bendR']
		outDiameter = self.shape['outDiameter']
		toolGap=self.shape['toolGap']
		self.model.ConstrainedSketch(name='__profile__', sheetSize=200.0)
		self.model.sketches['__profile__'].ArcByCenterEnds(center=(-bendR, 
			0.0), direction=CLOCKWISE, point1=(-bendR, -outDiameter/2 - toolGap), point2=(-bendR, outDiameter/2+toolGap))
		self.model.Part(dimensionality=THREE_D, name=self.partName, type=
			DEFORMABLE_BODY)
		self.model.parts[self.partName].BaseShellExtrude(depth=bendR-outDiameter/2, sketch=
			self.model.sketches['__profile__'])
		del self.model.sketches['__profile__']
	def outerSurface(self):
		p = self.model.parts[self.partName]
		s = p.faces
		side1Faces = s.getSequenceFromMask(mask=('[#1 ]', ), )
		p.Surface(side1Faces=side1Faces, name='Surf-Outer')
	def setRP(self,RP):
		self.RP = RP
		p = self.model.parts[self.partName]
		p.ReferencePoint(point=self.RP)
		r = p.referencePoints
		refPoints=(r[2], )
		p.Set(referencePoints=refPoints, name='Set-RP')

class BendDie(Tool):
	def _init_(self):
		Tool._init_(self)
		self.partName = 'Part-BendDie'
		self.friction = .125
	def geometry(self):
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
		bendR = self.shape['bendR']
		outDiameter = self.shape['outDiameter']
		toolGap=self.shape['toolGap']
		self.model.ConstrainedSketch(name='__profile__', sheetSize=200.0)
		self.model.sketches['__profile__'].ConstructionLine(point1=(0.0, 
			-100.0), point2=(0.0, 100.0))
		self.model.sketches['__profile__'].FixedConstraint(entity=
			self.model.sketches['__profile__'].geometry[2])
		self.model.sketches['__profile__'].ArcByCenterEnds(center=(-bendR, 
			0.0), direction=CLOCKWISE, point1=(-bendR, outDiameter/2 + toolGap), point2=(-bendR, -outDiameter/2-toolGap))
		self.model.Part(dimensionality=THREE_D, name=self.partName, type=
			DEFORMABLE_BODY)
		self.model.parts['Part-BendDie'].BaseShellRevolve(angle=270.0, 
			flipRevolveDirection=OFF, sketch=
			self.model.sketches['__profile__'])
		del self.model.sketches['__profile__']
	def outerSurface(self):
		p = self.model.parts[self.partName]
		s = p.faces
		side1Faces = s.getSequenceFromMask(mask=('[#1 ]', ), )
		p.Surface(side1Faces=side1Faces, name='Surf-Outer')

class Wiper(Tool):
	def _init_(self):
		Tool._init_(self)
		self.partName = 'Part-Wiper'
		self.friction = .5
	
	def geometry(self):
		from part import CLOCKWISE
		from part import THREE_D
		from part import DEFORMABLE_BODY
		
		bendR = self.shape['bendR']
		outDiameter = self.shape['outDiameter']
		toolGap=self.shape['toolGap']
		self.model.ConstrainedSketch(name='__profile__', sheetSize=200.0)
		self.model.sketches['__profile__'].ArcByCenterEnds(center=(-bendR, 
			0.0), direction=CLOCKWISE, point1=(-bendR, outDiameter/2+toolGap), point2=(-bendR, 
			-outDiameter/2-toolGap))
		self.model.Part(dimensionality=THREE_D, name=self.partName, type=
			DEFORMABLE_BODY)
		self.model.parts[self.partName].BaseShellExtrude(depth=6 * outDiameter, sketch=
			self.model.sketches['__profile__'])
		del self.model.sketches['__profile__']
		
	def outerSurface(self):
		p = self.model.parts[self.partName]
		s = p.faces
		side1Faces = s.getSequenceFromMask(mask=('[#1 ]', ), )
		p.Surface(side1Faces=side1Faces, name='Surf-Outer')

class Press(Tool):
	def _init_(self):
		Tool._init_(self)
		self.partName = 'Part-Press'
		self.friction = .5
	def geometry(self):
		from part import CLOCKWISE
		from part import THREE_D
		from part import DEFORMABLE_BODY
		bendR = self.shape['bendR']
		outDiameter = self.shape['outDiameter']
		toolGap=self.shape['toolGap']
		self.model.ConstrainedSketch(name='__profile__', sheetSize=200.0)
		self.model.sketches['__profile__'].ArcByCenterEnds(center=(-bendR, 
			0.0), direction=CLOCKWISE, point1=(-bendR, -outDiameter/2 - toolGap), point2=(-bendR, outDiameter/2+toolGap))
		self.model.Part(dimensionality=THREE_D, name=self.partName, type=
			DEFORMABLE_BODY)
		self.model.parts[self.partName].BaseShellExtrude(depth=15 * outDiameter, sketch=
			self.model.sketches['__profile__'])
		del self.model.sketches['__profile__']
	def outerSurface(self):
		p = self.model.parts[self.partName]
		s = p.faces
		side1Faces = s.getSequenceFromMask(mask=('[#1 ]', ), )
		p.Surface(side1Faces=side1Faces, name='Surf-Outer')
	def setRP(self,RP):
		self.RP = RP
		p = self.model.parts[self.partName]
		p.ReferencePoint(point=self.RP)
		r = p.referencePoints
		refPoints=(r[2], )
		p.Set(referencePoints=refPoints, name='Set-RP')
		
class Tube(Part):
	def _init_(self):
		Part._init_(self)
		self.partName = 'Part-Tube'
	def geometry(self):
		from part import STANDALONE
		from part import CLOCKWISE
		from part import THREE_D
		from part import DEFORMABLE_BODY
		bendR = self.shape['bendR']
		outDiameter = self.shape['outDiameter']
		s1 = self.model.ConstrainedSketch(name='__profile__', 
			sheetSize=200.0)
		g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
		s1.setPrimaryObject(option=STANDALONE)
		s1.CircleByCenterPerimeter(center=(-bendR, 0.0), point1=(-bendR, outDiameter/2))
		p = self.model.Part(name=self.partName, dimensionality=THREE_D, 
			type=DEFORMABLE_BODY)
		p.BaseShellExtrude(sketch=s1, depth=30*outDiameter)
		s1.unsetPrimaryObject()
		del self.model.sketches['__profile__']
	
	def outerSurface(self):
		p = self.model.parts[self.partName]
		s = p.faces
		side1Faces = s.getSequenceFromMask(mask=('[#1 ]', ), )
		p.Surface(side1Faces=side1Faces, name='Surf-Outer')
	
	def innerSurface(self):
		p = self.model.parts[self.partName]
		s = p.faces
		side2Faces = s.getSequenceFromMask(mask=('[#1 ]', ), )
		p.Surface(side2Faces=side2Faces, name='Surf-Inner')
# Mdb()
# modelname = 'Model-1'
# model = mdb.models[modelname]
# shapes = {'bendR':220,'outDiameter':40,'toolGap':.1}

# insert = BendDie()
# insert._init_()
# insert.setModel(model)
# insert.setShape(shapes)
# insert.geometry()
# insert.outerSurface()
# RP = (-shapes['bendR'],0,3*shapes['outDiameter'])
# insert.setRP(RP)