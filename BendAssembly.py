# -*- coding: utf-8 -*- 
from Assembly import *
from BendParts import *
from math import *
from step import *
from load import *
from step import *
from load import *
from material import *
from interaction import *
from connectorBehavior import *
from section import *
from assembly import *
class BendAssembly(Assembly):
	innerTools = []
	def setupMaterials(self,materials):
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
		self.innerTools.append(ball)
		
		mandrel = Mandrel(self.model)
		RPMandrel = (-self.shapes['bendR'], 0.0, 0.)
		mandrel.makeIt(self.shapes,RPMandrel,'Section-Tool',meshSizes['pressDie'])
		self.innerTools.append(mandrel)
		
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
		for instance in self.innerTools:
			p = self.model.parts[instance.partName]
			a.Instance(name=instance.partName+'-1', part=p, dependent=ON)
			if instance.partName == 'Part-Ball':
				a.translate(instanceList=(instance.partName+'-1', ), vector=positions['ball'])
				#添加阵列
			elif :
				a.translate(instanceList=(instance.partName+'-1', ), vector=positions['mandrel'])

		for instance in self.parts:
			p = self.model.parts[instance.partName]
			a.Instance(name=instance.partName+'-1', part=p, dependent=ON)
			a.translate(instanceList=(instance.partName+'-1', ), vector=positions['tube'])
				
	def interactions(self,inits,args):
		
		a = self.model.rootAssembly
		region1=a.instances['Part-BendDie-1'].surfaces['Surf-Outer']
		region2=a.instances['Part-Insert-1'].surfaces['Surf-Outer']
		self.model.Tie(name='Tie-1', master=region1, slave=region2, 
			positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
			thickness=ON,constraintEnforcement=SURFACE_TO_SURFACE)

		# region1=a.instances['Part-BendDie-1'].surfaces['Surf-Outer']
		# region2=a.instances['Part-RecifyClamp-1'].surfaces['Surf-Outer']
		# self.model.Tie(name='Tie-2', master=region1, slave=region2, 
			# positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
			# thickness=ON,constraintEnforcement=SURFACE_TO_SURFACE)
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
		
	def setBC(self,BCs,args):
		
		angle = BCs['angle']
		close = BCs['close']
		assist = args['assist'] * (self.shapes['bendR']+self.shapes['outDiameter']/2)*angle
		self.model.TabularAmplitude(name='Amp-1', timeSpan=STEP, 
			smooth=0.05, data=((0.0, 0.0), (0.1, 0.05),(0.7,0.6),(.8,.9), (0.9,.95), (1.0, 
			1.0)))
		self.model.TabularAmplitude(name='Amp-3', timeSpan=STEP, smooth=0.1, 
			data=((0.0, 0.0), (0.01, 0.05),(0.07,0.6),(.08,.9), (0.09,.95), (.1, \
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
	def setLoads(self,loads):
		self.model.TabularAmplitude(name='Amp-2', timeSpan=STEP, smooth=0.1, 
			data=((0.0, 0.0), (0.05, 0.3), (0.1, 1.0), (1.0, 1.0)))
		a = self.model.rootAssembly
		region = a.instances['Part-Press-1'].sets['Set-RP']
		self.model.ConcentratedForce(name='Load-1', createStepName='Step-2', 
			region=region, cf1=loads['Press'], amplitude='Amp-2', 
			distributionType=UNIFORM, field='', localCsys=None)
		
	def stepSetup(self, steps,args):
		self.model.ExplicitDynamicsStep(name='Step-1', previous='Initial', 
			timePeriod=0.1,\
			massScaling=((SEMI_AUTOMATIC, MODEL, AT_BEGINNING, 1000, 0.0, None, 
			0, 0, 0.0, 0.0, 0, None), ))
		self.model.fieldOutputRequests['F-Output-1'].setValues(variables=(
			'S', 'SVAVG', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 'V', 'A', 
			'RF', 'CSTRESS', 'EVF', 'STH', 'COORD'))
		for ii in range(2,steps+1):
			self.model.ExplicitDynamicsStep(name='Step-'+str(ii), previous='Step-'+str(ii-1))

