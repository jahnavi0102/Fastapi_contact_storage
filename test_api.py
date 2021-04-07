from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import models

from db import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

#did testing on single user 
def test_create_user(db: Session = Depends(override_get_db)):
    

    #test on creating new user 
    response = client.post(
        "/users/",
        json={"email": "terry@example.com", "password": "chimichangas4life"},
    )
  
    assert response.status_code == 200, response.text
    user = response.json()
    assert user["email"] == "terry@example.com"
    assert "id" in user
    user_id = user["id"]

   

    #test on getting that user with the user id 
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200,response.text
    user = response.json()
    assert user["email"] == "terry@example.com"
    assert user["id"] == user_id
   
    #test on updating the user 
    response = client.put(f"/users/update/{user_id}", json = { "email": "captain@example.com", "password": "sadkasdhnotreallyhashed"})
    assert response.status_code == 200, response.text
    user = response.json()
    
    #test on deleting the user 
    response = client.delete(f"/users/delete/{user_id}")
    assert response.status_code == 200, response.text
    user = response.json()
    
#testing on single contact
def test_create_cont(db:Session = Depends(override_get_db)):

    #creating user to create contact list under it 
    response = client.post(
        "/users/",
        json={"email": "terry@example.com", "password": "chimichangas4life"},
    )
  
    assert response.status_code == 200, response.text
    user = response.json()
    assert user["email"] == "terry@example.com"
    assert "id" in user
    user_id = user["id"]
    
    #creating the contact
    response = client.post(
        f"/users/{user_id}/contacts/",
        json = {"name":"happy","email":"happy@gmail.com","phone":"0000000000"},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    contact_id = data["id"]
    email = data["email"]
    name = data["name"]
    phone = data["phone"]
    
    #testing the get  contact by email
    response = client.get(f"/contacts/email/{user_id}/{email}")
    assert response.status_code == 200, response.text
    assert data["name"] == "happy"
    assert data["email"] == "happy@gmail.com"
    assert data["phone"] == "0000000000"

    #testing the get  contact by name
    response = client.get(f"/contacts/name/{user_id}/{name}")
    assert response.status_code == 200, response.text
    assert data["name"] == "happy"
    assert data["email"] == "happy@gmail.com"
    assert data["phone"] == "0000000000"
   
    #testing the get  contact by phone
    response = client.get(f"/contacts/phone/{user_id}/{phone}")
    assert response.status_code == 200, response.text
    assert data["name"] == "happy"
    assert data["email"] == "happy@gmail.com"
    assert data["phone"] == "0000000000"

    #testing the  updating api for contact
    response = client.put(f"/contacts/update/{user_id}/{contact_id}" , json = {"name":"sad","email": "sad@gmail.com","phone":"1111111111" })
    assert response.status_code == 200, response.text
    data = response.json()
    
    #testing the deletion of the contact
    response = client.delete(f"/contacts/delete/{user_id}/{contact_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    
    #deleting the dummy user 
    response = client.delete(f"/users/delete/{user_id}")
    assert response.status_code == 200, response.text
    user = response.json()

    