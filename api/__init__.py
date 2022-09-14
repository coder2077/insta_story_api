from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from api.middlewares import MyMiddleware
from api.config import load_config, VERSION
from api.routes import router



config = load_config() # load config from config.ini
app = FastAPI(title="Instagram Story API", description="", version=VERSION) # create app

my_middleware = MyMiddleware() # create middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=my_middleware) # add middleware to app


# Register the routes
app.include_router(router, prefix="/api")



@app.get("/")
async def welcome():
    """ Welcome message """
    json_response = {
        "error": False, 
        "response": "Welcome to the Instagram Story API!", 
        "version": VERSION, 
        "author": "@coder2077"
    }
    return json_response


@app.get("/version")
async def version():
    """ Returns the version of the application """
    json_response = {
        "error": False, 
        "response": {'version': VERSION}, 
        "author": "@coder2077"
    }
    return json_response

