# -*- coding: utf-8 -*- 
from PartRoot import *
from part import *
from assembly import *
from sketch import *
from section import *
from regionToolset import *
from displayGroupMdbToolset import *
from part import *
from material import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from xyPlot import *
from displayGroupOdbToolset import *
from connectorBehavior import *
from part import *
_metaclass_ = type
class Insert(Tool):
	def __init__(self,model):
		Tool.__init__(self,model)
		self.partName = 'Part-Insert'
		self.friction = .5
	
	def geometry(self):
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
	def __init__(self,model):
		Tool.__init__(self,model)
		self.partName = 'Part-Clamp'
		self.friction = .5
	def geometry(self):

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
	def __init__(self,model):
		Tool.__init__(self,model)
		self.partName = 'Part-BendDie'
		self.friction = .125
	def geometry(self):
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
	def __init__(self,model):
		Tool.__init__(self,model)
		self.partName = 'Part-Wiper'
		self.friction = .5
	
	def geometry(self):
		
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
	def __init__(self,model):
		Tool.__init__(self,model)
		self.partName = 'Part-Press'
		self.friction = .5
	def geometry(self):
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
		
class RecifyClamp(Tool):
	def __init__(self,model):
		Tool.__init__(self,model)
		self.partName = 'Part-RecifyClamp'
		self.friction = .5
		self.r2=0.
		self.r3=0.
		self.h=0.
	def geometry(self):
		bendR = self.shape['bendR']
		outDiameter = self.shape['outDiameter']
		toolGap=self.shape['toolGap']
		if bendR / outDiameter > 1.5 and bendR / outDiameter <= 2:
			self.r2=0.95*outDiameter
			self.r3=0.37*outDiameter
			self.h=0.56*outDiameter
		elif bendR /outDiameter > 2 and bendR / outDiameter <= 3.5:
			self.r2=outDiameter
			self.r3=0.4*outDiameter
			self.h=0.545*outDiameter
		elif bendR / outDiameter > 3.5:
			self.r2=outDiameter
			self.r3=0.5*outDiameter
			self.h=0.5*outDiameter
		s1 = self.model.ConstrainedSketch(name='__profile__', 
			sheetSize=200.0)
		g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
		s1.setPrimaryObject(option=STANDALONE)
		s1.CircleByCenterPerimeter(center=(-bendR, 0.0), point1=(-bendR, outDiameter/2+toolGap))
		s1.FixedConstraint(entity=g[2])
		s1.ArcByCenterEnds(center=(-bendR-self.h+self.r3, 0.0), point1=(-bendR-self.h, 0.0),\
			point2=(-bendR-self.h+self.r3, self.r3), direction=CLOCKWISE)
		s1.FixedConstraint(entity=g[3])
		s1.ArcByCenterEnds(center=(-bendR+outDiameter/5, -outDiameter/1.7), \
			point1=(-bendR-outDiameter/2+5, outDiameter/2-5),\
			point2=(-bendR+outDiameter/4, outDiameter/1.7), direction=CLOCKWISE)
		s1.TangentConstraint(entity1=g[3], entity2=g[4])
		s1.TangentConstraint(entity1=g[2], entity2=g[4])
		s1.trimExtendCurve(curve1=g[4], point1=(-bendR-outDiameter/6, outDiameter/2), 
			curve2=g[3], point2=(-bendR-self.h+5, outDiameter/3))
		s1.trimExtendCurve(curve1=g[3], point1=(-bendR-self.h+2, outDiameter/5), 
			curve2=g[5], point2=(-bendR-outDiameter/5, outDiameter/2+2))
		s1.Line(point1=(-bendR-self.h, 0.0), point2=(-bendR, 0.0))
		s1.HorizontalConstraint(entity=g[7], addUndoState=False)
		s1.Line(point1=(-bendR, 0.0), point2=(-bendR, outDiameter/2+5))
		s1.VerticalConstraint(entity=g[8], addUndoState=False)
		
		s1.autoTrimCurve(curve1=g[2], point1=(-bendR-self.h+3, outDiameter/5))
		s1.autoTrimCurve(curve1=g[10], point1=(-bendR, -outDiameter))
		s1.autoTrimCurve(curve1=g[5], point1=(-bendR+outDiameter/6, outDiameter/1.5))
		s1.autoTrimCurve(curve1=g[11], point1=(-bendR-outDiameter/6, outDiameter/2))
	
		s1.setAsConstruction(objectList=(g[7], g[8]))
		s1.copyMirror(mirrorLine=g[7], objectList=(g[6], g[12], g[9]))
		p = self.model.Part(name=self.partName, dimensionality=THREE_D, 
			type=DEFORMABLE_BODY)
		p = self.model.parts[self.partName]
		p.BaseShellExtrude(sketch=s1, depth=bendR-outDiameter/2)
		s1.unsetPrimaryObject() 
		p = self.model.parts[self.partName]
		del self.model.sketches['__profile__']
		
	def outerSurface(self):
		p = self.model.parts[self.partName]
		s = p.faces
		side2Faces = s.getSequenceFromMask(mask=('[#1f ]', ), )
		p.Surface(side2Faces=side2Faces, name='Surf-Outer')
	def setRP(self,RP):
		self.RP = RP
		p = self.model.parts[self.partName]
		p.ReferencePoint(point=self.RP)
		r = p.referencePoints
		refPoints=(r[2], )
		p.Set(referencePoints=refPoints, name='Set-RP')
	def setMaterial(self,sectName):
		p = self.model.parts[self.partName]
		f = p.faces
		faces = f.getSequenceFromMask(mask=('[#ff ]', ), )
		p.Set(faces=faces, name='Set-Body')
		region = p.sets['Set-Body']
		p.SectionAssignment(region=region, sectionName=sectName, offset=0.0, 
			offsetType=BOTTOM_SURFACE, offsetField='', 
			thicknessAssignment=FROM_SECTION)

class RecifyPress(Tool):
	def __init__(self,model):
		Tool.__init__(self,model)
		self.partName = 'Part-RecifyPress'
		self.friction = .5
		self.r2=0.
		self.r3=0.
		self.h=0.
	def geometry(self):
		bendR = self.shape['bendR']
		outDiameter = self.shape['outDiameter']
		toolGap=self.shape['toolGap']
		if bendR / outDiameter > 1.5 and bendR / outDiameter <= 2:
			self.r2=0.95*outDiameter
			self.r3=0.37*outDiameter
			self.h=0.56*outDiameter
		elif bendR /outDiameter > 2 and bendR / outDiameter <= 3.5:
			self.r2=outDiameter
			self.r3=0.4*outDiameter
			self.h=0.545*outDiameter
		elif bendR / outDiameter > 3.5:
			self.r2=outDiameter
			self.r3=0.5*outDiameter
			self.h=0.5*outDiameter
		s1 = self.model.ConstrainedSketch(name='__profile__', 
			sheetSize=200.0)
		g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
		s1.setPrimaryObject(option=STANDALONE)
		s1.CircleByCenterPerimeter(center=(-bendR, 0.0), point1=(-bendR, outDiameter/2+toolGap))
		s1.FixedConstraint(entity=g[2])
		s1.ArcByCenterEnds(center=(-bendR-self.h+self.r3, 0.0), point1=(-bendR-self.h, 0.0),\
			point2=(-bendR-self.h+self.r3, self.r3), direction=CLOCKWISE)
		s1.FixedConstraint(entity=g[3])
		s1.ArcByCenterEnds(center=(-bendR+outDiameter/5, -outDiameter/1.7), \
			point1=(-bendR-outDiameter/2+5, outDiameter/2-5),\
			point2=(-bendR+outDiameter/4, outDiameter/1.7), direction=CLOCKWISE)
		s1.TangentConstraint(entity1=g[3], entity2=g[4])
		s1.TangentConstraint(entity1=g[2], entity2=g[4])
		s1.trimExtendCurve(curve1=g[4], point1=(-bendR-outDiameter/6, outDiameter/2), 
			curve2=g[3], point2=(-bendR-self.h+5, outDiameter/3))
		s1.trimExtendCurve(curve1=g[3], point1=(-bendR-self.h+2, outDiameter/5), 
			curve2=g[5], point2=(-bendR-outDiameter/5, outDiameter/2+2))
		s1.Line(point1=(-bendR-self.h, 0.0), point2=(-bendR, 0.0))
		s1.HorizontalConstraint(entity=g[7], addUndoState=False)
		s1.Line(point1=(-bendR, 0.0), point2=(-bendR, outDiameter/2+5))
		s1.VerticalConstraint(entity=g[8], addUndoState=False)
		
		s1.autoTrimCurve(curve1=g[2], point1=(-bendR-self.h+3, outDiameter/5))
		s1.autoTrimCurve(curve1=g[10], point1=(-bendR, -outDiameter))
		s1.autoTrimCurve(curve1=g[5], point1=(-bendR+outDiameter/6, outDiameter/1.5))
		s1.autoTrimCurve(curve1=g[11], point1=(-bendR-outDiameter/6, outDiameter/2))
	
		s1.setAsConstruction(objectList=(g[7], g[8]))
		s1.copyMirror(mirrorLine=g[7], objectList=(g[6], g[12], g[9]))
		p = self.model.Part(name=self.partName, dimensionality=THREE_D, 
			type=DEFORMABLE_BODY)
		p = self.model.parts[self.partName]
		p.BaseShellExtrude(sketch=s1, depth=15 * outDiameter,)
		s1.unsetPrimaryObject()
		p = self.model.parts[self.partName]
		del self.model.sketches['__profile__']
	def outerSurface(self):
		p = self.model.parts[self.partName]
		s = p.faces
		side2Faces = s.getSequenceFromMask(mask=('[#1f ]', ), )
		p.Surface(side2Faces=side2Faces, name='Surf-Outer')
	def setRP(self,RP):
		self.RP = RP
		p = self.model.parts[self.partName]
		p.ReferencePoint(point=self.RP)
		r = p.referencePoints
		refPoints=(r[2], )
		p.Set(referencePoints=refPoints, name='Set-RP')
	def setMaterial(self,sectName):
		p = self.model.parts[self.partName]
		f = p.faces
		faces = f.getSequenceFromMask(mask=('[#ff ]', ), )
		p.Set(faces=faces, name='Set-Body')
		region = p.sets['Set-Body']
		p.SectionAssignment(region=region, sectionName=sectName, offset=0.0, 
			offsetType=BOTTOM_SURFACE, offsetField='', 
			thicknessAssignment=FROM_SECTION)
			
class Ball(Tool):
	def __init__(self,model):
		Tool.__init__(self,model)
		self.partName = 'Part-Ball'
		self.friction = .05
	def geometry(self):
		ballThick = self.shape['ballThick']
		outDiameter = self.shape['outDiameter']
		ballGap = self.shape['ballGap']
		thick = self.shape['thick']
		ballRadius = outDiameter/2 - ballGap - thick
		#画球
		s = self.model.ConstrainedSketch(name='__profile__', 
			sheetSize=200.0)
		g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
		s.setPrimaryObject(option=STANDALONE)
		s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
		s.FixedConstraint(entity=g[2])
		s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, ballRadius), point2=(0.0, -ballRadius), 
			direction=CLOCKWISE)
		s.Line(point1=(0.0, ballRadius), point2=(0.0, -ballRadius))
		s.VerticalConstraint(entity=g[4], addUndoState=False)
		p = self.model.Part(name=self.partName, dimensionality=THREE_D, 
			type=DEFORMABLE_BODY)
		p.BaseSolidRevolve(sketch=s, angle=360, flipRevolveDirection=OFF)
		s.unsetPrimaryObject()
		del self.model.sketches['__profile__']
		#切除 
		p = self.model.parts[self.partName]
		p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=100.0)
		e, d1 = p.edges, p.datums
		#dp = d1.findAt(0.0,100,0.0)
		t = p.MakeSketchTransform(sketchPlane=d1[2], sketchUpEdge=e[0], 
			sketchPlaneSide=SIDE1, sketchOrientation=TOP, origin=(0.0, 100.0, 0.0))
		s1 = self.model.ConstrainedSketch(name='__profile__', 
			sheetSize=318.98, gridSpacing=7.97, transform=t)
		g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
		s1.setPrimaryObject(option=SUPERIMPOSE)
		p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
		s1.rectangle(point1=(-100.0, ballThick/2), point2=(100.0, 100.0))
		s1.ConstructionLine(point1=(-100.0, 0.0), point2=(100.0, 0.0))
		s1.HorizontalConstraint(entity=g[6], addUndoState=False)
		s1.copyMirror(mirrorLine=g[6], objectList=(g[3], g[2], g[5], g[4]))
		e1, d2 = p.edges, p.datums
		p.CutExtrude(sketchPlane=d2[2], sketchUpEdge=e1[0], sketchPlaneSide=SIDE1, 
			sketchOrientation=TOP, sketch=s1, flipExtrudeDirection=OFF)
		s1.unsetPrimaryObject()
		del self.model.sketches['__profile__']
		c1 = p.cells
		p.RemoveCells(cellList = c1[0:1])
		
	def outerSurface(self):
		p = self.model.parts[self.partName]
		s = p.faces
		side1Faces = s.getSequenceFromMask(mask=('[#7 ]', ), )
		p.Surface(side1Faces=side1Faces, name='Surf-Outer')
		
	def setRP(self,RP):
		self.RP = RP
		p = self.model.parts[self.partName]
		p.ReferencePoint(point=self.RP)
		r = p.referencePoints
		refPoints=(r[5], )
		p.Set(referencePoints=refPoints, name='Set-RP')
	def setMaterial(self,sectName):
		p = self.model.parts[self.partName]
		f = p.faces
		faces = f.getSequenceFromMask(mask=('[#7 ]', ), )
		p.Set(faces=faces, name='Set-Body')
		region = p.sets['Set-Body']
		p.SectionAssignment(region=region, sectionName=sectName, offset=0.0, 
			offsetType=BOTTOM_SURFACE, offsetField='', 
			thicknessAssignment=FROM_SECTION)
	
	def mesh(self,size):
		p = self.model.parts[self.partName]
		p.seedPart(size=size, deviationFactor=0.1, minSizeFactor=0.1)
		p.generateMesh()
		
class Mandrel(Tool):
	def __init__(self,model):
		Tool.__init__(self,model)
		self.partName = 'Part-Mandrel'
		self.friction = .05
	def geometry(self):
		bendR = self.shape['bendR']
		ballThick = self.shape['ballThick']
		outDiameter = self.shape['outDiameter']
		ballGap = self.shape['ballGap']
		thick = self.shape['thick']
		ballRadius = outDiameter/2 - ballGap - thick
		s1 = self.model.ConstrainedSketch(name='__profile__', 
			sheetSize=200.0)
		g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
		s1.setPrimaryObject(option=STANDALONE)
		s1.CircleByCenterPerimeter(center=(-bendR, 0.0), point1=(-bendR, ballRadius))
		p = self.model.Part(name=self.partName, dimensionality=THREE_D, 
			type=DEFORMABLE_BODY)
		p.BaseShellExtrude(sketch=s1, depth=10*outDiameter)
		s1.unsetPrimaryObject()
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
	def setMaterial(self,sectName):
		p = self.model.parts[self.partName]
		f = p.faces
		faces = f.getSequenceFromMask(mask=('[#7 ]', ), )
		p.Set(faces=faces, name='Set-Body')
		region = p.sets['Set-Body']
		p.SectionAssignment(region=region, sectionName=sectName, offset=0.0, 
			offsetType=BOTTOM_SURFACE, offsetField='', 
			thicknessAssignment=FROM_SECTION)
	
	def mesh(self,size):
		p = self.model.parts[self.partName]
		p.seedPart(size=size, deviationFactor=0.1, minSizeFactor=0.1)
		p.generateMesh()
		
class Tube(Part):
	def __init__(self,model):
		Part.__init__(self,model)
		self.partName = 'Part-Tube'
	def geometry(self):
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
		
	def mesh(self,size):
		p = self.model.parts[self.partName]
		p.seedPart(size=size, deviationFactor=0.1, minSizeFactor=0.1)
		p.generateMesh()
		n = p.nodes
		nodeLen=len(n)
		heads=n[0:11]
		ends=n[nodeLen-11:-1]
		p.Set(nodes=heads, name='Set-Head')
		p.Set(nodes=ends,name='Set-End')
		
# Mdb()
# modelname = 'Model-1'
# model = mdb.models[modelname]
# shapes = {'bendR':200,'outDiameter':65,'toolGap':.1,'ballGap':1.0,'ballThick':20.,'thick':3.5}
# insert = Mandrel(model)
# insert.setShape(shapes)
# insert.geometry()
# insert.setRP((-shapes['bendR'],0.,0.))
# insert.outerSurface()

