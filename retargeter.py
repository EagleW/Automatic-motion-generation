# -*- coding: utf-8 -*-
"""
FILE:     retargeter.py
AUTHOR:   Qingyun Wang(dalewanghz@gail.com)
DATE:     07.18.2017
REVISION:
REVISION DATE:
PURPOSE:   Retarget multiple bvh files to multiple fbx files to generate synthetic
           video
INFO:
************************************************************************
INPUTS:     newCharPopup: The folder includes all fbx chracter files.
            oldAnimsPopup: The folder includes all bvh motion files.
OUTPUTS:   A bunch of videos that are generated by retargeting bvh to the fbx.
"""

import os
import re
from pyfbsdk import *
import time
from random import randint
bipedPrefixNamingScheme = True

# This is the Motionbuilder mapping to use the same function.
mobuMap = {'Reference' : 'BVH:reference',
            'Hips':'BVH:Hips',
             'LeftUpLeg' : 'BVH:LeftUpLeg',
             'LeftLeg' : 'BVH:LeftLeg',
             'LeftFoot' : 'BVH:LeftFoot',
             'RightUpLeg' : 'BVH:RightUpLeg',
             'RightLeg' : 'BVH:RightLeg',
             'RightFoot' : 'BVH:RightFoot',
             'Spine' : 'BVH:Spine',
             'LeftArm' : 'BVH:LeftArm',
             'LeftForeArm' : 'BVH:LeftForeArm',
             'LeftHand' : 'BVH:LeftHand',
             'RightArm' : 'BVH:RightArm',
             'RightForeArm' : 'BVH:RightForeArm',
             'RightHand' : 'BVH:RightHand',
             'Head' : 'BVH:Head',
             'LeftShoulder' : 'BVH:LeftShoulder',
             'RightShoulder' : 'BVH:RightShoulder',
             'Neck' : 'BVH:Neck',
             'Spine1' : 'BVH:Spine1',
             'Spine2' : 'BVH:Spine2',
             'Spine3' : 'BVH:Spine3',
             'Spine4' : 'BVH:Spine4',
             'Spine5' : 'BVH:Spine5',
             'Spine6' : 'BVH:Spine6',
             'Spine7' : 'BVH:Spine7',
             'Spine8' : 'BVH:Spine8',
             'Spine9' : 'BVH:Spine9',
             'Neck1' : 'BVH:Neck1',
             'Neck2' : 'BVH:Neck2',
             'Neck3' : 'BVH:Neck3',
             'Neck4' : 'BVH:Neck4',
             'Neck5' : 'BVH:Neck5',
             'Neck6' : 'BVH:Neck6',
             'Neck7' : 'BVH:Neck7',
             'Neck8' : 'BVH:Neck8',
             'Neck9' : 'BVH:Neck9',
             'LeftFingerBase' : 'BVH:LeftFingerBase',
             'LeftHandThumb1' : 'BVH:LThumb_End',
             'LeftHandThumb2' : 'BVH:LeftHandThumb2',
             'LeftHandThumb3' : 'BVH:LeftHandThumb3',
             'LeftHandIndex1' : 'BVH:LeftHandIndex1',
             'LeftHandIndex2' : 'BVH:LeftHandIndex1_End',
             'LeftHandIndex3' : 'BVH:LeftHandIndex3',
             'LeftHandMiddle1' : 'BVH:LeftHandMiddle1',
             'LeftHandMiddle2' : 'BVH:LeftHandMiddle2',
             'LeftHandMiddle3' : 'BVH:LeftHandMiddle3',
             'LeftHandRing1' : 'BVH:LeftHandRing1',
             'LeftHandRing2' : 'BVH:LeftHandRing2',
             'LeftHandRing3' : 'BVH:LeftHandRing3',
             'LeftHandPinky1' : 'BVH:LeftHandPinky1',
             'LeftHandPinky2' : 'BVH:LeftHandPinky2',
             'LeftHandPinky3' : 'BVH:LeftHandPinky3',
             'RightFingerBase' : 'BVH:RightFingerBase',
             'RightHandThumb1' : 'BVH:RThumb_End',
             'RightHandThumb2' : 'BVH:RightHandThumb2',
             'RightHandThumb3' : 'BVH:RightHandThumb3',
             'RightHandIndex1' : 'BVH:RightHandIndex1',
             'RightHandIndex2' : 'BVH:RightHandIndex1_End',
             'RightHandIndex3' : 'BVH:RightHandIndex3',
             'RightHandMiddle1' : 'BVH:RightHandMiddle1',
             'RightHandMiddle2' : 'BVH:RightHandMiddle2',
             'RightHandMiddle3' : 'BVH:RightHandMiddle3',
             'RightHandRing1' : 'BVH:RightHandRing1',
             'RightHandRing2' : 'BVH:RightHandRing2',
             'RightHandRing3' : 'BVH:RightHandRing3',
             'RightHandPinky1' : 'BVH:RightHandPinky1',
             'RightHandPinky2' : 'BVH:RightHandPinky2',
             'RightHandPinky3' : 'BVH:RightHandPinky3',
             'LeftInHandThumb' : 'BVH:LThumb',
             'RightInHandThumb' : 'BVH:RThumb',
             'LeftFootThumb1' : 'BVH:LeftFootThumb1',
             'LeftFootThumb2' : 'BVH:LeftFootThumb2',
             'LeftFootThumb3' : 'BVH:LeftFootThumb3',
             'LeftFootIndex1' : 'BVH:LeftFootIndex1',
             'LeftFootIndex2' : 'BVH:LeftFootIndex2',
             'LeftFootIndex3' : 'BVH:LeftFootIndex3',
             'LeftFootMiddle1' : 'BVH:LeftFootMiddle1',
             'LeftFootMiddle2' : 'BVH:LeftFootMiddle2',
             'LeftFootMiddle3' : 'BVH:LeftFootMiddle3',
             'LeftFootRing1' : 'BVH:LeftFootRing1',
             'LeftFootRing2' : 'BVH:LeftFootRing2',
             'LeftFootRing3' : 'BVH:LeftFootRing3',
             'LeftFootPinky1' : 'BVH:LeftFootPinky1',
             'LeftFootPinky2' : 'BVH:LeftFootPinky2',
             'LeftFootPinky3' : 'BVH:LeftFootPinky3',
             'RightFootThumb1' : 'BVH:RightFootThumb1',
             'RightFootThumb2' : 'BVH:RightFootThumb2',
             'RightFootThumb3' : 'BVH:RightFootThumb3',
             'RightFootIndex1' : 'BVH:RightFootIndex1',
             'RightFootIndex2' : 'BVH:RightFootIndex2',
             'RightFootIndex3' : 'BVH:RightFootIndex3',
             'RightFootMiddle1' : 'BVH:RightFootMiddle1',
             'RightFootMiddle2' : 'BVH:RightFootMiddle2',
             'RightFootMiddle3' : 'BVH:RightFootMiddle3',
             'RightFootRing1' : 'BVH:RightFootRing1',
             'RightFootRing2' : 'BVH:RightFootRing2',
             'RightFootRing3' : 'BVH:RightFootRing3',
             'RightFootPinky1' : 'BVH:RightFootPinky1',
             'RightFootPinky2' : 'BVH:RightFootPinky2',
             'RightFootPinky3' : 'BVH:RightFootPinky3',
             'LeftUpLegRoll' : 'BVH:LeftUpLegRoll',
             'LeftLegRoll' : 'BVH:LeftLegRoll',
             'RightUpLegRoll' : 'BVH:RightUpLegRoll',
             'RightLegRoll' : 'BVH:RightLegRoll',
             'LeftArmRoll' : 'BVH:LeftArmRoll',
             'LeftForeArmRoll' : 'BVH:LeftForeArmRoll',
             'RightArmRoll' : 'BVH:RightArmRoll',
             'RightForeArmRoll' : 'BVH:RightForeArmRoll' }
#this dictionary stored the potential camera position
camera = {
"pos":[[ 50, 50, 1000],[1000, 50, 50]],
"rotate":[ [0, 90, 0],[170,0,170]]
}

light = {
"pos":[[200,200,10]],
"rotate":[[100,0,0]]
}

def addJointToCharacter ( characterObject, slot, jointName ):
    myJoint = FBFindModelByLabelName(jointName)
    if myJoint:
        proplist = characterObject.PropertyList.Find(slot + "Link")
        proplist.append (myJoint)

def CharacterizeBiped(rootname, useBipedPrefixNamingScheme, nameprefix, boneMap, models):

    system = FBSystem()
    app = FBApplication()

    longname = models.LongName
    namespaceindex = longname.rfind(":")
    if namespaceindex != -1:
        namespace = longname[0:namespaceindex+1]
        name = longname[namespaceindex + 1:]
    else:
        namespace = ""
        name = longname

    myBiped = FBCharacter("mycharacter")
    app.CurrentCharacter = myBiped

    # If in Biped mode, extract the character prefix name
    if useBipedPrefixNamingScheme:
        splitname = name.split()
        nameprefix = splitname[0] + " "
        # Override the rootname so it is the character orefix name
        rootname = splitname[0]
        myBiped.LongName = namespace + rootname
    else:
        myBiped.LongName = namespace + nameprefix + rootname


    # Create a FBProgress object and set default values for the caption and text.
    fbp = FBProgress()
    fbp.Caption = ""
    fbp.Text = " -----------------------------------   Creating Biped character"
    progress = 0.0
    progresssteps = len(boneMap)

    # assign Biped to Character Mapping.
    for pslot, pjointName in boneMap.iteritems():
        if not pjointName:
            addJointToCharacter (myBiped, pslot, namespace + rootname)
        else:
            addJointToCharacter (myBiped, pslot, namespace + nameprefix + pjointName)
        progress += 1
        val = progress / len(boneMap)  * 100
        fbp.Percent = int(val)

    switchOn = myBiped.SetCharacterizeOn( True )
    print "Character mapping created for " + (myBiped.LongName)

    # We must call FBDelete when the FBProgress object is no longer needed.
    fbp.FBDelete()
    return myBiped



def plotAnim(char, animChar):
    """
    Receives two characters, sets the input of the first character to the second
    and plot. Return ploted character.
    """
    if char.GetCharacterize:
        switchOn = char.SetCharacterizeOn(True)

    plotoBla = FBPlotOptions()
    plotoBla.ConstantKeyReducerKeepOneKey = True
    plotoBla.PlotAllTakes = True
    plotoBla.PlotOnFrame = True
    plotoBla.PlotPeriod = FBTime( 0, 0, 0, 1 )
    #plotoBla.PlotTranslationOnRootOnly = True
    plotoBla.PreciseTimeDiscontinuities = True
    #plotoBla.RotationFilterToApply = FBRotationFilter.kFBRotationFilterGimbleKiller
    plotoBla.UseConstantKeyReducer = False
    plotoBla.ConstantKeyReducerKeepOneKey  = True

    char.InputCharacter = animChar
    char.InputType = FBCharacterInputType.kFBCharacterInputCharacter
    char.ActiveInput = True
    if (not char.PlotAnimation(FBCharacterPlotWhere.kFBCharacterPlotOnSkeleton, plotoBla)):
        FBMessageBox( "Something went wrong", "Plot animation returned false, cannot continue", "OK", None, None )
        return False

    return char



def main():

    # asking for the character, already characterized
    newCharPopup = FBFolderPopup();
    newCharPopup.Caption = "Select an already Characterized folder"
    newCharPopup.Filter = "*.fbx"
    newCharPopup.Path = "C:\\Users\\ISL-WORKSTATION\\Desktop\\motionbuilder\\automatic"
    fileList_char = []
    if newCharPopup.Execute():
        # Getting the names of the files in your previously selected folder
        # Using os to get the file names from the specified folder (above) and storing names of files in a list
        allList_char = os.listdir(newCharPopup.Path)
        # Setting the regular expression to only look for .fbx or .bvh extenstion
        fbxRE = re.compile('^\w+.fbx$', re.I)
        # Removing any files that do not have an .fbx extenstion
        for fname in allList_char:
            mo = fbxRE.search(fname)
            if mo:
                fileList_char.append(fname)
    else:
        FBMessageBox( "Selection canceled", "Character selection canceled.", "OK", None, None )
        return False

    # asking which file format to load. ".fbx" might have a character on the scene.

    fileFormat = ".bvh"

    # asking for the animations folder
    # this part should be changed to load other formats
    # in theory it should work with any skeleton that can be characterized.
    oldAnimsPopup = FBFolderPopup()
    oldAnimsPopup.Caption = "Animations to retarget"
    oldAnimsPopup.Filter = "*" + fileFormat
    oldAnimsPopup.Path = newCharPopup.Path # easier to navigate

    fileList = []
    if oldAnimsPopup.Execute():
        # Getting the names of the files in your previously selected folder
        # Using os to get the file names from the specified folder (above) and storing names of files in a list
        allList = os.listdir(oldAnimsPopup.Path)
        # Setting the regular expression to only look for .fbx or .bvh extenstion
        bvhRE = re.compile('^\w+.bvh$', re.I)
        # Removing any files that do not have an .fbx extenstion
        for fname in allList:
            mi = bvhRE.search(fname)
            if mi:
                fileList.append(fname)
    else:
        FBMessageBox( "Animations selection canceled", "Cannot continue without animations.", "OK", None, None )
        return False

    userRoot = ["Hips/Pelvis", "Hips"]
    boneMap = bipedMap
    bipedPrefixNamingScheme = False
    prefix = ["",""]
    for filename_char in fileList_char:

        app = FBApplication()
        scene = FBSystem().Scene
        filename = newCharPopup.Path  + "\\" + filename_char
        print(filename_char)
        # get root name from the skeleton on the animations folder


        # iterate through animation list
        for animName in fileList:

            app.FileNew()
            scene.Evaluate()
            app.FileOpen(filename)

            newChar = app.CurrentCharacter
            if not newChar:
                FBMessageBox( "Not characterized", "No characterized character on the character scene.", "OK", None, None )
                return False

            # FileMerge() can load only native .fbx, and it loads characters if they are present, of course
            # FileImport() on the other hand just imports the file into the scene
            if fileFormat == ".fbx":
                # setup load/merge options
                lOptions = FBFbxOptions(True) # true = load options
                lOptions.CustomImportNamespace = "merged"
                app.FileMerge(oldAnimsPopup.Path + "\\" + animName, False, lOptions)
            else:
                app.FileImport(oldAnimsPopup.Path + "\\" + animName, False) # False means it will create objects regardless


            # if there's no character in the merged animation scene we need to characterize it
            if len(scene.Characters) == 1:

                # find root model to pass to CharacterizeBiped()
                # if merging FBX, it has custom namespace
                if fileFormat == ".fbx":
                    oldAnimRoot = FBFindModelByLabelName("merged:" + prefix[1] + userRoot[1])
                # if importing BVH, it will have it's own BVH: namespace
                else:
                    oldAnimRoot = FBFindModelByLabelName(prefix[1] + userRoot[1])

                if not oldAnimRoot:
                    FBMessageBox( "Could not find hips object", "Check opened scene. Root node name must be given without namespace.", "OK", None, None )
                    return False

                # characterize imported animation with modified 3dsmaxbipedtemplate.py
                oldAnimChar = CharacterizeBiped(userRoot[1], bipedPrefixNamingScheme, prefix[1], boneMap, oldAnimRoot)

            else:
                # merged FBX with an character present in the scene
                oldAnimChar = scene.Characters[1]


            # plot
            charToSave = plotAnim(newChar, oldAnimChar)
            for i in range(0, 2):
                #
                mylight = FBLight("mylight")
                mylight.LightType = FBLightType.kFBLightTypePoint
                mylight.SetVector( FBVector3d(light["pos"][0][0],light["pos"][0][1],light["pos"][0][2]))
                mylight.SetVector( FBVector3d(light["rotate"][0][0],light["rotate"][0][1],camera["rotate"][0][2]), FBModelTransformationType.kModelRotation)
                mylight.Show = True
                x = "Camera1"
                myCamera = FBCamera(x)
                myCamera.SetVector( FBVector3d( camera["pos"][i][0], camera["pos"][i][1], camera["pos"][i][2] ) )
                myCamera.SetVector( FBVector3d( camera["rotate"][i][0], camera["rotate"][i][1], camera["rotate"][i][2] ), FBModelTransformationType.kModelRotation)
                FBSystem().Renderer.Render()
                FBSystem().Scene.Renderer.SetCameraInPane( myCamera, 0 )
                # hide Axis and grid from renders
                for lCamera in FBSystem().Scene.Cameras:
                    lCamera.ViewShowAxis = False
                    lCamera.ViewShowGrid = False
                FBPlayerControl().Goto(FBTime(0, 0, 0, 0))
                try:
                    mgr = FBVideoCodecManager()
                    # By specifying Codec stored, the first time we render a scene, the codec dialog
                    # will ve available if user press con configure
                    # the second time a scene is rendered, the same settings will be used.
                    mgr.VideoCodecMode = FBVideoCodecMode.FBVideoCodecUncompressed
                    filename_char_origin = (filename_char + "%d") % i
                    lDstFileName = os.path.join(newCharPopup.Path, filename_char_origin.replace( '.fbx', '_' ) + animName.replace( 'bvh', 'avi' ))
                    lOptions = FBVideoGrabber().GetOptions()
                    timeSpan = FBSystem().CurrentTake.LocalTimeSpan
                    start = FBTime()
                    start.SetTime( 0,0,0, 1 )
                    timeSpan.Set(start, timeSpan.GetStop())
                    lOptions.TimeSpan =  timeSpan
                    # render first time: user can specify rendering params
                    lOptions.OutputFileName = lDstFileName
                    app.FileRender( lOptions )


                except Exception, e:
                    # Unkown error encountered... Maybe from the 'listdir' call failing...
                    FBMessageBox( "ERROR", "Unknown error encountered. Aborting! " + str(e), "OK", None, None )
                del( myCamera,mylight)
                # unhide axis and grid from scene
                for lCamera in FBSystem().Scene.Cameras:
                    lCamera.ViewShowAxis = True
                    lCamera.ViewShowGrid = True





main()
del(bipedPrefixNamingScheme, bipedMap, mobuMap)
