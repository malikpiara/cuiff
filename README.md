# Cuiff

Daily standup meetings can be a pain in remote settings due to time zone differences. When people miss out, they can feel disconnected. On the other hand, Slack bot alternatives can make standups feel like a chore where people have to report what they are working on.

Cuiff provides teams with a long-form writing alternative to daily standups. The goal of this product is to improve autonomy and communication while boosting motivation by letting everyone see daily progress.

## Getting Started

**_Prerequisites: Python 3.9.0._**

```shell script
$ git clone https://github.com/malikpiara/cuiff.git

$ cd cuiff

$ python3 -m venv venv              # Create a virtual environment.

$ source venv/bin/activate          # Activate your virtual environment.

$ pip install -r requirements.txt   # Install project requirements.

$ export FLASK_APP=app.py

$ export FLASK_ENV=development      # Enable hot reloading, debug mode.

$ flask run
```

The app will only work locally when the debug is enabled due to [Flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman), which forces all connects to https.

The default content security policy is extremely strict and will prevent loading any resources that are not in the same domain as the application. [Here are some examples on how to change the default policy](https://github.com/GoogleCloudPlatform/flask-talisman#content-security-policy).

## Setting up the database

Create a `.env` file in the root directory of your project and connect the app to a MongoDB atlas cluster.
