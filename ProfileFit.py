# -*- coding: utf-8 -*- 
from scipy.linalg import lstsq
import numpy as np
import math
from TBPost import *
	
def solveArray(modelname,args):
	tbPost=TBPost(modelname)
	tbPost.setPart('PART-TUBE-1')
	endCoords,headCoords,a,b=tbPost.output(args)
	
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
	tbPost.close()
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
	
def getSection(modelname,args):
	tbPost=TBPost(modelname)
	tbPost.setPart('PART-TUBE-1')
	section=tbPost.section(args)
	
	bendR = args['bendR']
	R = args['outDiameter']/2
	meshSize = args['meshSize']
	xs = []
	ys = []
	for ii in section:
		x = ii.data[0]
		y = ii.data[1]
		xx = [x**2,y**2,x*y,x,1]
		yy = [-y]
		xs.append(xx)
		ys.append(yy)
	axs = array(xs)
	ays = array(ys)
	xe,ye,ze,we=lstsq(axs,ays)
	A,B,C,D,F = xe
	right = D ** 2 / 4 / A  + 1 / 4 / B - F
	long = (right / B) **.5
	short = (right / A) **.5
	ell = (R - short)/R
	return 	ell
	
# modelname= 'Model-40-1-SP'
# args={'modelname':modelname,'angle':1.0,}
# x=solveArray(modelname,args)


# r = 20.0
# angle=1.0
# np1 = np.array((angle,r))
# plsq2 = leastsq(err,np1,args = args,ftol=1.5e-8,xtol=1e-8,epsfcn=0.0000001,factor=10)
# print plsq2