# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：models/invoice_item.py
# 模块用途：发票明细数据模型，定义发票商品明细行项目表结构
# 说明：
#   - 存储发票的商品/服务明细信息，每行一个商品
#   - 通过invoice_id外键与发票主表关联
#   - 一张发票可以对应多条明细记录
# ================================================================================

# 从SQLAlchemy导入列、字符串、整数、十进制和外键类型
from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey
# 从基础模型导入BaseModel
from models.base import BaseModel


class InvoiceItem(BaseModel):
    """
    发票明细模型类
    对应数据库表 invoice_item，存储发票的商品/服务明细行

    表关联:
        - 与 invoice_main 表是多对一关系（多条明细对应一张发票）
        - 通过 invoice_id 外键关联到发票主表

    字段说明:
        - id: 主键ID（继承自BaseModel）
        - invoice_id: 发票主表ID，外键
        - item_name: 商品/服务名称
        - specification: 规格型号
        - unit: 计量单位
        - quantity: 数量
        - unit_price: 单价（不含税）
        - amount: 金额（不含税）= 数量 × 单价
        - tax_rate: 税率
        - tax_amount: 税额 = 金额 × 税率
        - created_at: 创建时间（继承自BaseModel）
        - updated_at: 更新时间（继承自BaseModel）
    """
    # 指定对应的数据库表名
    __tablename__ = "invoice_item"

    # 发票主表ID字段
    # 外键关联到invoice_main表的id字段
    # 表示这条明细属于哪张发票
    # nullable=False: 必填字段，每条明细必须属于某张发票
    invoice_id = Column(
        Integer,
        ForeignKey("invoice_main.id"),
        nullable=False,
        comment="发票主表ID"
    )

    # 商品名称字段
    # 商品或服务的名称，必填字段
    item_name = Column(
        String(200),
        nullable=False,
        comment="商品名称"
    )

    # 规格型号字段
    # 商品的规格型号信息，可选
    specification = Column(
        String(100),
        nullable=True,
        comment="规格型号"
    )

    # 计量单位字段
    # 商品的计量单位，如：个、件、台、千克等，可选
    unit = Column(
        String(20),
        nullable=True,
        comment="单位"
    )

    # 数量字段
    # 商品的数量，整数类型
    # 默认值为1
    quantity = Column(
        Integer,
        default=1,
        nullable=False,
        comment="数量"
    )

    # 单价字段
    # 不含税单价，DECIMAL(18,6)精度
    # 保留6位小数以支持高精度计算
    unit_price = Column(
        DECIMAL(18, 6),
        default=0,
        nullable=False,
        comment="单价"
    )

    # 金额字段
    # 不含税金额 = 数量 × 单价，DECIMAL(18,2)精度
    # 保留2位小数
    amount = Column(
        DECIMAL(18, 2),
        default=0,
        nullable=False,
        comment="金额"
    )

    # 税率字段
    # 增值税税率，DECIMAL(5,4)精度
    # 例如：0.13表示13%税率，0.09表示9%税率，0.06表示6%税率
    # 保留4位小数支持精确税率
    tax_rate = Column(
        DECIMAL(5, 4),
        default=0,
        nullable=False,
        comment="税率"
    )

    # 税额字段
    # 增值税税额 = 金额 × 税率，DECIMAL(18,2)精度
    # 保留2位小数
    tax_amount = Column(
        DECIMAL(18, 2),
        default=0,
        nullable=False,
        comment="税额"
    )
