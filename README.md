# PSS
A scheduling program built using Python.

## How to use
### Windows
Run `python main.py` or `py main.py` from the root directory.

### macOS/Linux
Run `python3 main.py` from the root directory.

## Useful Terminal Commands
### Windows
`py -3 -m venv .venv` or `python -m venv .venv` to create a virtual environment in the current directory.
`.venv\scripts\activate` to activate the virtual environment.
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` if you get an error when trying to activate the virtual environment.

#### Deploying to other machines
`pip install -r requirements.txt` to easily install all required packages.
`pip freeze --local > requirements.txt` to generate the requirements.txt file after installing any new packages.

### macOS/Linux
`python3 -m venv .venv` to create a virtual environment in the current directory
`sudo apt-get install python3-venv` may need to be ran first

### Deploying to other machines
`pip3 install -r requirements.txt` to easily install all required packages.
`pip3 freeze --local > requirements.txt` to generate the requirements.txt file after installing any new packages.