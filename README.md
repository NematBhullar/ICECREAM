# Icecream E-Invoicing

1. About 
2. Getting Started 

## 1. About
An invoice sending application through the Software as a Service (SaaS) model, which assists users in sending eco-friendly, fast, reliable and affordable e-invoices to their customers. The service accepts input and creates an invoice in a usable UBL format, with a visual confirmation supporting the transfer.

Website: https://seng2021-app-d4e5c.web.app/

## 2. Getting Started

### Coverage report
https://codecov.io/gh/SENG2021-22T1/ICECREAM

### File Structure
`src` is where we store the code. The entry point is `application.py`, which is not in `src`. This is because `Elastic Beanstalk` finds the file named `appliaction.py` in the `root` directory by default. `db_model` is a directory that stores the model of the database entity.

`routes.py` is where flask dispatches the apis. `auth.py` is in charge of authentication and athourization. `db.py` are functions that are related to the database. `email.py` is in charge of the functionality to send the invoice via email. `config.py` is storing the configurations.

`test` is where we store our tests. Integration tests are stored in `system_test` and unit tests are stored in `unit_test`.

### Create a Virtual Environment
```bash
pip install virtualenv
virtualenv virt
source virt/bin/activate
```

### Exit Virtual Environment
```bash
deactivate
```

### Install Dependencies
```bash
pip install -r requirements.txt
pip install pylint
pip install coverage
```

### Create Database
After downloading postgres, and starting postgresql.
```bash
createdb seng2021_db
python3 create_db.py
```

### Linting
```bash
find . -type f -name "*.py" | xargs pylint
```

### Test
```bash
python3 application.py &
coverage run -m pytest test/ --junitxml=pytest_report.xml
coverage report
coverage html
```

### Create Requirements
Before running the following commands, create a virtual environment first.
```bash
pip freeze > requirements.txt
```

### Clean Up
```bash
make clean
```

### Style Guide
We will try to follow the Google Python Style Guide https://google.github.io/styleguide/pyguide.html.
