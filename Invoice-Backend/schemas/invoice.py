"""
项目名称：Invoice-Backend（发票管理系统后端）
模块名称：invoice.py
模块用途：定义发票相关的Pydantic数据模型（Schema）
模块说明：本文件包含发票明细、发票创建、发票更新、发票响应和发票详情响应等数据模型，
         用于API请求参数验证和响应数据格式化。
"""

# 导入Optional和List类型，用于声明可选字段和列表类型字段
from typing import Optional, List
# 导入date和datetime类型，用于处理日期和日期时间字段
from datetime import date, datetime
# 导入Pydantic的BaseModel基类和Field字段验证器
# BaseModel：所有Pydantic模型的基类，提供数据验证、序列化等功能
# Field：用于定义字段的额外验证规则和描述信息
from pydantic import BaseModel, Field


class InvoiceItemCreate(BaseModel):
    """
    发票明细创建数据模型

    用途：用于创建发票明细项时的请求参数验证
    字段说明：
        - item_name: 商品名称（必填）
        - specification: 规格型号（可选）
        - unit: 单位（可选）
        - quantity: 数量（默认1）
        - unit_price: 单价（默认0）
        - amount: 金额（默认0）
        - tax_rate: 税率（默认0）
        - tax_amount: 税额（默认0）
    使用场景：创建发票时，通过此模型验证发票明细项的数据
    """
    item_name: str = Field(..., description="商品名称")           # 商品名称，必填字段
    specification: Optional[str] = Field(default=None, description="规格型号")  # 规格型号，可选
    unit: Optional[str] = Field(default=None, description="单位") # 计量单位，可选（如：个、件、台等）
    quantity: int = Field(default=1, description="数量")          # 数量，默认为1
    unit_price: float = Field(default=0, description="单价")      # 单价，默认为0
    amount: float = Field(default=0, description="金额")          # 金额（数量×单价），默认为0
    tax_rate: float = Field(default=0, description="税率")        # 税率，默认为0（如：0.13表示13%）
    tax_amount: float = Field(default=0, description="税额")      # 税额（金额×税率），默认为0


class InvoiceItemResponse(BaseModel):
    """
    发票明细响应数据模型

    用途：用于发票明细查询接口的响应数据格式化
    字段说明：
        - id: 明细ID
        - invoice_id: 发票ID
        - item_name: 商品名称
        - specification: 规格型号（可选）
        - unit: 单位（可选）
        - quantity: 数量
        - unit_price: 单价
        - amount: 金额
        - tax_rate: 税率
        - tax_amount: 税额
        - created_at: 创建时间
        - updated_at: 更新时间
    使用场景：返回发票明细信息给前端时，通过此模型进行数据序列化
    """
    id: int                             # 发票明细唯一标识ID
    invoice_id: int                     # 所属发票ID
    item_name: str                      # 商品名称
    specification: Optional[str] = None # 规格型号，可选
    unit: Optional[str] = None          # 计量单位，可选
    quantity: int                       # 数量
    unit_price: float                   # 单价
    amount: float                       # 金额
    tax_rate: float                     # 税率
    tax_amount: float                   # 税额
    created_at: datetime                # 创建时间
    updated_at: datetime                # 最后更新时间

    class Config:
        """Pydantic模型配置类"""
        # 启用ORM模式，允许从ORM对象（如SQLAlchemy模型实例）直接创建Pydantic模型
        from_attributes = True


class InvoiceCreate(BaseModel):
    """
    发票创建数据模型

    用途：用于创建新发票时的请求参数验证
    字段说明：
        - invoice_code: 发票代码（可选）
        - invoice_number: 发票号码（必填）
        - invoice_date: 开票日期（可选）
        - invoice_type: 发票类型（默认1）
        - seller_name: 销方名称（可选）
        - seller_tax_no: 销方税号（可选）
        - buyer_name: 购方名称（可选）
        - buyer_tax_no: 购方税号（可选）
        - total_amount: 合计金额（默认0）
        - total_tax: 合计税额（默认0）
        - total_price_tax: 价税合计（默认0）
        - check_code: 校验码（可选）
        - remark: 备注（可选）
        - items: 发票明细列表（默认为空列表）
    使用场景：用户录入或导入发票时，通过此模型验证发票信息
    """
    invoice_code: Optional[str] = Field(default=None, description="发票代码")        # 发票代码，可选
    invoice_number: str = Field(..., description="发票号码")                         # 发票号码，必填字段
    invoice_date: Optional[date] = Field(default=None, description="开票日期")       # 开票日期，可选
    invoice_type: int = Field(default=1, description="发票类型")                     # 发票类型，默认为1（如：1=增值税专用发票，2=增值税普通发票等）
    seller_name: Optional[str] = Field(default=None, description="销方名称")         # 销售方名称，可选
    seller_tax_no: Optional[str] = Field(default=None, description="销方税号")       # 销售方纳税人识别号，可选
    buyer_name: Optional[str] = Field(default=None, description="购方名称")          # 购买方名称，可选
    buyer_tax_no: Optional[str] = Field(default=None, description="购方税号")        # 购买方纳税人识别号，可选
    total_amount: float = Field(default=0, description="合计金额")                   # 合计金额（不含税），默认为0
    total_tax: float = Field(default=0, description="合计税额")                      # 合计税额，默认为0
    total_price_tax: float = Field(default=0, description="价税合计")                # 价税合计（总金额+总税额），默认为0
    check_code: Optional[str] = Field(default=None, description="校验码")            # 发票校验码，可选
    remark: Optional[str] = Field(default=None, description="备注")                  # 备注信息，可选
    items: List[InvoiceItemCreate] = Field(default_factory=list, description="发票明细")  # 发票明细项列表，默认为空列表


class InvoiceUpdate(BaseModel):
    """
    发票更新数据模型

    用途：用于更新发票信息时的请求参数验证
    字段说明：
        - invoice_code: 发票代码（可选）
        - invoice_number: 发票号码（可选）
        - invoice_date: 开票日期（可选）
        - invoice_type: 发票类型（可选）
        - invoice_status: 发票状态（可选）
        - seller_name: 销方名称（可选）
        - seller_tax_no: 销方税号（可选）
        - buyer_name: 购方名称（可选）
        - buyer_tax_no: 购方税号（可选）
        - total_amount: 合计金额（可选）
        - total_tax: 合计税额（可选）
        - total_price_tax: 价税合计（可选）
        - check_code: 校验码（可选）
        - remark: 备注（可选）
        - deduct_status: 抵扣状态（可选）
        - deduct_date: 抵扣日期（可选）
        - archive_location: 归档位置（可选）
    使用场景：用户修改发票信息时，通过此模型验证需要更新的字段
    说明：所有字段均为可选，只更新传入的字段值
    """
    invoice_code: Optional[str] = None       # 发票代码，可选
    invoice_number: Optional[str] = None     # 发票号码，可选
    invoice_date: Optional[date] = None      # 开票日期，可选
    invoice_type: Optional[int] = None       # 发票类型，可选
    invoice_status: Optional[int] = None     # 发票状态，可选（如：1=正常，2=作废等）
    seller_name: Optional[str] = None        # 销售方名称，可选
    seller_tax_no: Optional[str] = None      # 销售方纳税人识别号，可选
    buyer_name: Optional[str] = None         # 购买方名称，可选
    buyer_tax_no: Optional[str] = None       # 购买方纳税人识别号，可选
    total_amount: Optional[float] = None     # 合计金额（不含税），可选
    total_tax: Optional[float] = None        # 合计税额，可选
    total_price_tax: Optional[float] = None  # 价税合计，可选
    check_code: Optional[str] = None         # 发票校验码，可选
    remark: Optional[str] = None             # 备注信息，可选
    deduct_status: Optional[int] = None      # 抵扣状态，可选（如：0=未抵扣，1=已抵扣）
    deduct_date: Optional[date] = None       # 抵扣日期，可选
    archive_location: Optional[str] = None   # 归档位置，可选


class InvoiceResponse(BaseModel):
    """
    发票响应数据模型

    用途：用于发票列表查询接口的响应数据格式化
    字段说明：
        - id: 发票ID
        - invoice_code: 发票代码（可选）
        - invoice_number: 发票号码
        - invoice_date: 开票日期（可选）
        - invoice_type: 发票类型
        - invoice_status: 发票状态
        - seller_name: 销方名称（可选）
        - seller_tax_no: 销方税号（可选）
        - buyer_name: 购方名称（可选）
        - buyer_tax_no: 购方税号（可选）
        - total_amount: 合计金额
        - total_tax: 合计税额
        - total_price_tax: 价税合计
        - check_code: 校验码（可选）
        - remark: 备注（可选）
        - deduct_status: 抵扣状态
        - deduct_date: 抵扣日期（可选）
        - archive_location: 归档位置（可选）
        - created_by: 创建人ID（可选）
        - created_at: 创建时间
        - updated_at: 更新时间
    使用场景：返回发票列表信息给前端时，通过此模型进行数据序列化
    """
    id: int                                  # 发票唯一标识ID
    invoice_code: Optional[str] = None       # 发票代码，可选
    invoice_number: str                      # 发票号码
    invoice_date: Optional[date] = None      # 开票日期，可选
    invoice_type: int                        # 发票类型
    invoice_status: int                      # 发票状态（如：1=正常，2=作废等）
    seller_name: Optional[str] = None        # 销售方名称，可选
    seller_tax_no: Optional[str] = None      # 销售方纳税人识别号，可选
    buyer_name: Optional[str] = None         # 购买方名称，可选
    buyer_tax_no: Optional[str] = None       # 购买方纳税人识别号，可选
    total_amount: float                      # 合计金额（不含税）
    total_tax: float                         # 合计税额
    total_price_tax: float                   # 价税合计
    check_code: Optional[str] = None         # 发票校验码，可选
    remark: Optional[str] = None             # 备注信息，可选
    deduct_status: int                       # 抵扣状态（如：0=未抵扣，1=已抵扣）
    deduct_date: Optional[date] = None       # 抵扣日期，可选
    archive_location: Optional[str] = None   # 归档位置，可选
    created_by: Optional[int] = None         # 创建人用户ID，可选
    created_at: datetime                     # 创建时间
    updated_at: datetime                     # 最后更新时间

    class Config:
        """Pydantic模型配置类"""
        # 启用ORM模式，允许从ORM对象（如SQLAlchemy模型实例）直接创建Pydantic模型
        from_attributes = True


class InvoiceDetailResponse(InvoiceResponse):
    """
    发票详情响应数据模型

    用途：用于发票详情查询接口的响应数据格式化
    字段说明：
        - 继承InvoiceResponse的所有字段
        - items: 发票明细列表（默认为空列表）
    使用场景：返回单张发票的详细信息（包含明细）给前端时，通过此模型进行数据序列化
    说明：继承自InvoiceResponse，在其基础上增加了发票明细列表字段
    """
    items: List[InvoiceItemResponse] = Field(default_factory=list, description="发票明细")  # 发票明细项列表，默认为空列表
