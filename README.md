# SENG2021 - e-Invoicing
Website: https://seng2021-app-d4e5c.web.app/

![test](https://github.com/SENG2021-22T1/ICECREAM/actions/workflows/test.yml/badge.svg)
![codecov](https://codecov.io/gh/SENG2021-22T1/ICECREAM/branch/main/graph/badge.svg?token=OAEBG7U0W9)

## Coverage report
https://codecov.io/gh/SENG2021-22T1/ICECREAM

## file structure
`src` is where we store the code. The entry point is `application.py`, which is not in `src`. This is because `Elastic Beanstalk` finds the file named `appliaction.py` in the `root` directory by default. `db_model` is a directory that stores the model of the database entity.

`routes.py` is where flask dispatches the apis. `auth.py` is in charge of authentication and athourization. `db.py` are functions that are related to the database. `email.py` is in charge of the functionality to send the invoice via email. `config.py` is storing the configurations.

`test` is where we store our tests. Integration tests are stored in `system_test` and unit tests are stored in `unit_test`.

## create a virtual environment
```bash
pip install virtualenv
virtualenv virt
source virt/bin/activate
```

## exit virtual environment
```bash
deactivate
```

## install dependencies
```bash
pip install -r requirements.txt
pip install pylint
pip install coverage
```

## create database
After downloading postgres, and starting postgresql.
```bash
createdb seng2021_db
python3 create_db.py
```

## linting
```bash
find . -type f -name "*.py" | xargs pylint
```

## test
```bash
python3 application.py &
coverage run -m pytest test/ --junitxml=pytest_report.xml
coverage report
coverage html
```

## create requirements.txt
Before running the following commands, create a virtual environment first.
```bash
pip freeze > requirements.txt
```

## cleanup
```bash
make clean
```

## Style Guide
We will try to follow the Google Python Style Guide https://google.github.io/styleguide/pyguide.html.
