# NFTracker
## Overview
This program will read collection names from a txt file and output the stats into an excel spreadsheet with each collection as a different sheet in the workbook.
## Setup
The setup of this project is relativly easy, make sure that you have python installed and then just run the run.bat file. If youre on MAC install the openpyxl and requests libraries and run the python script
## Configuration
Place the names of collections in the collections.txt file **NOTE:** the names of the collections must be the names that appear in the url on OpenSea website. For example, https://opensea.io/collection/boredapeyachtclub is the URL for Bored Ape Yacht Club, therefore the name in the collections.txt would be everything after the last '/' (boredapeyachtclub). 
### Thanks to Opensea for providing the API
