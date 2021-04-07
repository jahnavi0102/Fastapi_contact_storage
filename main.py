from fastapi import Depends, FastAPI, HTTPException,status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List
import logging
import secrets
import crud, models, schemas
from db import SessionLocal, database
import json

models.Base.metadata.create_all(bind=database)

app = FastAPI(debug=True)

security = HTTPBasic()

    
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "morr")
    correct_password = secrets.compare_digest(credentials.password, "morr")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/users/me/")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}
    
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")  
    else:    
        return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
#limit for pagination 
def read_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users        


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/update/{owner_id}")
def update_user(
    *,
    db: Session = Depends(get_db),
    owner_id: int,
    item_in: schemas.UserCreate,
) ->any:
    """
    Update an item.

    """
    user = crud.get_user(db, user_id = owner_id)  
    if user:
        # can also use jsonable_encoder()
        user = {
            "email": item_in.email,
            "hashed_password": item_in.password
        }
        db.query(models.User).filter(models.User.id== owner_id).update(user, synchronize_session = "fetch")
        db.commit()
        return { "User Updated Successfully":True}
    else:
        raise HTTPException(status_code=404, detail = " User doesn't exist")   

@app.delete("/users/delete/{owner_id}")
def del_user(owner_id:int, db:Session = Depends(get_db)):
    user = crud.get_user(db, user_id = owner_id)
    if user:
       crud.del_user(db, user_id = owner_id)
       return "successfully deleted"
    else:
        raise HTTPException(status_code=404, detail = " User doesn't exist")                


@app.post("/users/{user_id}/contacts/", response_model=schemas.Contact)
def create_contact_for_user(
    user_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db)
):  
    user = crud.get_user(db, user_id = user_id)

    if user:  
         
        con = crud.get_contact_by_email(db, email = contact.email, owner_id = user_id)
        if con:
            raise HTTPException(status_code = 409, detail="User already exist")
        else:
            return crud.create_contact(db=db, contact=contact, user_id=user_id)
    else:
        raise HTTPException(status_code=404, detail = "Create User first , User doesn't exist")        


@app.get("/contacts/", response_model=List[schemas.Contact])
#limit for pagination 
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contacts = crud.get_contacts_all(db, skip=skip, limit=limit)
    return contacts 

@app.get("/users/{user_id}/contacts", response_model = List[schemas.Contact])
def read_contacts(user_id:int, db:Session = Depends(get_db)):
    user = crud.get_user(db, user_id = user_id)
    if user:
        contacts = crud.get_contacts_by_user(db, owner_id = user_id)   
        if contacts:
            return contacts
        else:
            raise HTTPException(status_code = 404, detail = "No contacts added ")
    else :
        raise HTTPException(status_code=404, detail = "Create User first , User doesn't exist")           

@app.get("/contacts/email/{owner_id}/{email}",response_model=schemas.Contact)
def read_contact_by_mail(owner_id:str, email:str, db:Session = Depends(get_db)):
    user = crud.get_user(db, user_id = owner_id)
    if user:
        contacts = crud.get_contact_by_email(db, email = email, owner_id= owner_id)
        if contacts is None:
           raise HTTPException(status_code=404, detail="Contact not found")
        else:
           return contacts
    else:
        raise HTTPException(status_code=404, detail = "Create User first , User doesn't exist")     
       
    


@app.get("/contacts/phone/{owner_id}/{phone}",response_model=schemas.Contact)
def read_contact_by_phone(owner_id:str, phone:str, db:Session = Depends(get_db)):
    user = crud.get_user(db, user_id = owner_id)
    if user:
        contacts = crud.get_contact_by_phone(db, phone = phone, owner_id= owner_id)
        if contacts is None:
           raise HTTPException(status_code=404, detail="Contact not found")
        else:
           return contacts
    else:
        raise HTTPException(status_code=404, detail = "Create User first , User doesn't exist")    

@app.get("/contacts/name/{owner_id}/{name}",response_model=schemas.Contact)
def read_contact_by_name(owner_id:str,name:str, db:Session = Depends(get_db)):
    user = crud.get_user(db, user_id = owner_id)
    if user:
        contacts = crud.get_contact_by_name(db, name = name, owner_id= owner_id)
        if contacts is None:
           raise HTTPException(status_code=404, detail="Contact not found")
        else:
           return contacts
    else:
        raise HTTPException(status_code=404, detail = "Create User first , User doesn't exist")            

    
@app.put("/contacts/update/{owner_id}/{contact_id}")
def update_contact(
    *,
    db: Session = Depends(get_db),
    contact_id: int,
    item_in: schemas.ContactBase,
    owner_id:int,
) ->any:
    """
    Update an item.

    """
    user = crud.get_user(db, user_id = owner_id)
    if user:
        contacts = crud.get_contact(db, owner_id= owner_id, contact_id=contact_id)
        if contacts:
            # can also use jsonable_encoder()
            contact = { 
                "name": item_in.name,
                "email": item_in.email,
                "phone": item_in.phone
            }
            db.query(models.Contact).filter(owner_id== owner_id, models.Contact.id==contact_id).update(contact, synchronize_session = "fetch")
            db.commit()
            return { "Contact Updated Successfully": True}
        else:
            raise HTTPException(status_code=404, detail="Contact not found")
    else:
        raise HTTPException(status_code=404, detail = " User doesn't exist")    


@app.delete("/contacts/delete/{owner_id}/{contact_id}")
def del_con(owner_id:int, contact_id:int, db:Session = Depends(get_db)):
    user = crud.get_user(db, user_id = owner_id)
    if user:
        contacts = crud.get_contact(db, owner_id= owner_id, contact_id=contact_id)
        if contacts is None:
           raise HTTPException(status_code=404, detail="Contact not found")
        else:
           crud.del_contact(db, owner_id = owner_id, contact_id = contact_id)
           return "successfully deleted"
    else:
        raise HTTPException(status_code=404, detail = " User doesn't exist")            






