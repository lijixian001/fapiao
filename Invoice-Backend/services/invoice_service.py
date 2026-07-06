from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, List

from models.invoice_main import InvoiceMain, INVOICE_STATUS_PENDING, INVOICE_STATUS_ARCHIVED
from models.invoice_item import InvoiceItem
from schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceItemCreate


class InvoiceService:
    @staticmethod
    def get_invoice_by_id(db: Session, invoice_id: int) -> Optional[InvoiceMain]:
        return db.query(InvoiceMain).filter(InvoiceMain.id == invoice_id).first()

    @staticmethod
    def get_invoice_items(db: Session, invoice_id: int) -> List[InvoiceItem]:
        return db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).all()

    @staticmethod
    def create_invoice(db: Session, invoice_data: InvoiceCreate, created_by: int = None) -> InvoiceMain:
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
        db.add(db_invoice)
        db.flush()

        for item_data in invoice_data.items:
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
            db.add(db_item)

        db.commit()
        db.refresh(db_invoice)
        return db_invoice

    @staticmethod
    def update_invoice(db: Session, invoice_id: int, invoice_data: InvoiceUpdate) -> InvoiceMain:
        invoice = InvoiceService.get_invoice_by_id(db, invoice_id)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="发票不存在"
            )
        
        update_data = invoice_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(invoice, key, value)
        
        db.commit()
        db.refresh(invoice)
        return invoice

    @staticmethod
    def delete_invoice(db: Session, invoice_id: int) -> bool:
        invoice = InvoiceService.get_invoice_by_id(db, invoice_id)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="发票不存在"
            )
        
        db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()
        db.delete(invoice)
        db.commit()
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
        query = db.query(InvoiceMain)
        
        if keyword:
            query = query.filter(
                (InvoiceMain.invoice_number.like(f"%{keyword}%")) |
                (InvoiceMain.seller_name.like(f"%{keyword}%")) |
                (InvoiceMain.buyer_name.like(f"%{keyword}%"))
            )
        
        if invoice_status is not None:
            query = query.filter(InvoiceMain.invoice_status == invoice_status)
        
        if invoice_type is not None:
            query = query.filter(InvoiceMain.invoice_type == invoice_type)
        
        query = query.order_by(InvoiceMain.created_at.desc())
        
        total = query.count()
        invoices = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "list": invoices
        }

    @staticmethod
    def archive_invoice(db: Session, invoice_id: int) -> InvoiceMain:
        invoice = InvoiceService.get_invoice_by_id(db, invoice_id)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="发票不存在"
            )
        
        invoice.invoice_status = INVOICE_STATUS_ARCHIVED
        db.commit()
        db.refresh(invoice)
        return invoice

    @staticmethod
    def unarchive_invoice(db: Session, invoice_id: int) -> InvoiceMain:
        invoice = InvoiceService.get_invoice_by_id(db, invoice_id)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="发票不存在"
            )
        
        invoice.invoice_status = INVOICE_STATUS_PENDING
        db.commit()
        db.refresh(invoice)
        return invoice

    @staticmethod
    def verify_invoice(db: Session, invoice_id: int) -> InvoiceMain:
        from models.invoice_main import INVOICE_STATUS_VERIFIED
        invoice = InvoiceService.get_invoice_by_id(db, invoice_id)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="发票不存在"
            )
        
        invoice.invoice_status = INVOICE_STATUS_VERIFIED
        db.commit()
        db.refresh(invoice)
        return invoice
