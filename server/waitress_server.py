import os

from waitress import serve
import app

## Run from the same directory as this script
#this_files_dir = os.path.dirname(os.path.abspath(__file__))
#os.chdir(this_files_dir)
myDir = 'd:\\theta-asrs\\asrs\\server'
os.chdir(myDir)

serve(app.app, host='0.0.0.0', port=6080)