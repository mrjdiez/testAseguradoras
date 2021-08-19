# Installation

The installation for this project is quite simple, but it's a python project, so it's required to have python installed

If you don't have it installed, please download it from your preferred package manager, or from https://www.python.org

After that, clone this repository using git:

    git clone git@github.com:mrjdiez/testAseguradoras.git
    cd testAseguradoras

Once done create a new virtualenv and install the requirements.
    
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt


# Running the Server

Once you've installed the requirements then you'll want to run the server. 
To do that, just define the FLASK_APP variable and execute the following commands

    export FLASK_APP=app.py
    flask reset-db
    flask run -h 127.0.0.1 -p 5000

# Postman

If you want to test the API or check the existing endpoint you can use the two Postman collections exported 
within the postman directory. If your server is running in a different interface or port please, remember to update
the environment variables within the collections.

1. API: Contains the definition of the different endpoints, including the health-check. Feel free to modify whatever parameter.
2. TestCollection: Contains a series of requests with tests integrated to test the most basic of uses. 
You can run these tests importing this collection and creating a runner using this collection.
You can read more about runners [here]([https://learning.postman.com/docs/running-collections/intro-to-collection-runs/)