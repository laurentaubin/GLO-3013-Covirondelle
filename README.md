# covirondelle-robot

## Get started
Follow these instructions to get a copy of the project up and running on your local machine


### Install packages
For of all, you need to install ``virtualenv``. To do so,  run the following command:
```bash
pip install virtualenv
```

Once ``virtualenv`` is downloaded, go to the root of the project and run the following commands:
```bash
virtualenv -p python3 venv

Linux : source venv/bin/activate
Windows : source venv/Scripts/activate
```

What that does is to activate a virtual environment where you can install all the dependencies to run the project.

Then, run 
```bash
pip install -r requirements.txt
```

All the dependencies should be installed and the app is ready to run.

To deactivate the virtual environment, just run ```deactivate``` in your command line.

### Run the app
*On windows, you can use ```mingw32-make``` instead of make

run the app:  
```bash
make run
```

run all tests:
```bash
make test
```

linting:
```bash
make lint
```

generate coverage report
```bash
coverage
or
coverage html
or 
coverage xml
```





