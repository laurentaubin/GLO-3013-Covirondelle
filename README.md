# covirondelle-station

## Get started
Follow these instructions to get a copy of the project up and running on your local machine


### Run the app locally using Docker
Make sure you have the latest versions of [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

Build the app:
```bash
docker-compose build
```

Run the app:
```bash
docker-compose up
```

Additionally, you can do both at the same time:
```bash
docker-compose up --build
```

*N.b. If this is your first time running the app using docker, the `covirondelle-station` project must be runned first. Alternatively, if you do not want to run the `covirondelle-station` project, run the following command beforehand:*
```bash
docker network create covirondelle-station_default
```


### Run the app in prod environment
#### Install packages
For of all, you need to install ``virtualenv``. To do so,  run the following command:
```bash
pip install virtualenv
```

Once ``virtualenv`` is downloaded, go to the root of the project and run the following commands:
```bash
virtualenv -p python3 venv
source venv/bin/activate
```

This activates a virtual environment where you can install all the dependencies to run the project.

Then, run 
```bash
pip install -r requirements.txt
```

All the dependencies should be installed and the app is ready to run.

To deactivate the virtual environment, just run ```deactivate``` in your command line.

#### Configure communication between station and robot
Navigate to `src/config/config.py` and update the `SOCKET_STATION_ADDRESS` field with the station's IP address when in the lab.

#### Run the app
```bash
make run
```

### Testing and linting
run all tests:
```bash
make test
```

If you are on Windows and cant use `make`, you can try to run:
```bash
python -m nose test
```

run formatter on source and test files: 
```bash
make format
```

If you are using Pycharm and want to format the code on save, follow these [instructions](https://black.readthedocs.io/en/stable/editor_integration.html) (Black documentation)

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






