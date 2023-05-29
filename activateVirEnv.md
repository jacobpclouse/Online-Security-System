## SETUP VIRT ENVIR:

0) Update Pip:
```pip install --upgrade pip```


1) Create New Virtural Envir. (when first starting up -- you can use any name) - 
    - If python2 and python3 is installed:
        ```python3 -m venv venvName```
    - Else:
        ```python -m venv venvName```


2) Activate Virtual Envir. 
    - (LINUX:) ```source venvName/bin/activate```
    - (WINDOWS: ) ```source venvName/Scripts/activate```


3) Install Packages inside it:
```python -m pip install <package-name>```


4) Deactivate Virtual Envir:
```deactivate```

------------------------------


## INSTALL REQUIREMENTS.TXT:
```pip install -r requirements.txt```


------------------------------


## PIP FREEZE REQUIREMENTS.TXT:
```pip freeze > requirements.txt```


------------------------------
From:
https://realpython.com/python-virtual-environments-a-primer/

<br>

### Virtual link:
```cd venv/lib/python2.7 && ln -s /usr/local/lib/python2.7/dist-packages/cv2.so``` <br>
```cd venv/lib/python2.7 && ln -s /usr/local/lib/python2.7/dist-packages/cv.py``` <br>
<br>
```cd venv1/lib/python3.8 && ln -s /usr/local/lib/python3.8/dist-packages/cv2.so``` <br>
```cd venv1/lib/python3.8 && ln -s /usr/local/lib/python3.8/dist-packages/cv.py``` <br>