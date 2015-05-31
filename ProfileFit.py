# -*- coding: utf-8 -*- 
from scipy.linalg import lstsq
import numpy as np
import math
from TBPost import *
# def err(p,args):
	# errs=[]
	# angle,r=p
	# tbPost=TBPost(args['modelname'])
	# tbPost.setPart('PART-TUBE-1')
	# coords=tbPost.output(args)
	# k,v=coords.popitem()
	# x0,y0,z0=v
	# m=np.cos(angle)
	# p=np.sin(angle)
	# for coord in coords.iteritems():
		# key,value = coord
		# print key
		# x,y,z=value
		# err=r**2-(p*(y-y0))**2-(m*(z-z0)-p*(x-x0))**2-(-m*(y-y0))**2
		# errs.append(err)
	# return np.array(errs)
	
def solveArray(modelname,args):
	tbPost=TBPost(modelname)
	tbPost.setPart('PART-TUBE-1')
	endCoords,headCoords=tbPost.output(args)
	tbPost.close()
	ae=[]
	be=[]
	ah=[]
	bh=[]
	for coord in endCoords.iteritems():
		key,value=coord
		v=[value[0],value[1],1]
		ae.append(v)
		be.append(value[2])
		
	npa=np.array(ae)
	npb=np.array(be)
	xe,ye,ze,we=lstsq(npa,npb)

	for coord in headCoords.iteritems():
		key,value=coord
		v=[value[0],value[1],1]
		ah.append(v)
		bh.append(value[2])
	npa=np.array(ah)
	npb=np.array(bh)
	xh,yh,zh,wh=lstsq(npa,npb)

	xee=np.array([xe[0],xe[1],-1])
	xhh=np.array([xh[0],xh[1],-1])
	Lxe=np.sqrt(xee.dot(xee))
	Lxh=np.sqrt(xhh.dot(xhh))
	cos_angle=xee.dot(xhh)/(Lxe*Lxh)
	angle=np.arccos(cos_angle)
	print angle / math.pi * 180
	return angle / math.pi * 180

def getThickandWrinkle(modelname,args):
	tbPost=TBPost(modelname)
	tbPost.setPart('PART-TUBE-1')
	endCoords,headCoords,thMin,wrinkle=tbPost.output(args)
	return 	thMin,wrinkle

# modelname= 'Model-40-1-SP'
# args={'modelname':modelname,'angle':1.0,}
# x=solveArray(modelname,args)


# r = 20.0
# angle=1.0
# np1 = np.array((angle,r))
# plsq2 = leastsq(err,np1,args = args,ftol=1.5e-8,xtol=1e-8,epsfcn=0.0000001,factor=10)
# print plsq2