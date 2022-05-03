# PSS
A scheduling program built using Python.

## How to use
run `main.py`

## Useful Terminal Commands
`py -3 -m venv .venv` to create a virtual environment in the current directory
`.venv\scripts\activate` to activate the virtual environment

`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` if you get an error when trying to activate the virtual environment

`pip install -r requirements.txt` to easily install all required packages to run this program
`pip freeze --local > requirements.txt` to re-generate the requirements.txt file after installing any new packages