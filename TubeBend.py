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
		self.friction = .3
	
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
		self.friction = .7
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
		self.friction = .3
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
		self.friction = .05
	
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
		self.friction = .3
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
			offsetType=TOP_SURFACE, offsetField='', 
			thicknessAssignment=FROM_SECTION)
	
	def mesh(self,size):
		p = self.model.parts[self.partName]
		f = p.faces
		pickedRegions = f.getSequenceFromMask(mask=('[#7 ]', ), )
		p.setMeshControls(regions=pickedRegions, elemShape=QUAD)
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
			offsetType=TOP_SURFACE, offsetField='', 
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
		p.BaseShellExtrude(sketch=s1, depth=20*outDiameter)
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
		

from Assembly import *
class BendAssembly(Assembly):
	def setupMaterials(self,materials):
		TDensity,TE,TPossion = materials['tool']
		self.model.Material(name='Material-Tools')
		self.model.materials['Material-Tools'].Density(table=((TDensity, ), ))
		self.model.materials['Material-Tools'].Elastic(table=((TE, TPossion), ))
		self.model.HomogeneousShellSection(name='Section-Tool', 
				preIntegrate=OFF, material='Material-Tools', thicknessType=UNIFORM, 
				thickness=self.shapes['thick'], thicknessField='', idealization=NO_IDEALIZATION, 
				poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
				useDensity=OFF, integrationRule=SIMPSON, numIntPts=5)
		PDensity,PE,PPossion,K,e0,n,r = materials['part']
		listPlastic= []
		for ep in range(0,20) :
			epx = ep * 0.025
			sigma = K * ((epx + e0) ** n)
			listPlastic.append((sigma,epx))
		sigma2 = K * ((2+e0)**n)
		listPlastic.append((sigma2,2+e0))
		tuplePlastic = tuple(listPlastic)
			
		r33 = ((r + 1)/2) ** .5
		r12 = (3 * (r + 1) * r /(4 * r * r + 2 * r)) ** .5
		self.model.Material(name='Material-Tube')
		self.model.materials['Material-Tube'].Density(table=((PDensity, ), ))
		self.model.materials['Material-Tube'].Elastic(table=((PE, PPossion), ))
		self.model.materials['Material-Tube'].Plastic(table=tuplePlastic)
		self.model.materials['Material-Tube'].plastic.Potential(table=(
				(1.0, 1.0, r33, r12, 1.0, 1.0), ))
		self.model.HomogeneousShellSection(name='Section-Tube', 
				preIntegrate=OFF, material='Material-Tube', thicknessType=UNIFORM, 
				thickness=self.shapes['thick'], thicknessField='', idealization=NO_IDEALIZATION, 
				poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
				useDensity=OFF, integrationRule=SIMPSON, numIntPts=5)
	
	def addInstance(self,meshSizes):
		#首先划分管材网格	
		tube = Tube(self.model)
		tube.makeIt(self.shapes,'Section-Tube',meshSizes['tube'])
		self.parts.append(tube)
		
		insert = Insert(self.model)
		RPInsert = (0,0,self.shapes['bendR']-self.shapes['outDiameter']/2)
		insert.makeIt(self.shapes,RPInsert,'Section-Tool',meshSizes['pressDie'])
		self.tools.append(insert)
		
		clamp = Clamp(self.model)
		RPClamp = (0.0, 0.0, self.shapes['bendR']-self.shapes['outDiameter']/2)
		clamp.makeIt(self.shapes,RPClamp,'Section-Tool',meshSizes['pressDie'])
		self.tools.append(clamp)
		
		die = BendDie(self.model)
		RPDie = (.0,.0,.0)
		die.makeIt(self.shapes,RPDie,'Section-Tool',meshSizes['pressDie'])
		self.tools.append(die)
		
		wiper = Wiper(self.model)
		RPWiper = (0,0,0)
		wiper.makeIt(self.shapes,RPWiper,'Section-Tool',meshSizes['pressDie'])
		self.tools.append(wiper)
		
		press = Press(self.model)
		RPPress = (-self.shapes['bendR'], 0.0, 7.5*self.shapes['outDiameter'])
		press.makeIt(self.shapes,RPPress,'Section-Tool',meshSizes['pressDie'])
		self.tools.append(press)
		
		ball = Ball(self.model)
		RPBall = (0.,0.,0.)
		ball.makeIt(self.shapes,RPBall,'Section-Tool',meshSizes['pressDie'])
		self.innertools.append(ball)
		
		mandrel = Mandrel(self.model)
		RPMandrel = (-self.shapes['bendR'], 0.0, 0.)
		mandrel.makeIt(self.shapes,RPMandrel,'Section-Tool',meshSizes['pressDie'])
		self.innertools.append(mandrel)
		
	def setPositions(self,positions,args):
		a = self.model.rootAssembly
		a.DatumCsysByDefault(CARTESIAN)
		indexPositions = 0
		for instance in self.tools:
			p = self.model.parts[instance.partName]
			a.Instance(name=instance.partName+'-1', part=p, dependent=ON)
			if instance.partName=='Part-Clamp' :
				a.translate(instanceList=(instance.partName+'-1', ), vector=positions['clamp'])
			elif instance.partName=='Part-Insert':
				a.translate(instanceList=(instance.partName+'-1', ), vector=positions['insert'])
			elif instance.partName=='Part-Press':
				a.translate(instanceList=(instance.partName+'-1', ), vector=positions['press'])
			elif instance.partName == 'Part-Wiper':
				a.rotate(instanceList=('Part-Wiper-1', ), axisPoint=(0.0, 0.0, 0.0), 
					axisDirection=(0.0, 1.0, 0.0), angle=positions['wiper'])
			
			indexPositions += 1
		for instance in self.innertools:
			p = self.model.parts[instance.partName]
			a.Instance(name=instance.partName+'-1', part=p, dependent=ON)
			if instance.partName == 'Part-Ball':
				ballNum = args['ballNum']
				ball2ball = args['ball2ball']
				
				a.translate(instanceList=(instance.partName+'-1', ), vector=positions['ball'])
				#????
				a1 = self.model.rootAssembly
				a1.DatumAxisByPrincipalAxis(principalAxis=ZAXIS)
				a1.LinearInstancePattern(instanceList=(instance.partName+'-1', ), direction1=(1.0, 0.0, 
					0.0), direction2=(0.0, 0.0, -1.0), number1=1, number2=ballNum, spacing1=56.0, 
					spacing2=ball2ball + self.shapes['ballThick'])
			else :
				a.translate(instanceList=(instance.partName+'-1', ), vector=positions['mandral'])

		for instance in self.parts:
			p = self.model.parts[instance.partName]
			a.Instance(name=instance.partName+'-1', part=p, dependent=ON)
			a.translate(instanceList=(instance.partName+'-1', ), vector=positions['tube'])
	
	def toolsRigid(self,args):
		Assembly.toolsRigid(self,args)
		a = self.model.rootAssembly
		if (args['ballNum']>1):
			for ii in range(2,args['ballNum']+1):
				region2 = a.instances['Part-Ball-1-lin-1-'+str(ii)].sets['Set-Body']
				region1 = a.instances['Part-Ball-1-lin-1-'+str(ii)].sets['Set-RP']
				self.model.RigidBody(name='RIGID-'+ 'Part-Ball-Lin-'+str(ii), refPointRegion=region1, 
					bodyRegion=region2)
	
				
	def interactions(self,inits,args):
		a = self.model.rootAssembly
		region1=a.instances['Part-BendDie-1'].surfaces['Surf-Outer']
		region2=a.instances['Part-Insert-1'].surfaces['Surf-Outer']
		self.model.Tie(name='Tie-1', master=region1, slave=region2, 
			positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
			thickness=ON,constraintEnforcement=SURFACE_TO_SURFACE)
			
		a = self.model.rootAssembly
		INTINDEX = 0
		for instance in self.tools:
			f = instance.friction
			self.model.ContactProperty('IntProp-'+instance.partName)
			self.model.interactionProperties['IntProp-'+instance.partName].TangentialBehavior(
				formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
				pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, 
				table=((f, ), ), shearStressLimit=None, 
				maximumElasticSlip=FRACTION, fraction=f, elasticSlipStiffness=None)
			region1=a.instances[instance.partName+'-1'].surfaces['Surf-Outer']
			region2=a.instances[self.parts[0].partName+'-1'].surfaces['Surf-Outer']
			self.model.SurfaceToSurfaceContactExp(name ='Int-'+str(INTINDEX), 
				createStepName='Step-1', master = region1, slave = region2, 
				mechanicalConstraint=PENALTY, sliding=FINITE, 
				interactionProperty='IntProp-'+instance.partName, initialClearance=OMIT, datumAxis=None, 
				clearanceRegion=None)
			INTINDEX = INTINDEX + 1
			
		for instance in self.innertools:
			f = instance.friction
			self.model.ContactProperty('IntProp-'+instance.partName)
			self.model.interactionProperties['IntProp-'+instance.partName].TangentialBehavior(
				formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
				pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, 
				table=((f, ), ), shearStressLimit=None, 
				maximumElasticSlip=FRACTION, fraction=f, elasticSlipStiffness=None)
			region1=a.instances[instance.partName+'-1'].surfaces['Surf-Outer']
			region2=a.instances[self.parts[0].partName+'-1'].surfaces['Surf-Inner']
			self.model.SurfaceToSurfaceContactExp(name ='Int-'+str(INTINDEX), 
				createStepName='Step-1', master = region1, slave = region2, 
				mechanicalConstraint=PENALTY, sliding=FINITE, 
				interactionProperty='IntProp-'+instance.partName, initialClearance=OMIT, datumAxis=None, 
				clearanceRegion=None)
			INTINDEX = INTINDEX + 1
		#芯球
		if (args['ballNum'] > 1):
			for ii in range(2,args['ballNum']+1):
				region1 = a.instances['Part-Ball-1-lin-1-'+str(ii)].surfaces['Surf-Outer']
				region2=a.instances[self.parts[0].partName+'-1'].surfaces['Surf-Inner']
				self.model.SurfaceToSurfaceContactExp(name ='Int-'+str(INTINDEX), 
					createStepName='Step-1', master = region1, slave = region2, 
					mechanicalConstraint=PENALTY, sliding=FINITE, 
					interactionProperty='IntProp-Part-Ball', initialClearance=OMIT, datumAxis=None, 
					clearanceRegion=None)
				INTINDEX = INTINDEX + 1
			
		region1=a.instances['Part-Mandrel-1'].surfaces['Surf-Outer']
		region2=a.instances['Part-Ball-1'].surfaces['Surf-Outer']
		self.model.SurfaceToSurfaceContactExp(name ='Int-'+str(INTINDEX), 
			createStepName='Step-1', master = region1, slave = region2, 
			mechanicalConstraint=PENALTY, sliding=FINITE, 
			interactionProperty='IntProp-Part-Ball', initialClearance=OMIT, datumAxis=None, 
			clearanceRegion=None)
		INTINDEX = INTINDEX + 1
		
		region1=a.instances['Part-Ball-1'].surfaces['Surf-Outer']
		region2=a.instances['Part-Ball-1-lin-1-2'].surfaces['Surf-Outer']
		self.model.SurfaceToSurfaceContactExp(name ='Int-'+str(INTINDEX), 
			createStepName='Step-1', master = region1, slave = region2, 
			mechanicalConstraint=PENALTY, sliding=FINITE, 
			interactionProperty='IntProp-Part-Ball', initialClearance=OMIT, datumAxis=None, 
			clearanceRegion=None)
		INTINDEX = INTINDEX + 1
		if (args['ballNum'] > 1):
			for ii in range(2,args['ballNum']):
				region1=a.instances['Part-Ball-1-lin-1-'+str(ii)].surfaces['Surf-Outer']
				region2=a.instances['Part-Ball-1-lin-1-'+str(ii+1)].surfaces['Surf-Outer']
				self.model.SurfaceToSurfaceContactExp(name ='Int-'+str(INTINDEX), 
					createStepName='Step-1', master = region1, slave = region2, 
					mechanicalConstraint=PENALTY, sliding=FINITE, 
					interactionProperty='IntProp-Part-Ball', initialClearance=OMIT, datumAxis=None, 
					clearanceRegion=None)
				INTINDEX = INTINDEX + 1
			
		self.model.ConnectorSection(name='ConnSect-1', 
			translationalType=LINK)
		a = self.model.rootAssembly
		r1 = a.instances['Part-Mandrel-1'].referencePoints
		r2 = a.instances['Part-Ball-1'].referencePoints
		wire = a.WirePolyLine(points=((r1[2], r2[5]), ), mergeType=IMPRINT, 
			meshable=False)
		oldName = wire.name
		a.features.changeKey(fromName=oldName, toName='Wire-1')
		e1 = a.edges
		edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
		a.Set(edges=edges1, name='Wire-1-Set-1')
		region = self.model.rootAssembly.sets['Wire-1-Set-1']
		csa = a.SectionAssignment(sectionName='ConnSect-1', region=region)
		r11 = a.instances['Part-Ball-1'].referencePoints
		r12 = a.instances['Part-Ball-1-lin-1-2'].referencePoints
		wire = a.WirePolyLine(points=((r11[5], r12[5]), ), mergeType=IMPRINT, 
			meshable=False)
		oldName = wire.name
		self.model.rootAssembly.features.changeKey(fromName=oldName, 
			toName='Wire-2')
		e1 = a.edges
		edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
		a.Set(edges=edges1, name='Wire-2-Set-1')
		region = self.model.rootAssembly.sets['Wire-2-Set-1']
		csa = a.SectionAssignment(sectionName='ConnSect-1', region=region)
		if (args['ballNum'] > 1):
			for ii in range(2,args['ballNum']):
				r1 = a.instances['Part-Ball-1-lin-1-'+str(ii)].referencePoints
				r2 = a.instances['Part-Ball-1-lin-1-'+str(ii+1)].referencePoints
				wire = a.WirePolyLine(points=((r1[5], r2[5]), ), mergeType=IMPRINT, 
					meshable=False)
				oldName = wire.name
				a.features.changeKey(fromName=oldName, 
					toName='Wire-'+str(ii+1))
				e1 = a.edges
				edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
				a.Set(edges=edges1, name='Wire-'+str(ii+1)+'-Set-1')
				region = a.sets['Wire-'+str(ii+1)+'-Set-1']
				csa = a.SectionAssignment(sectionName='ConnSect-1', region=region)
		
		
		
	def setBC(self,BCs,args):
		angle = BCs['angle']
		close = BCs['close']
		assist = args['assist'] * (self.shapes['bendR']+self.shapes['outDiameter']/2)*angle
		self.model.TabularAmplitude(name='Amp-1', timeSpan=STEP, 
		 data=((0.0, 0.0), (0.05, 0.05),(0.35,0.6),(.4,.9), (0.45,.95), (.5, 
			1.0)))
		self.model.TabularAmplitude(name='Amp-3', timeSpan=STEP,  
			data=((0.0, 0.0), (0.005, 0.05),(0.035,0.6),(.04,.9), (0.045,1.), (.05, \
			1.0)))
		a = self.model.rootAssembly
		region = a.instances['Part-BendDie-1'].sets['Set-RP']
		self.model.DisplacementBC(name='BC-Bend', createStepName='Step-1', 
			region=region, u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0, 
			amplitude='Amp-1', fixed=OFF, distributionType=UNIFORM, fieldName='', 
			localCsys=None)
		self.model.boundaryConditions['BC-Bend'].setValuesInStep(
			stepName='Step-2', ur2=-angle)
		region = a.instances['Part-Press-1'].sets['Set-RP']
		self.model.DisplacementBC(name='BC-Press', createStepName='Step-1', 
			region=region, u1=close, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0, 
			amplitude='Amp-3', fixed=OFF, distributionType=UNIFORM, fieldName='', 
			localCsys=None)
		self.model.boundaryConditions['BC-Press'].setValuesInStep(
			stepName='Step-2',amplitude='Amp-1',u1=0.0, u3=-assist)
		region = a.instances['Part-Clamp-1'].sets['Set-RP']
		self.model.DisplacementBC(name='BC-Clamp', createStepName='Step-1', 
			region=region, u1=close, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0, 
			amplitude='Amp-3', fixed=OFF, distributionType=UNIFORM, fieldName='', 
			localCsys=None)
		self.model.boundaryConditions['BC-Clamp'].setValuesInStep(
			stepName='Step-2',amplitude='Amp-1',u1=0.0, ur2=-angle)
		region = a.instances['Part-Wiper-1'].sets['Set-RP']
		self.model.DisplacementBC(name='BC-Wiper', createStepName='Step-1', 
			region=region, u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0, 
			amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
			localCsys=None)
		region = a.instances['Part-Mandrel-1'].sets['Set-RP']
		self.model.DisplacementBC(name='BC-Mandral', 
			createStepName='Step-1', region=region, u1=0.0, u2=0.0, u3=0.0, 
			ur1=0.0, ur2=0.0, ur3=0.0, amplitude=UNSET, fixed=OFF, 
			distributionType=UNIFORM, fieldName='', localCsys=None)
	def setLoads(self,loads):
		self.model.TabularAmplitude(name='Amp-2', timeSpan=STEP,
			data=((0.0, 0.0), (0.025, 0.3), (0.05, 1.0), (.5, 1.0)))
		a = self.model.rootAssembly
		region = a.instances['Part-Press-1'].sets['Set-RP']
		self.model.ConcentratedForce(name='Load-1', createStepName='Step-2', 
			region=region, cf1=loads['Press'], amplitude='Amp-2', 
			distributionType=UNIFORM, field='', localCsys=None)
		
	def stepSetup(self, steps,args):
		regionDef0=self.model.rootAssembly.allInstances[self.parts[0].partName+'-1'].sets['Set-Body']
		self.model.ExplicitDynamicsStep(name='Step-1', previous='Initial', 
			timePeriod=0.05,\
			massScaling=((SEMI_AUTOMATIC, regionDef0, AT_BEGINNING, 10., 0.0, None, \
			0, 0, 0.0, 0.0, 0, None), ))
		self.model.fieldOutputRequests['F-Output-1'].setValues(variables=(
			'S', 'SVAVG', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 'V', 'A', 
			'RF', 'CSTRESS', 'EVF', 'STH', 'COORD'))
		for ii in range(2,steps+1):
			self.model.ExplicitDynamicsStep(name='Step-'+str(ii), previous='Step-'+str(ii-1)\
				,timePeriod=.5)
				
				
from Springback import *
class TubeSP(Springback):
	def setModel(self):
		a = self.model.rootAssembly
		parts = a.features
		a.deleteFeatures(parts)
		interactions = a.interactions
		self.model.interactions.delete(interactions)

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


from FEA import * 
from TubeSP import TubeSP
from ProfileFit import *
import random
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
		self.springback = TubeSP(self.modelname)
		self.springback.makeIt()
	def doJobs(self):
		pass
	def getResults(self):
		pass
		
		


paramFile = open('result.txt','a+')
paramFile.write('R D Thick angle E K e0 n m d e g j assist minTh springback Ell Wrinkle\n')
paramFile.close()
for jj in range(7,15):
		modelname='Model-'+str(jj)+'-'+str(1)
		t = TBFEA(modelname)
		
		Load={'Press':30000}
		bendR = float(random.randint(140,200))
		outDiameter = float(random.randint(70,100))
		angle = float(random.randint(5,90))
		thick = random.uniform(1.0,3.)
		ballGap = random.uniform(.3,.8)
		
		ballNum = random.randint(1,5)
		ballThick = random.uniform(.24,.3) * outDiameter
		mandralOut = random.uniform(5.,7.)
		assist = random.uniform(.9,1.2)
		
		if outDiameter < 80:
			ball2ball = random.uniform(.7,1.1) * ballThick
		else :
			ball2ball = random.uniform(1.,1.3) * ballThick
		E = float(random.randint(170,220)) * 1000
		K = float(random.randint(750,850))
		e0 = random.uniform(.02,0.05)
		n = random.uniform(.2,.27)
		tools = [7.85e-9,210000.0,.3]
		parts = [7.85e-9,E,.3,K,e0,n,1.0]		
		shapes = {'bendR':bendR,'outDiameter':outDiameter,'thick':thick,'toolGap':0.1,'ballGap':ballGap,'ballThick':ballThick}
		meshSize = {'pressDie':6,'tube':5}
		BCs={'angle':angle/180.0*pi,'close':shapes['outDiameter']/2}
		arg={'assist':assist,'mandralOut':mandralOut,'ball2ball':ball2ball,'ballNum':ballNum,'bendR':shapes['bendR'],\
			'outDiameter':shapes['outDiameter'],'thickness':shapes['thick'],'meshSize':meshSize['tube']}
		positions = {'clamp':(-BCs['close'],0,-shapes['bendR']+shapes['outDiameter']/2),'insert':(.0,0.,-shapes['bendR']+shapes['outDiameter']/2),\
			'press':(-BCs['close'],0.,0.),\
			'tube':(0,0,-shapes['bendR']-shapes['outDiameter']/2),'ball':(-shapes['bendR'],0,-arg['ball2ball']-arg['mandralOut']-shapes['ballThick']/2),\
			'mandral':(0,0,-arg['mandralOut']),'wiper':0.5}
		material={'tool':tools,'part':parts}
		
		
		t.setParameter(shapes,material,positions,0,\
			2,BCs,Load,meshSize,arg)
		t.setModels()
		modelsp=modelname+'-SP'
		init=solveArray(modelname,arg)
		springback=solveArray(modelsp,arg)
		minTh,wrinkle = getThickandWrinkle(modelsp,arg)
		ell = getSection(modelsp,arg)
		#initial paramters
	
		paramFile = open('result.txt','a+')
		
		paramFile.write('%10.3E %10.3E %10.3E %10.3E\
			%10.3E %10.3E %10.3E %10.3E\
			%10.3E %10.3E %10.3E %10.3E %10.3E %10.3E\
			%10.3E %10.3E %10.3E %s\n'\
			%(shapes['bendR'],shapes['outDiameter'],shapes['thick'],init,\
			parts[1],parts[3],parts[4],parts[5],\
			ballNum,ballThick,mandralOut,ballGap,ball2ball,assist,\
			minTh,springback,ell,wrinkle))
		paramFile.close()