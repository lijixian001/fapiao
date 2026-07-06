# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：schemas/common.py
# 模块用途：通用数据模式定义，提供统一的响应格式、分页查询等基础数据结构
# 说明：
#   - 使用Pydantic进行数据验证和序列化
#   - 定义统一的API响应格式，确保前后端交互规范
#   - 提供泛型支持，可复用性强
# ================================================================================

# 导入泛型相关工具：Generic用于定义泛型类，TypeVar用于类型变量
from typing import Generic, TypeVar, Optional, List
# 从Pydantic导入基础模型类和字段装饰器
from pydantic import BaseModel, Field

# 定义泛型类型变量T
# 用于ResponseModel和PageResponse的data/list元素类型
# 使这些类可以适配任意数据类型
T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    """
    统一响应模型（泛型）
    所有API接口的统一响应格式规范，确保前后端数据交互的一致性

    泛型参数:
        T: 响应数据的具体类型

    字段说明:
        code: 状态码，200表示成功，其他表示错误
        message: 响应消息，描述请求结果
        data: 响应数据，泛型类型，可为None

    使用示例:
        ResponseModel[UserResponse] - 返回用户数据的响应
        ResponseModel[List[InvoiceResponse]] - 返回发票列表的响应
    """
    # 状态码字段
    # 默认值200表示成功
    code: int = Field(default=200, description="状态码")
    # 响应消息字段
    # 默认值"success"表示成功
    message: str = Field(default="success", description="消息")
    # 响应数据字段
    # 使用Optional[T]表示可以为None
    # 泛型T使得data可以是任意类型
    data: Optional[T] = Field(default=None, description="数据")


class PageQuery(BaseModel):
    """
    分页查询参数模型
    用于接收前端分页查询的请求参数

    字段说明:
        page: 当前页码，默认第1页
        page_size: 每页数据条数，默认10条
        keyword: 搜索关键词，可选

    使用场景:
        列表查询接口的查询参数，支持分页和关键词搜索
    """
    # 页码字段
    # 默认第1页
    page: int = Field(default=1, description="页码")
    # 每页数量字段
    # 默认每页10条数据
    page_size: int = Field(default=10, description="每页数量")
    # 搜索关键词字段
    # 可选参数，用于模糊搜索
    keyword: Optional[str] = Field(default=None, description="搜索关键词")


class PageResponse(BaseModel, Generic[T]):
    """
    分页响应模型（泛型）
    分页查询的统一响应格式，包含总记录数和当前页数据

    泛型参数:
        T: 列表中每条数据的类型

    字段说明:
        total: 总记录数
        page: 当前页码
        page_size: 每页数量
        list: 当前页数据列表

    使用示例:
        PageResponse[UserResponse] - 用户分页数据
        PageResponse[InvoiceResponse] - 发票分页数据
    """
    # 总记录数字段
    # 符合查询条件的所有数据总数，用于计算总页数
    total: int = Field(default=0, description="总记录数")
    # 当前页码字段
    page: int = Field(default=1, description="当前页码")
    # 每页数量字段
    page_size: int = Field(default=10, description="每页数量")
    # 数据列表字段
    # 使用List[T]表示元素类型为泛型T的列表
    # default_factory=list表示默认值为空列表
    list: List[T] = Field(default_factory=list, description="数据列表")
