### Description 
PRGViewer program designed for viewing files of prg format.

#### Features
* Work with commands Pick&Place (code 25) and Dispense (code 107)
* Support format files version #1 and #2. File format #1 may not have header.
* Files with empty columns are not supported (they should at least once to open in APS_Main and save). 

### System requirements
* Windows XP and up
* Python 3.3 and up
* cx_freeze 4.3.x and up (for freeze to exe file)

### Setup - freeze
1. Unpack archive
2. In Command line input "setup.py build"

### Setup (for freezed version)
1. Copy all files from all files build\exe.win32-3.3 folder into new folder
2. Right-click on any prg file
3. Select Open with
4. In the dialog, select the file PRGViewer.exe

### Run
Run PRGViewer.exe or click any prg file.

### Usage
* Use mouse wheel for select file.
* Use left mouse button for load file.
* Use Up/Down/Left/Right button for move field.
* Use Show/Hide description radiobuttons for change description vision mode .
* Use +/- buttons for change scale of fields.
* For backlight of a group of components in the listbox, click on one of the items for filter selection.
* For turning off the backlight, click on the item Nothing in the listbox.