from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    code: int = Field(default=200, description="状态码")
    message: str = Field(default="success", description="消息")
    data: Optional[T] = Field(default=None, description="数据")


class PageQuery(BaseModel):
    page: int = Field(default=1, description="页码")
    page_size: int = Field(default=10, description="每页数量")
    keyword: Optional[str] = Field(default=None, description="搜索关键词")


class PageResponse(BaseModel, Generic[T]):
    total: int = Field(default=0, description="总记录数")
    page: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=10, description="每页数量")
    list: List[T] = Field(default_factory=list, description="数据列表")
