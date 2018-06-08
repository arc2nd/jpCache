#cmds.deformer( type='jpShiftNode' )

import sys
 
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
 
kPluginNodeTypeName = "jpCacheNode"

jpCacheNodeId = OpenMaya.MTypeId(0x5202) #range: 0-0x7ffff

# Node definition
class jpCacheNode(OpenMayaMPx.MPxDeformerNode):
	# class variables
	time = OpenMaya.MObject()
	shiftX = OpenMaya.MObject()
	shiftY = OpenMaya.MObject()
	shiftZ = OpenMaya.MObject()
	# constructor
	def __init__(self):
		OpenMayaMPx.MPxDeformerNode.__init__(self)
	# deform
	def deform(self,dataBlock,geomIter,matrix,multiIndex):  
		#
		# get the time
		timeHandle = dataBlock.inputValue( self.time )
		timeValue = timeHandle.asFloat()
		#
		# get the shifts from the datablock
		shiftXHandle = dataBlock.inputValue( self.shiftX )
		shiftXValue = shiftXHandle.asDouble()
		shiftYHandle = dataBlock.inputValue( self.shiftY )
		shiftYValue = shiftYHandle.asDouble()
		shiftZHandle = dataBlock.inputValue( self.shiftZ )
		shiftZValue = shiftZHandle.asDouble()
		#
		# get the envelope
		envelope = OpenMayaMPx.cvar.MPxDeformerNode_envelope
		envelopeHandle = dataBlock.inputValue( envelope )
		envelopeValue = envelopeHandle.asFloat()
		#
		# iterate over the object and change the points
		while geomIter.isDone() == False:
			point = geomIter.position()

			point.x = point.x + shiftXValue*envelopeValue
			point.y = point.y + shiftYValue*envelopeValue
			point.z = point.z + shiftZValue*envelopeValue

			geomIter.setPosition( point )
			geomIter.next()
			
# creator
def nodeCreator():
	return OpenMayaMPx.asMPxPtr( jpCacheNode() )

# initializer
def nodeInitializer():
	# time
	nAttr = OpenMaya.MFnNumericAttribute()
	jpCacheNode.time = nAttr.create( "time", "t", OpenMaya.MFnNumericData.kDouble, 1.0 )
	nAttr.setKeyable(True)
	# shift
	nAttr = OpenMaya.MFnNumericAttribute()
	jpCacheNode.shiftX = nAttr.create( "shiftX", "shX", OpenMaya.MFnNumericData.kDouble, 0.0 )
	nAttr.setKeyable(True)

	nAttr = OpenMaya.MFnNumericAttribute()
	jpCacheNode.shiftY = nAttr.create( "shiftY", "shY", OpenMaya.MFnNumericData.kDouble, 0.0 )
	nAttr.setKeyable(True)

	nAttr = OpenMaya.MFnNumericAttribute()
	jpCacheNode.shiftZ = nAttr.create( "shiftZ", "shZ", OpenMaya.MFnNumericData.kDouble, 0.0 )
	nAttr.setKeyable(True)

	# add attribute
	#try:
	outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom
	
	jpCacheNode.addAttribute( jpCacheNode.time )

	jpCacheNode.addAttribute( jpCacheNode.shiftX )
	jpCacheNode.addAttribute( jpCacheNode.shiftY )
	jpCacheNode.addAttribute( jpCacheNode.shiftZ )

	jpCacheNode.attributeAffects( jpCacheNode.time, outputGeom )
	jpCacheNode.attributeAffects( jpCacheNode.shiftX, outputGeom )
	jpCacheNode.attributeAffects( jpCacheNode.shiftY, outputGeom )
	jpCacheNode.attributeAffects( jpCacheNode.shiftZ, outputGeom )
	#except:
	#	sys.stderr.write( "Failed to create attributes of %s node\n", kPluginNodeTypeName )

# initialize the script plug-in
def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode( kPluginNodeTypeName, jpCacheNodeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kDeformerNode )
	except:
		sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( jpCacheNodeId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )