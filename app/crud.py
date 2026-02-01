from sqlalchemy.orm import Session
from . import models, auth

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_products_by_user(db: Session, user_id: int):
    return db.query(models.Product).filter(models.Product.user_id == user_id).all()


def create_user(db: Session, email: str, password: str):
    user = models.User(
        email=email,
        password=auth.hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_product(db: Session, name: str, price: float, user_id: int):
    product = models.Product(
        name=name,
        price=price,
        user_id=user_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_all_products(db: Session):
    return db.query(models.Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return product
