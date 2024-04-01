# digiCamControlPython

Simple python class to use digiCamControl via the [single command system](https://digicamcontrol.com/doc/userguide/remoteutil) to control your camera. [Digicamcontrol](https://digicamcontrol.com/) needs to be installed and running. Supports cameras from many popular manufacturers such as Nikon, Canon, Sony as well as GoPro. A list of compatible cameras can be found [here](https://digicamcontrol.com/cameras).

## Example code:
``` Python

# Setup
import digiCamControlPython as dccp
camera = dccp.Camera()

camera.set_iso(100)
>>> Set the Iso to 100

camera.get_shutterspeed()
>>> Current shutterspeed: 1/125

camera.list_compression()
>>> List of all possible compressionsettings: ['JPEG (BASIC)', 'JPEG (NORMAL)', 'JPEG (FINE)', 'RAW', 'RAW + JPEG (BASIC)', 'RAW + JPEG (NORMAL)', 'RAW + JPEG (FINE)']

camera.set_autofocus("off")
>>> Autofocus is off.

camera.set_transfer("Save_to_PC_only")

camera.set_folder(r"C:\Images\")
>>> Set the session.folder to C:\Images\

camera.capture()
>>> Captured image.
>>> Current lastcaptured: Image1.jpg

```


