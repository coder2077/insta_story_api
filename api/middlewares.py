from fastapi import Request
from starlette.responses import JSONResponse
from api.config import load_config


config = load_config() # load config from config.ini

class MyMiddleware:
	async def __call__(self, request: Request, call_next):
		# do something with the request object
		request_path = request.url.path
		if request_path in ['/', '/version', '/docs', '/openapi.json', '/redoc']:
			return await call_next(request)

		token = request.headers.get('secret-key')
		if token == config.key.secret:
			return JSONResponse(
				status_code=401,
				content={
					'error': True,
					'message': 'Unauthorized'
				}
			)
		response = await call_next(request)
		return response
