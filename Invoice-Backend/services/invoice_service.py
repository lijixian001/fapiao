"""
发票服务模块

本模块提供发票管理相关的业务逻辑处理，包括发票的增删改查、
发票明细管理、发票状态变更（归档、取消归档、验真）等核心发票管理功能。
"""

# SQLAlchemy 数据库会话对象，用于数据库操作
from sqlalchemy.orm import Session
# FastAPI HTTP异常类和状态码常量，用于返回标准化的HTTP错误响应
from fastapi import HTTPException, status
# 类型注解：可选类型和列表类型
from typing import Optional, List

# 发票主表模型及状态常量（待审核、已归档）
from models.invoice_main import InvoiceMain, INVOICE_STATUS_PENDING, INVOICE_STATUS_ARCHIVED
# 发票明细表模型
from models.invoice_item import InvoiceItem
# 发票创建、更新和明细创建的数据验证模式
from schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceItemCreate


class InvoiceService:
    """
    发票服务类

    提供发票管理相关的静态方法，封装了发票的增删改查、明细管理和状态变更等业务逻辑。
    所有方法均为静态方法，可直接通过类名调用，无需实例化。
    """

    @staticmethod
    def get_invoice_by_id(db: Session, invoice_id: int) -> Optional[InvoiceMain]:
        """
        根据发票ID查询发票主表信息

        参数:
            db (Session): 数据库会话对象，用于执行数据库查询操作
            invoice_id (int): 发票唯一标识ID

        返回:
            Optional[InvoiceMain]: 发票主表信息对象，若不存在则返回None
        """
        # 根据发票ID查询发票主表记录，返回第一条匹配结果或None
        return db.query(InvoiceMain).filter(InvoiceMain.id == invoice_id).first()

    @staticmethod
    def get_invoice_items(db: Session, invoice_id: int) -> List[InvoiceItem]:
        """
        根据发票ID查询发票明细列表

        参数:
            db (Session): 数据库会话对象，用于执行数据库查询操作
            invoice_id (int): 发票唯一标识ID

        返回:
            List[InvoiceItem]: 发票明细对象列表
        """
        # 根据发票ID查询所有关联的发票明细记录
        return db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).all()

    @staticmethod
    def create_invoice(db: Session, invoice_data: InvoiceCreate, created_by: int = None) -> InvoiceMain:
        """
        创建发票

        创建一条新的发票记录，包括发票主表信息和对应的发票明细项。

        参数:
            db (Session): 数据库会话对象，用于执行数据库操作
            invoice_data (InvoiceCreate): 发票创建数据，包含发票主表信息和明细列表
            created_by (int, optional): 创建该发票的操作人ID，默认为None

        返回:
            InvoiceMain: 创建成功后的发票主表信息对象

        业务逻辑说明:
            1. 创建发票主表实体对象并设置各项属性
            2. 将发票主表对象添加到数据库会话
            3. 执行flush操作获取发票ID（用于关联明细项）
            4. 遍历发票明细数据，创建明细项对象并关联发票ID
            5. 将所有明细项添加到数据库会话
            6. 提交事务到数据库
            7. 刷新发票主表对象以获取最新数据
            8. 返回发票主表信息
        """
        # 创建发票主表实体对象，设置各项发票属性
        db_invoice = InvoiceMain(
            invoice_code=invoice_data.invoice_code,
            invoice_number=invoice_data.invoice_number,
            invoice_date=invoice_data.invoice_date,
            invoice_type=invoice_data.invoice_type,
            seller_name=invoice_data.seller_name,
            seller_tax_no=invoice_data.seller_tax_no,
            buyer_name=invoice_data.buyer_name,
            buyer_tax_no=invoice_data.buyer_tax_no,
            total_amount=invoice_data.total_amount,
            total_tax=invoice_data.total_tax,
            total_price_tax=invoice_data.total_price_tax,
            check_code=invoice_data.check_code,
            remark=invoice_data.remark,
            created_by=created_by
        )
        # 将发票主表对象添加到数据库会话
        db.add(db_invoice)
        # 执行flush操作，将数据写入数据库但不提交事务，用于获取自增的发票ID
        db.flush()

        # 遍历发票明细数据，创建每条明细记录
        for item_data in invoice_data.items:
            # 创建发票明细实体对象，关联当前发票ID
            db_item = InvoiceItem(
                invoice_id=db_invoice.id,
                item_name=item_data.item_name,
                specification=item_data.specification,
                unit=item_data.unit,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                amount=item_data.amount,
                tax_rate=item_data.tax_rate,
                tax_amount=item_data.tax_amount
            )
            # 将发票明细对象添加到数据库会话
            db.add(db_item)

        # 提交事务，将发票主表和所有明细数据持久化到数据库
        db.commit()
        # 刷新发票主表对象，获取数据库中的最新数据
        db.refresh(db_invoice)
        # 返回创建成功的发票主表信息
        return db_invoice

    @staticmethod
    def update_invoice(db: Session, invoice_id: int, invoice_data: InvoiceUpdate) -> InvoiceMain:
        """
        更新发票信息

        根据发票ID更新发票的主表信息，支持部分字段更新。

        参数:
            db (Session): 数据库会话对象，用于执行数据库操作
            invoice_id (int): 发票唯一标识ID
            invoice_data (InvoiceUpdate): 发票更新数据，仅包含需要更新的字段

        返回:
            InvoiceMain: 更新成功后的发票主表信息对象

        异常:
            HTTPException: 
                - 404 Not Found: 发票不存在

        业务逻辑说明:
            1. 根据发票ID查询发票记录
            2. 校验发票是否存在，不存在则抛出404异常
            3. 提取发票数据中已设置的字段（排除未设置的字段）
            4. 遍历更新数据，动态设置发票对象的属性
            5. 提交事务到数据库
            6. 刷新发票对象以获取最新数据
            7. 返回更新后的发票信息
        """
        # 根据发票ID查询发票记录
        invoice = InvoiceService.get_invoice_by_id(db, invoice_id)
        # 发票不存在，抛出404资源未找到异常
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="发票不存在"
            )
        
        # 提取发票数据中已显式设置的字段（排除未设置的字段，实现部分更新）
        update_data = invoice_data.model_dump(exclude_unset=True)
        # 遍历更新数据，使用setattr动态设置发票对象的属性
        for key, value in update_data.items():
            setattr(invoice, key, value)
        
        # 提交事务，将更新后的数据持久化到数据库
        db.commit()
        # 刷新发票对象，获取数据库中的最新数据
        db.refresh(invoice)
        # 返回更新后的发票信息
        return invoice

    @staticmethod
    def delete_invoice(db: Session, invoice_id: int) -> bool:
        """
        删除发票

        根据发票ID删除指定的发票记录，同时删除关联的发票明细。

        参数:
            db (Session): 数据库会话对象，用于执行数据库操作
            invoice_id (int): 发票唯一标识ID

        返回:
            bool: 删除成功返回True

        异常:
            HTTPException: 
                - 404 Not Found: 发票不存在

        业务逻辑说明:
            1. 根据发票ID查询发票记录
            2. 校验发票是否存在，不存在则抛出404异常
            3. 删除该发票关联的所有明细记录
            4. 删除发票主表记录
            5. 提交事务
            6. 返回删除成功标识
        """
        # 根据发票ID查询发票记录
        invoice = InvoiceService.get_invoice_by_id(db, invoice_id)
        # 发票不存在，抛出404资源未找到异常
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="发票不存在"
            )
        
        # 先删除该发票关联的所有明细记录
        db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()
        # 删除发票主表记录
        db.delete(invoice)
        # 提交事务，执行删除操作
        db.commit()
        # 返回删除成功
        return True

    @staticmethod
    def list_invoices(
        db: Session,
        page: int = 1,
        page_size: int = 10,
        keyword: Optional[str] = None,
        invoice_status: Optional[int] = None,
        invoice_type: Optional[int] = None
    ) -> dict:
        """
        分页查询发票列表

        支持按关键字模糊搜索、按发票状态和发票类型筛选，支持分页功能，按创建时间倒序排列。

        参数:
            db (Session): 数据库会话对象，用于执行数据库查询操作
            page (int, optional): 页码，默认为1
            page_size (int, optional): 每页数据条数，默认为10
            keyword (Optional[str], optional): 搜索关键字，支持发票号、销售方名称、购买方名称模糊匹配，默认为None
            invoice_status (Optional[int], optional): 发票状态筛选，默认为None
            invoice_type (Optional[int], optional): 发票类型筛选，默认为None

        返回:
            dict: 分页查询结果，包含以下字段：
                - total (int): 总记录数
                - page (int): 当前页码
                - page_size (int): 每页数据条数
                - list (List[InvoiceMain]): 发票数据列表

        业务逻辑说明:
            1. 构建发票查询对象
            2. 若有关键字，则添加发票号、销售方名称、购买方名称的模糊搜索条件（OR关系）
            3. 若指定了发票状态，则添加状态筛选条件
            4. 若指定了发票类型，则添加类型筛选条件
            5. 按创建时间倒序排序
            6. 查询符合条件的总记录数
            7. 计算分页偏移量，查询当前页的发票数据
            8. 返回分页结果字典
        """
        # 构建发票查询对象
        query = db.query(InvoiceMain)
        
        # 若有关键字，则添加模糊搜索条件（发票号、销售方名称、购买方名称任一匹配）
        if keyword:
            query = query.filter(
                (InvoiceMain.invoice_number.like(f"%{keyword}%")) |
                (InvoiceMain.seller_name.like(f"%{keyword}%")) |
                (InvoiceMain.buyer_name.like(f"%{keyword}%"))
            )
        
        # 若指定了发票状态，则添加状态筛选条件
        if invoice_status is not None:
            query = query.filter(InvoiceMain.invoice_status == invoice_status)
        
        # 若指定了发票类型，则添加类型筛选条件
        if invoice_type is not None:
            query = query.filter(InvoiceMain.invoice_type == invoice_type)
        
        # 按创建时间倒序排序（最新的在前）
        query = query.order_by(InvoiceMain.created_at.desc())
        
        # 查询符合条件的总记录数
        total = query.count()
        # 计算分页偏移量，查询当前页的发票数据列表
        invoices = query.offset((page - 1) * page_size).limit(page_size).all()
        
        # 返回分页结果字典
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "list": invoices
        }

    @staticmethod
    def archive_invoice(db: Session, invoice_id: int) -> InvoiceMain:
        """
        归档发票

        将指定发票的状态更新为已归档状态。

        参数:
            db (Session): 数据库会话对象，用于执行数据库操作
            invoice_id (int): 发票唯一标识ID

        返回:
            InvoiceMain: 更新后的发票主表信息对象

        异常:
            HTTPException: 
                - 404 Not Found: 发票不存在

        业务逻辑说明:
            1. 根据发票ID查询发票记录
            2. 校验发票是否存在，不存在则抛出404异常
            3. 将发票状态更新为已归档
            4. 提交事务到数据库
            5. 刷新发票对象以获取最新数据
            6. 返回更新后的发票信息
        """
        # 根据发票ID查询发票记录
        invoice = InvoiceService.get_invoice_by_id(db, invoice_id)
        # 发票不存在，抛出404资源未找到异常
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="发票不存在"
            )
        
        # 将发票状态更新为已归档
        invoice.invoice_status = INVOICE_STATUS_ARCHIVED
        # 提交事务，将状态变更持久化到数据库
        db.commit()
        # 刷新发票对象，获取数据库中的最新数据
        db.refresh(invoice)
        # 返回更新后的发票信息
        return invoice

    @staticmethod
    def unarchive_invoice(db: Session, invoice_id: int) -> InvoiceMain:
        """
        取消归档发票

        将指定发票的状态从已归档恢复为待审核状态。

        参数:
            db (Session): 数据库会话对象，用于执行数据库操作
            invoice_id (int): 发票唯一标识ID

        返回:
            InvoiceMain: 更新后的发票主表信息对象

        异常:
            HTTPException: 
                - 404 Not Found: 发票不存在

        业务逻辑说明:
            1. 根据发票ID查询发票记录
            2. 校验发票是否存在，不存在则抛出404异常
            3. 将发票状态更新为待审核
            4. 提交事务到数据库
            5. 刷新发票对象以获取最新数据
            6. 返回更新后的发票信息
        """
        # 根据发票ID查询发票记录
        invoice = InvoiceService.get_invoice_by_id(db, invoice_id)
        # 发票不存在，抛出404资源未找到异常
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="发票不存在"
            )
        
        # 将发票状态更新为待审核（取消归档）
        invoice.invoice_status = INVOICE_STATUS_PENDING
        # 提交事务，将状态变更持久化到数据库
        db.commit()
        # 刷新发票对象，获取数据库中的最新数据
        db.refresh(invoice)
        # 返回更新后的发票信息
        return invoice

    @staticmethod
    def verify_invoice(db: Session, invoice_id: int) -> InvoiceMain:
        """
        验真发票

        将指定发票的状态更新为已验真状态。

        参数:
            db (Session): 数据库会话对象，用于执行数据库操作
            invoice_id (int): 发票唯一标识ID

        返回:
            InvoiceMain: 更新后的发票主表信息对象

        异常:
            HTTPException: 
                - 404 Not Found: 发票不存在

        业务逻辑说明:
            1. 延迟导入已验真状态常量（避免循环导入）
            2. 根据发票ID查询发票记录
            3. 校验发票是否存在，不存在则抛出404异常
            4. 将发票状态更新为已验真
            5. 提交事务到数据库
            6. 刷新发票对象以获取最新数据
            7. 返回更新后的发票信息
        """
        # 延迟导入已验真状态常量，避免模块顶部循环导入问题
        from models.invoice_main import INVOICE_STATUS_VERIFIED
        # 根据发票ID查询发票记录
        invoice = InvoiceService.get_invoice_by_id(db, invoice_id)
        # 发票不存在，抛出404资源未找到异常
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="发票不存在"
            )
        
        # 将发票状态更新为已验真
        invoice.invoice_status = INVOICE_STATUS_VERIFIED
        # 提交事务，将状态变更持久化到数据库
        db.commit()
        # 刷新发票对象，获取数据库中的最新数据
        db.refresh(invoice)
        # 返回更新后的发票信息
        return invoice
