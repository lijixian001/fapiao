# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：models/invoice_main.py
# 模块用途：发票主表模型
# ================================================================================

from sqlalchemy import Column, String, Integer, DECIMAL, Date, Text
from models.base import BaseModel

# 发票类型
INVOICE_TYPE_SPECIAL = 1
INVOICE_TYPE_NORMAL = 2
INVOICE_TYPE_ELECTRONIC_SPECIAL = 3
INVOICE_TYPE_ELECTRONIC_NORMAL = 4

# 发票状态
INVOICE_STATUS_PENDING = 0
INVOICE_STATUS_VERIFIED = 1
INVOICE_STATUS_CANCELLED = 2
INVOICE_STATUS_RED = 3
INVOICE_STATUS_ARCHIVED = 4
INVOICE_STATUS_DEDUCTED = 5

# 抵扣状态
DEDUCT_STATUS_NO = 0
DEDUCT_STATUS_YES = 1


class InvoiceMain(BaseModel):
    __tablename__ = "invoice_main"

    invoice_code = Column(
        String(20),
        nullable=True,
        comment="发票代码"
    )

    invoice_number = Column(
        String(20),
        nullable=False,
        comment="发票号码"
    )

    invoice_date = Column(
        Date,
        nullable=True,
        comment="开票日期"
    )

    invoice_type = Column(
        Integer,
        default=INVOICE_TYPE_SPECIAL,
        nullable=False,
        comment="发票类型"
    )

    invoice_status = Column(
        Integer,
        default=INVOICE_STATUS_PENDING,
        nullable=False,
        comment="发票状态"
    )

    seller_name = Column(
        String(200),
        nullable=True,
        comment="销方名称"
    )

    seller_tax_no = Column(
        String(50),
        nullable=True,
        comment="销方税号"
    )

    buyer_name = Column(
        String(200),
        nullable=True,
        comment="购方名称"
    )

    buyer_tax_no = Column(
        String(50),
        nullable=True,
        comment="购方税号"
    )

    total_amount = Column(
        DECIMAL(18, 2),
        default=0,
        nullable=False,
        comment="合计金额"
    )

    total_tax = Column(
        DECIMAL(18, 2),
        default=0,
        nullable=False,
        comment="合计税额"
    )

    total_price_tax = Column(
        DECIMAL(18, 2),
        default=0,
        nullable=False,
        comment="价税合计"
    )

    check_code = Column(
        String(20),
        nullable=True,
        comment="校验码"
    )

    remark = Column(
        String(500),
        nullable=True,
        comment="备注"
    )

    deduct_status = Column(
        Integer,
        default=DEDUCT_STATUS_NO,
        nullable=False,
        comment="抵扣状态"
    )

    deduct_date = Column(
        Date,
        nullable=True,
        comment="抵扣日期"
    )

    archive_location = Column(
        String(200),
        nullable=True,
        comment="归档位置"
    )

    created_by = Column(
        Integer,
        nullable=True,
        comment="创建人ID"
    )
