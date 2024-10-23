from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, auth
from .database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register a new user
@app.post("/register", response_model=schemas.UserCreate)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login to get token
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Get list of blogs (no auth needed)
@app.get("/blogs", response_model=list[schemas.Blog])
def get_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()

# Create a new blog (protected route)
@app.post("/blogs", response_model=schemas.Blog)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    username = auth.verify_token(token)
    new_blog = models.Blog(**blog.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Get a single blog post by ID
@app.get("/blogs/{id}", response_model=schemas.Blog)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

# Update an existing blog (protected route)
@app.put("/blogs/{id}", response_model=schemas.Blog)
def update_blog(id: int, blog: schemas.BlogUpdate, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    username = auth.verify_token(token)
    db_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    for key, value in blog.dict(exclude_unset=True).items():
        setattr(db_blog, key, value)
    db.commit()
    db.refresh(db_blog)
    return db_blog

# Delete a blog (protected route)
@app.delete("/blogs/{id}", response_model=dict)
def delete_blog(id: int, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    username = auth.verify_token(token)
    db_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(db_blog)
    db.commit()
    return {"message": "Blog deleted"}

# Add comment to a blog post
@app.post("/blogs/{id}/comments", response_model=schemas.Comment)
def add_comment(id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    db_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    new_comment = models.Comment(**comment.dict(), blog_id=id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# Like a blog post (no auth needed)
@app.put("/blogs/{id}/like", response_model=schemas.Blog)
def like_blog(id: int, db: Session = Depends(get_db)):
    db_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    db_blog.likes += 1
    db.commit()
    db.refresh(db_blog)
    return db_blog
