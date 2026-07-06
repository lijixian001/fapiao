# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：models/invoice_main.py
# 模块用途：发票主表数据模型，定义发票基本信息表结构
# 说明：
#   - 存储发票的基本信息，包括发票头信息、购销方信息、金额汇总等
#   - 发票明细存储在invoice_item表中，通过外键关联
#   - 定义了发票类型和发票状态的常量枚举
# ================================================================================

# 从SQLAlchemy导入列、字符串、整数、十进制、日期和文本类型
from sqlalchemy import Column, String, Integer, DECIMAL, Date, Text
# 从基础模型导入BaseModel
from models.base import BaseModel

# ========================================
# 发票类型常量定义
# ========================================
# 增值税专用发票 - 可以抵扣进项税
INVOICE_TYPE_SPECIAL = 1
# 增值税普通发票 - 不能抵扣进项税
INVOICE_TYPE_NORMAL = 2
# 电子增值税专用发票 - 电子版专用发票
INVOICE_TYPE_ELECTRONIC_SPECIAL = 3
# 电子增值税普通发票 - 电子版普通发票
INVOICE_TYPE_ELECTRONIC_NORMAL = 4

# ========================================
# 发票状态常量定义
# ========================================
# 待审核 - 发票已录入但尚未审核
INVOICE_STATUS_PENDING = 0
# 已审核 - 发票已审核通过
INVOICE_STATUS_VERIFIED = 1
# 已作废 - 发票已作废
INVOICE_STATUS_CANCELLED = 2
# 已红冲 - 发票已红冲（负数发票）
INVOICE_STATUS_RED = 3
# 已归档 - 发票已归档存储
INVOICE_STATUS_ARCHIVED = 4
# 已抵扣 - 发票已进行进项税抵扣
INVOICE_STATUS_DEDUCTED = 5

# ========================================
# 抵扣状态常量定义
# ========================================
# 未抵扣
DEDUCT_STATUS_NO = 0
# 已抵扣
DEDUCT_STATUS_YES = 1


class InvoiceMain(BaseModel):
    """
    发票主表模型类
    对应数据库表 invoice_main，存储发票的基本信息（发票头）

    表关联:
        - 与 invoice_item 表是一对多关系（一张发票对应多条明细）
        - 与 sys_user 表通过 created_by 关联（记录创建人）

    字段说明:
        - id: 主键ID（继承自BaseModel）
        - 发票基本信息: invoice_code, invoice_number, invoice_date, invoice_type, invoice_status
        - 销方信息: seller_name, seller_tax_no
        - 购方信息: buyer_name, buyer_tax_no
        - 金额信息: total_amount, total_tax, total_price_tax
        - 其他信息: check_code, remark, deduct_status, deduct_date, archive_location
        - 审计信息: created_by, created_at, updated_at
    """
    # 指定对应的数据库表名
    __tablename__ = "invoice_main"

    # 发票代码字段
    # 纸质发票的发票代码，电子发票可能为空
    invoice_code = Column(
        String(20),
        nullable=True,
        comment="发票代码"
    )

    # 发票号码字段
    # 发票的唯一编号，必填字段
    invoice_number = Column(
        String(20),
        nullable=False,
        comment="发票号码"
    )

    # 开票日期字段
    # 发票的开具日期，Date类型只存日期不存时间
    invoice_date = Column(
        Date,
        nullable=True,
        comment="开票日期"
    )

    # 发票类型字段
    # 参见上方发票类型常量：1=专票, 2=普票, 3=电子专票, 4=电子普票
    # 默认为增值税专用发票
    invoice_type = Column(
        Integer,
        default=INVOICE_TYPE_SPECIAL,
        nullable=False,
        comment="发票类型"
    )

    # 发票状态字段
    # 参见上方发票状态常量：0=待审核, 1=已审核, 2=已作废等
    # 默认状态为待审核
    invoice_status = Column(
        Integer,
        default=INVOICE_STATUS_PENDING,
        nullable=False,
        comment="发票状态"
    )

    # 销方名称字段
    # 销售方（开票方）的企业名称
    seller_name = Column(
        String(200),
        nullable=True,
        comment="销方名称"
    )

    # 销方税号字段
    # 销售方的纳税人识别号
    seller_tax_no = Column(
        String(50),
        nullable=True,
        comment="销方税号"
    )

    # 购方名称字段
    # 购买方（受票方）的企业名称
    buyer_name = Column(
        String(200),
        nullable=True,
        comment="购方名称"
    )

    # 购方税号字段
    # 购买方的纳税人识别号
    buyer_tax_no = Column(
        String(50),
        nullable=True,
        comment="购方税号"
    )

    # 合计金额字段
    # 不含税金额总计，DECIMAL(18,2)精度
    # 保留2位小数，最多18位整数
    total_amount = Column(
        DECIMAL(18, 2),
        default=0,
        nullable=False,
        comment="合计金额"
    )

    # 合计税额字段
    # 税额总计
    total_tax = Column(
        DECIMAL(18, 2),
        default=0,
        nullable=False,
        comment="合计税额"
    )

    # 价税合计字段
    # 金额加税额的总计（含税总额）
    total_price_tax = Column(
        DECIMAL(18, 2),
        default=0,
        nullable=False,
        comment="价税合计"
    )

    # 校验码字段
    # 增值税普通发票的校验码，用于查验发票真伪
    check_code = Column(
        String(20),
        nullable=True,
        comment="校验码"
    )

    # 备注字段
    # 发票备注信息，使用Text类型支持较长文本
    remark = Column(
        String(500),
        nullable=True,
        comment="备注"
    )

    # 抵扣状态字段
    # 参见上方抵扣状态常量：0=未抵扣, 1=已抵扣
    # 默认未抵扣
    deduct_status = Column(
        Integer,
        default=DEDUCT_STATUS_NO,
        nullable=False,
        comment="抵扣状态"
    )

    # 抵扣日期字段
    # 进行进项税抵扣的日期
    deduct_date = Column(
        Date,
        nullable=True,
        comment="抵扣日期"
    )

    # 归档位置字段
    # 纸质发票的归档存放位置，便于查找
    archive_location = Column(
        String(200),
        nullable=True,
        comment="归档位置"
    )

    # 创建人ID字段
    # 记录录入发票的用户ID
    created_by = Column(
        Integer,
        nullable=True,
        comment="创建人ID"
    )
