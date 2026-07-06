# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：models/invoice_item.py
# 模块用途：发票明细模型
# ================================================================================

from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey
from models.base import BaseModel


class InvoiceItem(BaseModel):
    __tablename__ = "invoice_item"

    invoice_id = Column(
        Integer,
        ForeignKey("invoice_main.id"),
        nullable=False,
        comment="发票主表ID"
    )

    item_name = Column(
        String(200),
        nullable=False,
        comment="商品名称"
    )

    specification = Column(
        String(100),
        nullable=True,
        comment="规格型号"
    )

    unit = Column(
        String(20),
        nullable=True,
        comment="单位"
    )

    quantity = Column(
        Integer,
        default=1,
        nullable=False,
        comment="数量"
    )

    unit_price = Column(
        DECIMAL(18, 6),
        default=0,
        nullable=False,
        comment="单价"
    )

    amount = Column(
        DECIMAL(18, 2),
        default=0,
        nullable=False,
        comment="金额"
    )

    tax_rate = Column(
        DECIMAL(5, 4),
        default=0,
        nullable=False,
        comment="税率"
    )

    tax_amount = Column(
        DECIMAL(18, 2),
        default=0,
        nullable=False,
        comment="税额"
    )
