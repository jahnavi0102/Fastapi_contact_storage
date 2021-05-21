#  Project 

## Technology used:
    FastAPI for backend framework 
    SQLAlchemy for connecting database with the app (FastApi framework)
    PostgreSQL used as the db for storing more than scalable data (more than 10000)
    Pytest for testing 

## In order to run the server :
    Open the project dir inside it . 
    Activate the env (virtual enviroment )
    Install the dependencies via requirements.txt file (pip install ...)    
    Run the command under the env : uvicorn main:app --reload
    Open the loacalhost on the browser :  http://127.0.0.1:8000
    Add /docs at the end of the route : http://127.0.0.1:8000/docs

    Try all the api.

    In order to run test , open the dir under env  in the new terminal and send command : pytest 


## Made 6 files . 

1. main.py for api , fetching data ( for crud properties )

2. crud.py for writing fucntions of crud in improvised manner 

3. models.py for creating database models in the db so that the main.py can fetch data from db instad of dummy data 

4. schemas.py for getting the response in serialize order after fetching 

5. db.py for connecting the app with the postgresql server , and getting the base model 

6. test_api.py for writing integrated test on crud api of user and contact (testing is done under another db ie: test_db)




