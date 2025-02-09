from fastapi import FastAPI
import uvicorn

from plugin_server.user_routes import router as user_router
from plugin_server.body_shape_routes import router as body_shape_router
from plugin_server.facefusion_routes import router as facefusion_routes
from plugin_server.gallery_routes import router as gallery_routes
from plugin_server.clothes_routes import router as clothes_routes
from plugin_server.task_routes import router as task_routes

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 配置 CORSMiddleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # 允许访问的源
	allow_credentials=True,  # 支持 cookie
	allow_methods=["*"],  # 允许使用的请求方法
	allow_headers=["*"]  # 允许携带的 Headers
)

app.include_router(user_router, tags=['user'])
app.include_router(body_shape_router, tags=['user_detail'])
app.include_router(facefusion_routes, tags=['facefusion'])
app.include_router(gallery_routes, tags=['gallery'])
app.include_router(clothes_routes, tags=['clothes'])
app.include_router(task_routes, tags=['task'])


if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=8000)
