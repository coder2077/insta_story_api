from uuid import uuid4

from fastapi import APIRouter, Header
from fastapi import APIRouter, Depends, File, UploadFile

from insta_library import InstagramAPI
from instagrapi.types import StoryLink



# Create the router
router = APIRouter(tags=["API endpoints"])
api = InstagramAPI()


@router.get("/login")
def login(
	username: str, password: str, verification_code: str = '', 
	secret_key: str | None = Header(default=None)
):
	""" User login endpoint """
	json_response = api.login(username=username, password=password, verification_code=verification_code)
	return json_response


@router.get("/login/by/sessionid")
def login_by_sessionid(
	sessionid: str, secret_key: str | None = Header(default=None)
):
	""" User login by sessionid endpoint """
	json_response = api.login_by_sessionid(sessionid=sessionid)
	return json_response


@router.get("/login/pass_sms_code")
def pass_sms_code(
	username: str, sms_code: str, secret_key: str | None = Header(default=None)
):
	""" User login 2fa pass code """
	json_response = api.pass_sms_code(username=username, sms_code=sms_code)
	return json_response


@router.get("/set/proxy")
def set_proxy(
	dsn: str = '', secret_key: str | None = Header(default=None)
):
	""" Set proxy for client """
	json_response = api.set_proxy(dsn=dsn)
	return json_response


@router.get("/get/sessionid")
def get_sessionid(
	secret_key: str | None = Header(default=None)
):
	""" Get sessionid """
	json_response = api.get_sessionid()
	return json_response


@router.post("/upload_photo_story")
async def upload_photo_story(
	photo: UploadFile = File(...), 
	link: StoryLink = Depends(), 
	secret_key: str | None = Header(default=None)
):
	""" Upload photo story """
	file_name = f'media/{uuid4()}.jpg'
	with open(file_name, 'wb') as f:
		f.write(photo.file.read())
	json_response = api.upload_photo_story(file_name=file_name, link_class=link)
	return json_response


@router.post("/upload_video_story")
async def upload_video_story(
	photo: UploadFile = File(...), 
	link: StoryLink = Depends(), 
	secret_key: str | None = Header(default=None)
):
	""" Upload video story """
	file_name = f'media/{uuid4()}.mp4'
	with open(file_name, 'wb') as f:
		f.write(photo.file.read())
	json_response = api.upload_photo_story(file_name=file_name, link_class=link)
	return json_response
