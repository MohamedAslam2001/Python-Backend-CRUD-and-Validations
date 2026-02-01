from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import engine
from . import models, schemas, crud, auth, deps


# ---------------- LIFESPAN (DEV DB RESET) ----------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⚠️ DEV MODE: Dropping & creating DB tables")

    # DROP ALL TABLES
    models.Base.metadata.drop_all(bind=engine)

    # CREATE ALL TABLES
    models.Base.metadata.create_all(bind=engine)

    print("✅ DB reset complete")
    yield
    # shutdown (nothing to clean)


# ---------------- APP INIT ----------------
app = FastAPI(
    title="Backend Test (DEV)",
    lifespan=lifespan
)


# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- HEALTH CHECK ----------------
@app.get("/")
def root():
    return {"status": "Backend is running (DEV reset enabled)"}


# ---------------- AUTH ----------------
@app.post("/register")
def register(
    user: schemas.UserCreate,
    db: Session = Depends(deps.get_db)
):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    crud.create_user(db, user.email, user.password)
    return {"message": "User registered successfully"}


@app.post("/login", response_model=schemas.Token)
def login(
    user: schemas.UserLogin,
    db: Session = Depends(deps.get_db)
):
    db_user = crud.get_user_by_email(db, user.email)

    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token({"sub": db_user.email})
    return {"access_token": token}


# ---------------- PRODUCTS ----------------
@app.post("/products", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    return crud.create_product(
        db=db,
        name=product.name,
        price=product.price,
        user_id=current_user.id
    )


@app.get("/products", response_model=list[schemas.ProductResponse])
def get_products(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    return crud.get_products_by_user(db, current_user.id)


@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    product = crud.get_product_by_id(db, product_id)

    if not product or product.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    product = crud.get_product_by_id(db, product_id)

    if not product or product.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Product not found")

    crud.delete_product(db, product_id)
    return {"message": "Product deleted"}
