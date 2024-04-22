# Programming Coursework Smart Home App

A Smart Home app protoype written in Python using the Tkinter Graphical User Interface. This was submitted as the second piece of coursework for the first-year Programming module at the University of Portsmouth.

## Main Features

### Fully Interactive GUI 

A fully interactive and working app where you can add, edit and remove devices from your 'Smart Home.

### Interface & Accessibility Settings

Functioning Accessibility Settings such as, a light and dark mode, a custom colour scheme that you can choose and changing the character size.

### Permanent Data Storage

Allows you to save the state of your current 'Smart Home' and upload a previously saved state.

### Device Scheduler

Lets you set specific times for devices to turn on or off automatically.

#### Pre-Defined Layout

All patchwork samples have a layout which determines the arrangement and colouring of patch designs. This layout was determined by our student numbers and so is pre-defined here.

### Patches

Individual patches are 100 × 100 in size and contain one of two geometric designs comprising several shapes, as determined by the layout.

### Input

Upon running the program, the user is prompted via the shell to enter:

* The __device__ the user would like to add (Smart Plug or Smart Oven)
* The consumption rate if 'Smart Plug' was chosen (the rate of power consumption)

#### Valid Sizes

Valid sizes for the patchwork samples are __5 × 5__, __7 × 7__, or __9 × 9__. These are multiplied by 100 to give the dimensions of the window.

The expected input is just one number that will be the common value for both the width and height.

#### Valid Colours

Valid colours for the patches are __blue__, __green__, __magenta__, __orange__, __pink__, or __red__.

### Editing

After a patchwork sample has been drawn, the user is able to interact with the patches it contains. They may select an individual patch by clicking on it and then pressing the following keys:

* if the selected patch has not been deleted:
    * the 'Enter' key to deselect the patch
    * the 's' key to switch the patch design to the other
    * the 'd' key to delete the patch, leaving an empty space
    
* if the selected patch has been deleted:
    * the key for the first letter of a valid colour to create a new patch with the second design of this colour
        * e.g. 'r' for 'red'

Other keys have no effect on a selected patch. When selected, a patch will show a thick black border.

## Requirements

This project uses features from John Zelle's graphics module, [graphics.py](https://mcsp.wartburg.edu/zelle/python/graphics.py). Please ensure this is installed for the patchwork sample to display.

To install, run the following command in the shell:

```
pip install -r requirements.txt
```

## Usage

To use the Smart Home GUI, run __frontend.py__.
