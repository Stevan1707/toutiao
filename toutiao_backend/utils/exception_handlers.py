# 封装异常类，直接在main.py里注册即可处理绝大部分异常
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, general_exception_handler

def register_exception_handlers(app):
    """注册异常处理类
    子类在前，父类在后，具体在前，抽象在后
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)