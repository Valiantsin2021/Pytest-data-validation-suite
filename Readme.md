# Data Tests - Using Python 

## This repository purpose is to showcase the data testing using pytest library.

## What is Python and Pytest Framework 

`Python` is a high-level, general-purpose programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991. Python is designed to be easy to learn and has a clean and concise syntax, which makes it a popular choice for both beginners and experienced programmers.

The `pytest` framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.

### Test Descriptions

Test analytics records file to verify the following scenarios:

●	The total number of distinct stories that appear in the record file

●	Sometimes, the system is dropping some analytics for some stories. This is an error and we are interested in building a mechanism that, given a piece of real time record, will be able to spot missing analytics. Could you implement a method to spot these issues related to missing analytics based on the information of the fields provided above?

●	The RP_ENTITY_ID field follows a clear format pattern. How would you implement a method to validate that the data received on this field conforms to the expected format.

### The validation process:

● 	Verify that the RP_ENTITY_ID field follows the format: regexp matching [A-Z0-9]{6}
● 	Verify the anallytics records number of distinct stories: by counting the number of unique/distinct stories
● 	Verify the anallytics records has no dropped analytics: by counting the number of analytics records comparying the DOCUMENT_RECORD_INDEX index of the last record is equal to DOCUMENT_RECORD_COUNT for the RP_DOCUMENT_ID
● 	Verify the anallytics records has no missing analytics: by counting the number of analytics records that are missing for the RP_DOCUMENT_ID 

### Setup of dependencies for the tests 

#### To activate our environment, we use the command:
```bash
python -m venv venv
venv\Scripts\Activate
```
If everything is correct, your environment will be activated and on the cmd you will see like this:
```bash
(name_of_environment) C:\User\tests 
```
To disable your environment just run:
```bash
deactivate
```
To install the dependencies:

```bash
pip install -r requirements.txt
```
If you update the libraries version you can freeze update requirements
```bash
pip freeze > requirements.txt
```

#### Optionally we can use pipenv

```bash
pip install pipenv \
pipenv shell \
pipenv install -r requirements.txt
```
### Run tests with pytest

```bash
pytest
```
To specify the path to the test data (records file):

```bash
FILE_PATH=<path_to_file> pytest
```

### Run with Docker

Build the image first

```bash
docker build -t <imagename> .
```
Then run the tests in a container 

```bash
 docker run -it --rm --name <testname> -v ${pwd}:/app -w /app <imagename>
```
### To run specific test function

focused test
```bash
pytest ./tests/test_analytics.py -s -v -k test_get_analytics --html-report=./report/report.html
```

To generate the allure report after the test finished:

```bash
allure generate allure-results --clean -o allure-report && allure open allure-report
```
