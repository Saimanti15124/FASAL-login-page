from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated

app = FastAPI()
# Setup templates
templates = Jinja2Templates(directory="templates")

# Mock user database (in a real app, use a proper database)
users_db = {
    "admin": "password123",
    "user1": "mypassword"
}

# Login route - displays the form
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Process login form
@app.post("/login")
async def handle_login(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    # Check credentials (in a real app, use proper password hashing)
    if username in users_db and users_db[username] == password:
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
