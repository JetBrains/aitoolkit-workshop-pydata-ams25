# AI-Toolkit Workshop PyData Amsterdam 2025  

## Install PyCharm  

[Download](https://www.jetbrains.com/pycharm/download) and install standalone PyCharm.  

## Install AI Agents Debugger Plugin

Download the zip archive of the plugin: [link](https://drive.google.com/file/d/1mgyU7oQlVn4qCaSuKvMvZBCpHoz77dL0).  
Then install it manually: 
 * Go to PyCharm
 * Settings (gear icon top-right corner) --> `Plugins`  
  <img src="images/plugins-1.png" alt="Screenshot" style="width: 55%; height: auto;">  
 * Gear icon (top-right-ish) --> `Install Plugin from Disk…`  
   <img src="images/plugin-install-from-disk.png" alt="Screenshot" style="width: 55%; height: auto;">  
 * Choose the downloaded .zip
 * `Save changes` (top-right)  

## Configure Python Environment  

Go to the project's root directory.  
First, [install uv](https://docs.astral.sh/uv/getting-started/installation/) if you haven't already.  
Install Python via uv:  
```bash
uv python install 3.10
```  
Install project dependencies:  
```bash
uv sync --all-packages --all-extras
```
Python virtual env `.venv` should appear in the project's root directory.  

### Configure Pytnon interpreter in PyCharm  

Click the interpreters section in botton-right of the screen:
Then choose `Add New Interpreter` --> `Add Local Interpreter...`:  
<img src="images/interpreter-add-local.png" alt="Screenshot" style="width: 50%; height: auto;">

The choose `Select existing` interpreter and then find your interpreter in local `.venv/bin` folder, then click OK:  
<img src="images/interpreter-select.png" alt="Screenshot" style="width: 50%; height: auto;">

## Test the plugin  

Run the `main` Run Config:  
<img src="images/run-main.png" alt="Screenshot" style="width: 60%; height: auto;">

You should see the AI Agents Debugger tool window on the right:  
<img src="images/traces-1.png" alt="Screenshot" style="width: 60%; height: auto;"> 
