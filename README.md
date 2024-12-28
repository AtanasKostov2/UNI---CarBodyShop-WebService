# UNI---CarBodyShop-WebService
Uni project for a web service app focused on the workflow and management of car garage shops

## To setup the project and populate the DB:
* Frontend: From the FE directory run
    ```serve .```
   
    Frontend is accessible at http://localhost:3000

* Backend: From the main directory run 

    1. ```python -m venv venv``` to create a local virtual environmnet
    
    2. ```venv\Scripts\activate``` to activate the virtual environmnet

    3. ```pip install -r requirements.txt``` to install the used libraries

    4. ```python models.py``` to setup the DB schemas

    5. ```python populate.py``` to add placeholder items into the DB

    6. ```python main.py``` to run the service

    
    Backend will listen for requests at http://127.0.0.1:8088
    
    Swagger docs available at: http://127.0.0.1:8088/docs
