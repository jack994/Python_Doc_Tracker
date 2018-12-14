# Python_Doc_Tracker
This application is a simple, data intensive application in Python 3 
able to analyse and display document tracking data from a major web site.  
  
Some external libraries need to be installed to allow the script to run (installation: "pip install <library>"). These are:  
- graphviz  
- pillow  
- httpagentparser  
- matplotlib  
- tkinter  
  
To run the application download the python script, install the library dependencies, and use the following command:  
- **python3 visualiser.py -g -f <file_name>** where file_name is the json file used as input.  
SAMPLE JSON FILES: [100k_lines.json](https://drive.google.com/uc?export=download&id=1YmkIeFBE462n-g5aHZMr9hQPMednEDTp), [600k_lines.json](https://drive.google.com/uc?export=download&id=1sEcVsiXycMWJvMcAThODM_80hcipYdsx)
  
**Functionality:**  
  
View by country/continent:  
- Take a Document ID string as input and output an histogram of countries of viewers.  
- Take a Document ID string as input and output an histogram of continents of viewers.  
  
Views by browser:  
- Take a Document ID string as input and output an histogram of user agents of viewers.  
- Take a Document ID string as input and output an histogram of browsers of viewers.  
  
Also-likes functionality:  
- Take a document ID and reader ID (optional) as parameters, the function returns a sorted list of liked documents.  
- Take a document ID and reader ID (optional) as parameters, the function returns graph created with "graphviz" displaying the relationship
between the input document and all documents that have been found as “also-liked” documents.  

