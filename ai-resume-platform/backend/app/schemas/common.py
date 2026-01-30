"""
通用响应模式
"""
from typing import Optional, Generic, TypeVar, List, Any
from pydantic import BaseModel

T = TypeVar('T')


class ResponseBase(BaseModel):
    """基础响应"""
    code: int = 200
    message: str = "success"
    
    
class Response(ResponseBase, Generic[T]):
    """通用响应"""
    data: Optional[T] = None


class PageResponse(ResponseBase, Generic[T]):
    """分页响应"""
    data: Optional[List[T]] = None
    total: int = 0
    page: int = 1
    page_size: int = 10
    
    @property
    def total_pages(self) -> int:
        if self.page_size <= 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size


class ErrorResponse(BaseModel):
    """错误响应"""
    code: int
    message: str
    detail: Optional[Any] = None
