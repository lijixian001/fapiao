"""
发票管理相关API路由模块

本模块提供发票管理相关的接口，包括发票列表查询、发票详情获取、
发票创建、发票更新、发票删除、发票归档/取消归档、发票审核等功能。
所有接口都需要登录认证。
"""

# 导入FastAPI框架相关组件：APIRouter用于创建路由，Depends用于依赖注入，
# Query用于查询参数解析和验证
from fastapi import APIRouter, Depends, Query
# 导入SQLAlchemy的Session类，用于数据库会话管理
from sqlalchemy.orm import Session
# 导入typing模块的Optional和List类型，用于表示可选参数和列表类型
from typing import Optional, List

# 导入数据库会话获取函数，用于依赖注入获取数据库连接
from core.database import get_db
# 导入当前用户获取函数，用于依赖注入获取当前登录用户信息
from core.auth import get_current_user
# 导入发票相关的Pydantic数据模型：创建模型、更新模型、响应模型、详情响应模型、明细项响应模型
from schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceResponse, InvoiceDetailResponse, InvoiceItemResponse
# 导入通用响应模型，包括统一响应格式和分页响应格式
from schemas.common import ResponseModel, PageResponse
# 导入发票服务类，封装了发票管理相关的业务逻辑
from services.invoice_service import InvoiceService

# 创建发票管理路由实例，前缀为/api/invoice，在API文档中归类为"发票管理"标签
router = APIRouter(prefix="/api/invoice", tags=["发票管理"])


@router.get("", response_model=ResponseModel[PageResponse[InvoiceResponse]])
def list_invoices(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    invoice_status: Optional[int] = Query(None, description="发票状态"),
    invoice_type: Optional[int] = Query(None, description="发票类型"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取发票列表接口

    分页查询发票列表，支持按关键词、发票状态、发票类型筛选。

    请求方式: GET
    请求路径: /api/invoice

    参数:
        page (int): 页码，默认为1
        page_size (int): 每页数量，默认为10
        keyword (Optional[str]): 搜索关键词，可选，用于模糊匹配发票号、客户名称等
        invoice_status (Optional[int]): 发票状态筛选，可选
        invoice_type (Optional[int]): 发票类型筛选，可选
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取

    返回值:
        ResponseModel[PageResponse[InvoiceResponse]]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 分页数据
                - total: 总记录数
                - page: 当前页码
                - page_size: 每页数量
                - items: 发票列表

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用发票服务获取分页发票列表，支持多种筛选条件
    result = InvoiceService.list_invoices(
        db, page=page, page_size=page_size,
        keyword=keyword, invoice_status=invoice_status,
        invoice_type=invoice_type
    )
    # 返回统一格式的成功响应
    return ResponseModel(data=result)


@router.get("/{invoice_id}", response_model=ResponseModel[InvoiceDetailResponse])
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取发票详情接口

    根据发票ID获取发票的详细信息，包括发票基本信息和明细项列表。

    请求方式: GET
    请求路径: /api/invoice/{invoice_id}

    参数:
        invoice_id (int): 发票ID，路径参数
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取

    返回值:
        ResponseModel[InvoiceDetailResponse]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 发票详细信息（发票不存在时为None）
                - 发票基本信息
                - items: 发票明细项列表

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用发票服务根据ID获取发票基本信息
    invoice = InvoiceService.get_invoice_by_id(db, invoice_id)
    # 判断发票是否存在，不存在则返回404错误
    if not invoice:
        return ResponseModel(code=404, message="发票不存在", data=None)
    # 获取发票明细项列表
    items = InvoiceService.get_invoice_items(db, invoice_id)
    # 将发票基本信息转换为详情响应模型
    result = InvoiceDetailResponse.model_validate(invoice)
    # 将明细项列表添加到详情响应中
    result.items = items
    # 返回发票详情响应
    return ResponseModel(data=result)


@router.post("", response_model=ResponseModel[InvoiceResponse])
def create_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    创建发票接口

    创建一张新的发票，包括发票基本信息和明细项。

    请求方式: POST
    请求路径: /api/invoice

    参数:
        invoice_data (InvoiceCreate): 发票创建请求体，包含发票信息
            - 发票基本信息字段
            - items: 发票明细项列表
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取
            - user_id: 创建人用户ID

    返回值:
        ResponseModel[InvoiceResponse]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 新创建的发票信息

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用发票服务创建新发票，传入当前用户ID作为创建人
    invoice = InvoiceService.create_invoice(db, invoice_data, created_by=current_user["user_id"])
    # 返回创建成功的响应
    return ResponseModel(data=invoice, message="创建成功")


@router.put("/{invoice_id}", response_model=ResponseModel[InvoiceResponse])
def update_invoice(
    invoice_id: int,
    invoice_data: InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    更新发票信息接口

    根据发票ID更新发票的信息。

    请求方式: PUT
    请求路径: /api/invoice/{invoice_id}

    参数:
        invoice_id (int): 发票ID，路径参数
        invoice_data (InvoiceUpdate): 发票更新请求体，包含要更新的字段
            - 可选的发票属性字段
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取

    返回值:
        ResponseModel[InvoiceResponse]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 更新后的发票信息

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用发票服务更新发票信息
    invoice = InvoiceService.update_invoice(db, invoice_id, invoice_data)
    # 返回更新成功的响应
    return ResponseModel(data=invoice, message="更新成功")


@router.delete("/{invoice_id}", response_model=ResponseModel)
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    删除发票接口

    根据发票ID删除指定发票。

    请求方式: DELETE
    请求路径: /api/invoice/{invoice_id}

    参数:
        invoice_id (int): 发票ID，路径参数
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取

    返回值:
        ResponseModel: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用发票服务删除发票
    InvoiceService.delete_invoice(db, invoice_id)
    # 返回删除成功的响应
    return ResponseModel(message="删除成功")


@router.post("/{invoice_id}/archive", response_model=ResponseModel[InvoiceResponse])
def archive_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    归档发票接口

    将指定发票标记为已归档状态。

    请求方式: POST
    请求路径: /api/invoice/{invoice_id}/archive

    参数:
        invoice_id (int): 发票ID，路径参数
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取

    返回值:
        ResponseModel[InvoiceResponse]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 归档后的发票信息

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用发票服务将发票归档
    invoice = InvoiceService.archive_invoice(db, invoice_id)
    # 返回归档成功的响应
    return ResponseModel(data=invoice, message="归档成功")


@router.post("/archive/unarchive", response_model=ResponseModel[InvoiceResponse])
def unarchive_invoice(
    invoice_id: int = Query(..., description="发票ID"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    取消归档发票接口

    将已归档的发票取消归档，恢复为正常状态。

    请求方式: POST
    请求路径: /api/invoice/archive/unarchive

    参数:
        invoice_id (int): 发票ID，查询参数，必填
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取

    返回值:
        ResponseModel[InvoiceResponse]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 取消归档后的发票信息

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用发票服务取消发票归档
    invoice = InvoiceService.unarchive_invoice(db, invoice_id)
    # 返回取消归档成功的响应
    return ResponseModel(data=invoice, message="取消归档成功")


@router.post("/{invoice_id}/verify", response_model=ResponseModel[InvoiceResponse])
def verify_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    审核发票接口

    对指定发票进行审核操作，将发票状态标记为已审核。

    请求方式: POST
    请求路径: /api/invoice/{invoice_id}/verify

    参数:
        invoice_id (int): 发票ID，路径参数
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取

    返回值:
        ResponseModel[InvoiceResponse]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 审核后的发票信息

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用发票服务审核发票
    invoice = InvoiceService.verify_invoice(db, invoice_id)
    # 返回审核成功的响应
    return ResponseModel(data=invoice, message="审核成功")
