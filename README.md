# COMPSCI 235 - Repository for the CS235 Recipe Portal Assignment 1 Submission
This is the repository for the recipes webapp project of CompSci 235 in Semester 2, 2025.
Made by the best team known to computer science: Emil, Arun and Rowan!

## Description

This repository contains the completed code for the implementation of Assignment 1. The domain model has been expanded to include all necessary tasks, and a Flask app is co figured to display the pages of our recipe website, with HTML rendered with Jinja. Tests have been written for both unit testing and integration testing.

## Installation

**Installation via requirements.txt**

**Windows**
```shell
$ cd <project directory>
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

**MacOS**
```shell
$ cd <project directory>
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File or PyCharm'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add Interpreter'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *project directory*, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Testing

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right-clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call 'python -m pytest tests' to run all the tests. PyCharm also provides a built-in terminal, which uses the configured virtual environment. 

## Configuration

The *project directory/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.
 
## Data sources

The data files are modified excerpts downloaded from:

https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews/


## Health Star Rating
Nutritional values are scaled according to FDA recommended daily intakes.

'Protein' and 'Fiber' are considered positive impacts.
'Calories', 'Sugar', 'Sodium' and 'Saturated Fat' are considered negative impacts.

Proportional values for negative and positive impacts have their weighted average calculated (with weights based on WHO advice for relative impacts).
Negative and positive impacts have their total weighted average calculated (with weights based on the proportion on negative/positively affecting data available).

Raw score is inputted to a sigmoid function to scale between 1 and 5, and then rounded to the nearest 0.5.




