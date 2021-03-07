# covirondelle-station

## Get started
Follow these instructions to get a copy of the project up and running on your local machine

### Run the app locally using Docker
Make sure you have the latest versions of [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

build the app:
```bash
docker-compose build
```

run the app:
```bash
docker-compose up
```

Additionally, you can do both at the same time:
```bash
docker-compose up --build
```

### Run the app in a prod environment
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
Make sure the station's IP address is correctly set in the robot's config file. See `covirondelle-robot`'s README for further information.

#### Run the app
```bash
make run
```

### Testing and linting
#### Run all tests
```bash
make test
```

If you are on Windows and can't use `make`, you can try to run:
```bash
python -m nose test
```

#### Run formatter on source and test files: 
```bash
make format
```

If you are using Pycharm and want to format the code on save, follow these [instructions](https://black.readthedocs.io/en/stable/editor_integration.html) (Black documentation)

#### Linting
```bash
make lint
```

#### Generate coverage report
To generate a command line report, run:
```bash
make coverage
```
To generate an html report, run:
```bash
make coverage-html
```
Then, navigate to the `reports/` directory and open `index.html`




