from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Database setup
DATABASE_URL = "postgresql://username:password@localhost/mydatabase"  # Update with your credentials
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User model
class User(Base):
    _tablename_ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Login route - displays the form
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Process login form
@app.post("/login")
async def handle_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if user and pwd_context.verify(password, user.password):
        # Successful login - redirect to a dashboard or home page
        return RedirectResponse(url="/welcome", status_code=303)
    else:
        # Failed login - show error
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"},
            status_code=401
        )

# Welcome page after successful login
@app.get("/welcome", response_class=HTMLResponse)
async def welcome_page(request: Request):
    return """
    <html>
        <head>
            <title>Welcome</title>
        </head>
        <body>
            <h1>Login Successful!</h1>
            <p>Welcome to your account.</p>
        </body>
    </html>
    """

if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
