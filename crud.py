from sqlalchemy.orm import Session
from sqlalchemy import delete

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_contact(db: Session, owner_id: int, contact_id:int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == owner_id ).first()    

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db:Session, email :str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_contact_by_email(db: Session, email: str, owner_id:str):
    return db.query(models.Contact).filter(models.Contact.email == email,models.Contact.owner_id == owner_id).first()

def get_contact_mail(db:Session, email:str):
    return db.query(models.Contact).filter(models.Contact.email == email).first()    

def get_contact_by_name(db: Session, name: str, owner_id:str):
    return db.query(models.Contact).filter(models.Contact.name == name,models.Contact.owner_id == owner_id).first()

def get_contact_by_phone(db:Session, phone: str,owner_id:str):
    return db.query(models.Contact).filter(models.Contact.phone == phone,models.Contact.owner_id == owner_id).first()        


def get_contacts_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()


def get_contacts_by_user(db: Session, owner_id = int):
    return db.query(models.Contact).filter(models.Contact.owner_id == owner_id).all()    

def del_user(db:Session, user_id:int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()

def del_contact(db:Session, contact_id:int, owner_id:int):
    db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == owner_id).delete()  
    db.commit()    

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_contact(db: Session, contact: schemas.ContactCreate, user_id: int):
    db_contact = models.Contact(**contact.dict(), owner_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact