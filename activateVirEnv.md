## SETUP VIRT ENVIR:

0) Update Pip:
```pip install --upgrade pip```
<br>
<br>

1) Create .gitignore and push Virtural Envir name into it (when first starting up -- you can use any name):
```echo "venvName/" > .gitignore```
    - You will need to add the names of the other folders you don't want to track into this 
<br>
<br>

2) Create New Virtural Envir. (use same name as you did in the .gitignore) 
    - If python2 and python3 is installed:
        ```python3 -m venv venvName```
    - Else:
        ```python -m venv venvName```
<br>
<br>


3) Activate Virtual Envir. 
    - (LINUX:) ```source venvName/bin/activate```
    - (WINDOWS: ) ```source venvName/Scripts/activate```
<br>
<br>

4) Install Packages inside it:
```python -m pip install <package-name>```
<br>
<br>

5) Deactivate Virtual Envir:
```deactivate```
<br>
<br>

> From: https://realpython.com/python-virtual-environments-a-primer/
------------------------------


## INSTALL REQUIREMENTS.TXT:
```pip install -r requirements.txt```


------------------------------


## PIP FREEZE REQUIREMENTS.TXT:
```pip freeze > requirements.txt```


------------------------------


## Check which python version you are using:
- If both python2 and python3 are installed:
    ```which python3```
- Else:
    ```which python```
- You want the version of python to be the one inside your project folder


------------------------------

<br>

### Virtual link:
```cd venv/lib/python2.7 && ln -s /usr/local/lib/python2.7/dist-packages/cv2.so``` <br>
```cd venv/lib/python2.7 && ln -s /usr/local/lib/python2.7/dist-packages/cv.py``` <br>
<br>
```cd venv1/lib/python3.8 && ln -s /usr/local/lib/python3.8/dist-packages/cv2.so``` <br>
```cd venv1/lib/python3.8 && ln -s /usr/local/lib/python3.8/dist-packages/cv.py``` <br>