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

To run these test please do so in a clean environment. To clean the environment just kill the server, and execute again 
both of the flask commands.
    
    flask reset-db
    flask run -h 127.0.0.1 -p 5000

# Closing

Developing this project I've needed to take some decisions to make easier the usage and developing.

* I've chosen flask as a framework because most of my experience is using it, and the project does use it. Also, 
I believe flask is better suited for small APIs rather than heavier frameworks such as Django.
* I've chosen sqlalchemy to simplify the code that deals with the Database. This choice has ended causing me a fair bit
of problems because I haven't worked with it in a long time, and the interfaces have changed quite a bit. In the end 
I've ended learning more as a result.
* I've chosen sqlite because of it's  more simple, and lightweight than other choices such as PSQL or MySQL. I've also 
learnt a bit about how sqlite works inside, particularly about how it deals with foreign keys. 
* I've also chosen to not use docker, even though it was my initial idea, because of a lack of time. Anyway, it should 
be pretty straightforward to dockerize. 
* Due to the design choices that made me keep most of the logic within the views in the controllers using a traditional 
approach to testing such as unittesting would make the process take a lot more of time than expected. As such I've opted 
to do API testing using postman. If I had a day more I would have chosen a proper framework such as Tavern Testing to do it.
But given the purpose of the project, postman will do. 
