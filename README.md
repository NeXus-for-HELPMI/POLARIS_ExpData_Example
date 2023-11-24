# Case study: Investigation of the applicability of the NeXus format for high intensity lasers and related experiments 

HELPMI (HElmholtz Laser-Plasma Metadata Initiative) is a 2 year project of GSI, HI Jena and HZDR, funded by the Helmholtz Metadata Collaboration, which addresses the problem that no data standard exists for ultra-high intensity laser plasma experiments, hampering the F.A.I.R. principles and associated emerging benefits.

Here we would like to test whether we can achieve the **"I"** standing for **I**nteroperability with the help of the NeXus standard.

This repository contains an example of some date collected in the [POLARIS](https://de.wikipedia.org/wiki/Polaris_(Laser)) laboratory during a proton acceleration experiment on a mass-limited target, in this case H~2~O dropplets

It contains a folder for some shots (001,002...). Inside are folders for respective diagnostic cameras. The laser focus is checked before the experiment. The images are in the "Focus" folder. 

If the [HIJ-Vision library](https://github.com/Vision-For-Laserlab) was used for the cameras, a report file (*.data) is saved for each image. The data file contains information about:
 - camera settings
 - background image, if taken and subtracted
 - image calibration 
 - Region Of Interest
 - target position
 - evaluation parameters

These data is important to facilitate the traceability of the evaluation results, stored also in the file.

The GCCD is a 3td closed application and stores the images with continuous numbers. The focus is checked before the experiment.

The Excel Table "Shotsheet.xlsx" contains additional measurements, important settings and comments.

With the Jupyter notebook "Map Shots to NeXus.ipynb" we try to find a NeXus representation for the experemental data. The HDF5 files are the resulting NeXus files.

## Question and suggestions:
a.kessler@hi-jena.gsi.de
