import os
import subprocess
import time
import psutil

# Simple python class to use digiCamControl via the single command system to control your camera.
# Digicamcontrol (https://digicamcontrol.com/) needs to be installed.
# For documentation please visit https://github.com/Eagleshot/digiCamControlPython

class Camera:
    'Python interface for the open source digicamcontrol software. Initialize the program by specifying where digiCamControl is installed. If left empty, the default location (C:/Program Files (x86)/digiCamControl) will be assumed. If openProgram is set to true, digiCamControl will automatically be opened in the background.'
    captureCommand = "capture "
    
    def __init__(self, exeDir = r"C:\Program Files (x86)\digiCamControl", verbose = True):
        
        if (os.path.exists(exeDir + r"/CameraControlRemoteCmd.exe")): # Check if file path exists
            self.exeDir = exeDir
            self.verbose = verbose # TODO Add ability to mute output
            
            if not "CameraControl.exe" in (i.name() for i in psutil.process_iter()): # Open program if closed
                self.openProgram()
                time.sleep(10)
        
        else:
            print("Error: digiCamControl not found.")
            
    
    def openProgram(self):
        'Opens the CameraControl.exe application.'
        subprocess.Popen(self.exeDir + r"/CameraControl.exe")
        
    #%% Capture  
    def capture(self, location = ""):
        'Takes a photo - filename and location can be specified in string location, otherwise the default will be used.' 
        r = self.runCmd(self.captureCommand + " " + location)
        if r == 0:
            print("Captured image.")
            
        return self.__getCmd("lastcaptured" )
    
    #%% Folder
    def setFolder(self, folder: str):
        'Set the folder where the pictures are saved.'
        self.__setCmd("session.folder", folder)

    def setImageName(self, name: str):
        'Set the name of the images.'
        self.__setCmd("session.name", name)
        
    def setCounter(self, counter = 0):
        'Set the counter to a specific number (default = 0).'
        self.__setCmd("session.Counter", str(counter))
        
    #%% Transfer mode
    def setTransfer(self, location: str):
        'Define where the pictures should be saved - "Save_to_camera_only", "Save_to_PC_only" or "Save:to_PC_and_camera"'
        return self.runCmd("set transfer %s" % (location))
        print("The pictures will be saved to %s." % location)

    #%% Autofocus
    def showLiveView(self):
        self.runCmd("do LiveViewWnd_Show")
        print("Showing live view window.")
    
    def setAutofocus(self, status):
        'Turn the autofocus on (default) or off - eg. "on" or "off"'
        if status == True:
            self.captureCommand = "Capture"
            print("Autofocus is on.")
        else:
            self.captureCommand = "CaptureNoAf"
            print("Autofocus is off.")
    
    #%% Shutterspeed
    def setShutterspeed(self, shutterspeed: str):
        'Set the shutter speed - eg. "1/50", "1/250" or 1s.'
        return self.__setCmd("shutterspeed", shutterspeed)
    
    def getShutterspeed(self):
        'Get the current shutter speed - eg. "1/50", "1/250" or 1s.'
        return self.__getCmd("shutterspeed")
    
    def listShutterspeed(self):
        'Get a list off all possible shutter speeds - eg. "1/50", "1/250" or 1s.'
        return self.__listCmd("shutterspeed")

    #%% ISO
    def setIso(self, iso: int):
        'Set the current ISO value - eg. 100, 200 or 400.'
        return self.__setCmd("Iso", str(iso))
     
    def getIso(self,):
        'Get the current ISO value - eg. 100, 200 or 400.'
        return self.__getCmd("Iso")

    def listIso(self,):
        'Get a list off all possible ISO values - eg. 100, 200 or 400.'
        return self.__listCmd("Iso")
       
    #%% Aperture
    def setAperture(self, aperture: float):
        'Set the aperture - eg. 2.8 or 8.0.'
        return self.__setCmd("aperture", str(aperture))
    
    def getAperture(self):
        'Get the current aperture - eg. 2.8 or 8.0.'
        return self.__getCmd("aperture")
    
    def listAperture(self):
        'Get a list off all possible aperture values - eg. 2.8 or 8.0.'
        return self.__listCmd("aperture")
    
    #%% Exposure Compensation
    def setExposureComp(self, ec: str):
        'Set the exposure compensation - eg. "-1.0" or "+2.3"'
        return self.__setCmd("exposurecompensation", ec)
    
    def getExposureComp(self):
        'Get the current exposure compensation - eg. "-1.0" or "+2.3"'
        return self.__getCmd("exposurecompensation")
    
    def listExposureComp(self):
        'Get a list off all possible exposure compensation values - eg. "-1.0" or "+2.3"'
        return self.__listCmd("exposurecompensation")
    
    #%% Compression
    def setCompression(self, comp: str):
        'Set the compression - eg. "RAW" or "JPEG (BASIC)"'
        return self.__setCmd("compressionsetting", comp)
    
    def getCompression(self):
        'Get the current compression - eg. "RAW" or "JPEG (BASIC)"'
        return self.__getCmd("compressionsetting")
    
    def listCompression(self):
        'Get a list off all possible compression setting - eg. "RAW" or "JPEG (BASIC)"'
        return self.__listCmd("compressionsetting")
    
    #%% Whitebalance   
    def setWhitebalance(self, wb: str):
         'Set the white balance - eg. "Auto" or "Daylight" or "Cloudy"'
         return self.__setCmd("whitebalance", wb)
     
    def getWhitebalance(self):
         'Get the current white balance - eg. "Auto" or "Daylight" or "Cloudy"'
         return self.__getCmd("whitebalance")
    
    def listWhitebalance(self):
         'Get a list off all possible white balance values - eg. "Auto" or "Daylight" or "Cloudy"'
         return self.__listCmd("whitebalance")

    #%% Commands
    def runCmd(self, cmd: str):
        'Run a generic command directly with CameraControlRemoteCmd.exe'
        r = subprocess.check_output("cd %s && CameraControlRemoteCmd.exe /c %s" % (self.exeDir, cmd), shell = True).decode()
        if 'null' in r: # Success
            return 0
        elif r'""' in r: # Success
            return 0
        else:           # Error
            print("Error: %s" % r) # Format output message
            return -1
    
    def __setCmd(self, cmd: str, value: str):
        'Run a set command with CameraControlRemoteCmd.exe'
        r = subprocess.check_output("cd %s && CameraControlRemoteCmd.exe /c set %s" % (self.exeDir, cmd + " " + value), shell = True).decode()
        if 'null' in r: # Success
            print("Set the %s to %s" % (cmd, value))
            return 0
        else:           # Error
             print("Error: %s" % r[109:]) # Format output message
             return -1
    
    def __getCmd(self, cmd: str):
        'Run a get command with CameraControlRemoteCmd.exe'
        r = subprocess.check_output("cd %s && CameraControlRemoteCmd.exe /c get %s" % (self.exeDir, cmd), shell = True).decode()
        if 'Unknown parameter' in r: # Error
            print("Error: %s" % r[109:]) # Format output message
            return -1
        else:           # Success
            returnValue = r[96:-6]
            print("Current %s: %s" % (cmd, returnValue)) # Format output message
            return returnValue
            
    def __listCmd(self, cmd: str):
        'Run a list command with CameraControlRemoteCmd.exe'
        r = subprocess.check_output("cd %s && CameraControlRemoteCmd.exe /c list %s" % (self.exeDir, cmd), shell = True).decode()
        if 'Unknown parameter' in r: # Error
            print("Error: %s" % r[109:]) # Format output message
            return -1
        else:           # Success
            returnList = r[96:-6].split(",") # Format response and turn into a list
            returnList = [e[1:-1] for e in returnList] # Remove "" from string
            print("List of all possible %ss: %s" % (cmd, returnList)) # Format output message
            return returnList


#%% Unittests
if __name__ == '__main__':
    
    # TODO: Coverage for whole document
    
    print("Beginning unit tests:")
    
    camera = Camera()
    
    assert(isinstance(camera.listShutterspeed(), list))
    temp = camera.listShutterspeed()[0]
    assert(camera.setShutterspeed(temp) == 0)
    assert(camera.getShutterspeed() == temp)
    
    assert(isinstance(camera.listIso(), list))
    temp = camera.listIso()[0]
    assert(camera.setIso(temp) == 0)
    assert(camera.getIso() == temp)
    
    assert(isinstance(camera.listAperture(), list))
    temp = camera.listAperture()[0]
    assert(camera.setAperture(temp) == 0)
    assert(camera.getAperture() == temp)
    
    assert(isinstance(camera.listExposureComp(), list))
    temp = camera.listExposureComp()[0]
    assert(camera.setExposureComp(temp) == 0)
    assert(camera.getExposureComp() == temp)
    
    assert(isinstance(camera.listCompression(), list))
    temp = camera.listCompression()[0]
    assert(camera.setCompression(temp) == 0)
    assert(camera.getCompression() == temp)
    
    assert(isinstance(camera.listWhitebalance(), list))
    temp = camera.listWhitebalance()[0]
    assert(camera.setWhitebalance(temp) == 0)
    assert(camera.getWhitebalance() == temp)
    
    print("End unit tests.")