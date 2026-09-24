from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

def success_response(message: str = "success", data=None):
    content = {
        "code" : 200,
        "message" : message,
        "data" : data
    }

    return JSONResponse(content= jsonable_encoder(content))
# 使用jsonable_encoder可以转换各种格式，包括ORM，pydantic对象等

