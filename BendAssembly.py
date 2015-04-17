# -*- coding: utf-8 -*- 
from Assembly import *
class BendAssembly(Assembly):
	def setupMaterials(self,materials):
		from section import UNIFORM
		from section import NO_IDEALIZATION
		from section import SIMPSON
		TDensity,TE,TPossion = materials['tool']
		self.model.Material(name='Material-Tools')
		self.model.materials['Material-Tools'].Density(table=((TDensity, ), ))
		self.model.materials['Material-Tools'].Elastic(table=((TE, TPossion), ))
		self.model.HomogeneousShellSection(name='Section-Tool', 
				preIntegrate=OFF, material='Material-Tools', thicknessType=UNIFORM, 
				thickness=self.shapes['thick']*3, thicknessField='', idealization=NO_IDEALIZATION, 
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
		from BendParts import Insert
		from BendParts import Clamp
		from BendParts import Tube
		from BendParts import BendDie
		from BendParts import Wiper
		from BendParts import Press
		
		insert = Insert()
		RPInsert = (-self.shapes['bendR'], 0.0, (self.shapes['bendR']-self.shapes['outDiameter']/2)/2)
		insert.makeIt(self.model,self.shapes,RPInsert,'Section-Tool',meshSizes['pressDie'])
		self.tools.append(insert)
		
		clamp = Clamp()
		RPClamp = (-self.shapes['bendR'], 0.0, (self.shapes['bendR']-self.shapes['outDiameter']/2)/2)
		clamp.makeIt(self.model,self.shapes,RPClamp,'Section-Tool',meshSizes['pressDie'])
		self.tools.append(clamp)
		
		die = BendDie()
		RPDie = (.0,.0,.0)
		die.makeIt(self.model,self.shapes,RPDie,'Section-Tool',meshSizes['pressDie'])
		self.tools.append(die)
		
		wiper = Wiper()
		RPWiper = (0,0,0)
		wiper.makeIt(self.model,self.shapes,RPWiper,'Section-Tool',meshSizes['pressDie'])
		self.tools.append(wiper)
		
		press = Press()
		RPPress = (-self.shapes['bendR'], 0.0, 7.5*self.shapes['outDiameter'])
		press.makeIt(self.model,self.shapes,RPPress,'Section-Tool',meshSizes['pressDie'])
		self.tools.append(press)
		
		tube = Tube()
		tube.makeIt(self.model,self.shapes,'Section-Tube',meshSizes['tube'])
		self.parts.append(tube)
		
	def setPositions(self,positions,args):
		from assembly import CARTESIAN
		a = self.model.rootAssembly
		a.DatumCsysByDefault(CARTESIAN)
		indexPositions = 0
		for instance in self.tools:
			p = self.model.parts[instance.partName]
			a.Instance(name=instance.partName+'-1', part=p, dependent=ON)
			if instance.partName=='Part-Clamp' or instance.partName=='Part-Insert' :
				a.translate(instanceList=(instance.partName+'-1', ), vector=positions['insert'])
			else:
				pass
			indexPositions += 1
		# for instance in self.innertools:
			# p = self.model.parts[instance.partName]
			# a.Instance(name=instance.partName+'-1', part=p, dependent=ON)
			# if instance.partName == 'Part-Ball':
				# a.translate(instanceList=(instance.partName+'-1', ), vector=positions['ball'])
			# else:
				# a.translate(instanceList=(instance.partName+'-1', ), vector=positions['mandral'])
		for instance in self.parts:
			p = self.model.parts[instance.partName]
			a.Instance(name=instance.partName+'-1', part=p, dependent=ON)
			a.translate(instanceList=(instance.partName+'-1', ), vector=positions['tube'])
		# a.LinearInstancePattern(instanceList=('Part-Ball-1', ), direction1=(0.0, 0.0, 
			# -1.0), direction2=(0.0, 1.0, 0.0), number1=args['num'], number2=1, spacing1=args['spacing'], 
			# spacing2=16.0)
		# for ii in range(2,args['num']+1):
			# self.model.rootAssembly.features.changeKey(
				# fromName='Part-Ball-1-lin-'+str(ii)+'-1', toName='Part-Ball-'+str(ii))
				
	def interactions(self,inits,args):
		from material import *
		from interaction import *
		from connectorBehavior import *
		a = self.model.rootAssembly
		region1=a.instances['Part-BendDie-1'].surfaces['Surf-Outer']
		region2=a.instances['Part-Insert-1'].surfaces['Surf-Outer']
		self.model.Tie(name='Tie-1', master=region1, slave=region2, 
			positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
			thickness=ON,constraintEnforcement=SURFACE_TO_SURFACE)

		region1=a.instances['Part-BendDie-1'].surfaces['Surf-Outer']
		region2=a.instances['Part-Clamp-1'].surfaces['Surf-Outer']
		self.model.Tie(name='Tie-2', master=region1, slave=region2, 
			positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
			thickness=ON,constraintEnforcement=SURFACE_TO_SURFACE)
		frictionBig = inits['0.5']
		frictionSmall = inits['0.125']
		self.model.ContactProperty('IntProp-BIG')
		self.model.interactionProperties['IntProp-BIG'].TangentialBehavior(
			formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
			pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, 
			table=((frictionBig, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
			fraction=0.005, elasticSlipStiffness=None)
		self.model.ContactProperty('IntProp-SMALL')
		self.model.interactionProperties['IntProp-SMALL'].TangentialBehavior(
			formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
			pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, 
			table=((frictionSmall, ), ), shearStressLimit=None, 
			maximumElasticSlip=FRACTION, fraction=0.005, elasticSlipStiffness=None)
		a = self.model.rootAssembly
		INTINDEX = 0
		for instance in self.tools:
			if instance.friction == .5:
				region1=a.instances[instance.partName+'-1'].surfaces['Surf-Outer']
				region2=a.instances[self.parts[0].partName+'-1'].surfaces['Surf-Outer']
				self.model.SurfaceToSurfaceContactExp(name ='Int-'+str(INTINDEX), 
					createStepName='Step-1', master = region1, slave = region2, 
					mechanicalConstraint=PENALTY, sliding=FINITE, 
					interactionProperty='IntProp-BIG', initialClearance=OMIT, datumAxis=None, 
					clearanceRegion=None)
			else :
				region1=a.instances[instance.partName+'-1'].surfaces['Surf-Outer']
				region2=a.instances[self.parts[0].partName+'-1'].surfaces['Surf-Outer']
				self.model.SurfaceToSurfaceContactExp(name ='Int-'+str(INTINDEX), 
					createStepName='Step-1', master = region1, slave = region2, 
					mechanicalConstraint=PENALTY, sliding=FINITE, 
					interactionProperty='IntProp-SMALL', initialClearance=OMIT, datumAxis=None, 
					clearanceRegion=None)
			INTINDEX = INTINDEX + 1
		# for instance in self.innertools:
			# region1=a.instances[instance.partName+'-1'].surfaces['Surf-Outer']
			# region2=a.instances[self.parts[0].partName+'-1'].surfaces['Surf-Inner']
			# self.model.SurfaceToSurfaceContactExp(name ='Int-'+str(INTINDEX), 
				# createStepName='Initial', master = region1, slave = region2, 
				# mechanicalConstraint=PENALTY, sliding=FINITE, 
					# interactionProperty='IntProp-SMALL', initialClearance=OMIT, datumAxis=None, 
					# clearanceRegion=None)
			# INTINDEX = INTINDEX + 1
		
		# self.model.ConnectorSection(name='ConnSect-1', translationalType=LINK)
		# a = self.model.rootAssembly
		# r11 = a.instances['Part-Mandral-1'].referencePoints
		# r12 = a.instances['Part-Ball-1'].referencePoints
		# wire = a.WirePolyLine(points=((r11[3], r12[5]), ), mergeType=IMPRINT, 
			# meshable=False)
		# a.features.changeKey(fromName=wire.name, 
			# toName='Wire-1')
		# e1 = a.edges
		# edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
		# a.Set(edges=edges1, name='Wire-1-Set-1')
		# region = a.sets['Wire-1-Set-1']
		# csa = a.SectionAssignment(sectionName='ConnSect-1', region=region)
		# region1=a.instances['Part-Mandral-1'].surfaces['Surf-Outer']
		# region2=a.instances['Part-Ball-1'].surfaces['Surf-Outer']
		# self.model.SurfaceToSurfaceContactExp(name ='Int-'+str(INTINDEX), 
			# createStepName='Initial', master = region1, slave = region2, 
			# mechanicalConstraint=PENALTY, sliding=FINITE, 
			# interactionProperty='IntProp-SMALL', initialClearance=OMIT, datumAxis=None, 
			# clearanceRegion=None)
		# INTINDEX = INTINDEX + 1
		# for ii in range(2,args['num']+1):
			# r11 = a.instances['Part-Ball-'+str(ii-1)].referencePoints
			# r12 = a.instances['Part-Ball-'+str(ii)].referencePoints
			# wire = a.WirePolyLine(points=((r11[5],r12[5]),),mergeType=IMPRINT,
				# meshable=False)
			# a.features.changeKey(fromName=wire.name,toName='Wire-'+str(ii))
			# e1 = a.edges
			# edges1=e1.getSequenceFromMask(mask=('[#1]',),)
			# a.Set(edges=edges1,name='Wire-'+str(ii)+'-Set-1')
			# region=a.sets['Wire-'+str(ii)+'-Set-1']
			# csa=a.SectionAssignment(sectionName='ConnSect-1',region=region)
			# region1=a.instances['Part-Ball-'+str(ii-1)].surfaces['Surf-Outer']
			# region2=a.instances['Part-Ball-'+str(ii)].surfaces['Surf-Outer']
			# region3=a.instances['Part-Tube-1'].surfaces['Surf-Inner']
			# self.model.SurfaceToSurfaceContactExp(name ='Int-'+str(INTINDEX), 
				# createStepName='Initial', master = region1, slave = region2, 
				# mechanicalConstraint=PENALTY, sliding=FINITE, 
				# interactionProperty='IntProp-SMALL', initialClearance=OMIT, datumAxis=None, 
				# clearanceRegion=None)
			# INTINDEX = INTINDEX + 1
			# self.model.SurfaceToSurfaceContactExp(name ='Int-'+str(INTINDEX), 
				# createStepName='Initial', master = region2, slave = region3, 
				# mechanicalConstraint=PENALTY, sliding=FINITE, 
				# interactionProperty='IntProp-SMALL', initialClearance=OMIT, datumAxis=None, 
				# clearanceRegion=None)
			# INTINDEX = INTINDEX + 1
		
tools = [7.85e-7,210000.0,.3]
parts = [7.85e-9,210000.0,.3,750.0,.06,.24,1.0]		
shapes = {'bendR':220.0,'outDiameter':40.0,'thick':1.0,'mandralGap':.8,'toolGap':0.0,'ballThick':10.0,}
positions = {'insert':(0,0,-200),'tube':(0,0,-240),'ball':(-shapes['bendR'],0,-12),'mandral':(0,0,0)}
material={'tool':tools,'part':parts}
meshSize = {'pressDie':3.0/0.6,'tube':1.0/0.6}
inits={'0.5':.5,'0.125':.125}
args={}
tubeBend = BendAssembly()
tubeBend._init_()
tubeBend.setupShapes(shapes)
tubeBend.setupMaterials(material)
tubeBend.addInstance(meshSize)
tubeBend.stepSetup(1,args)
tubeBend.setPositions(positions,args)
tubeBend.toolsRigid(args)
tubeBend.interactions(inits,args)
