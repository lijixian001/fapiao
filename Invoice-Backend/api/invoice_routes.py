from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from core.database import get_db
from core.auth import get_current_user
from schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceResponse, InvoiceDetailResponse, InvoiceItemResponse
from schemas.common import ResponseModel, PageResponse
from services.invoice_service import InvoiceService

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
    result = InvoiceService.list_invoices(
        db, page=page, page_size=page_size,
        keyword=keyword, invoice_status=invoice_status,
        invoice_type=invoice_type
    )
    return ResponseModel(data=result)


@router.get("/{invoice_id}", response_model=ResponseModel[InvoiceDetailResponse])
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    invoice = InvoiceService.get_invoice_by_id(db, invoice_id)
    if not invoice:
        return ResponseModel(code=404, message="发票不存在", data=None)
    items = InvoiceService.get_invoice_items(db, invoice_id)
    result = InvoiceDetailResponse.model_validate(invoice)
    result.items = items
    return ResponseModel(data=result)


@router.post("", response_model=ResponseModel[InvoiceResponse])
def create_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    invoice = InvoiceService.create_invoice(db, invoice_data, created_by=current_user["user_id"])
    return ResponseModel(data=invoice, message="创建成功")


@router.put("/{invoice_id}", response_model=ResponseModel[InvoiceResponse])
def update_invoice(
    invoice_id: int,
    invoice_data: InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    invoice = InvoiceService.update_invoice(db, invoice_id, invoice_data)
    return ResponseModel(data=invoice, message="更新成功")


@router.delete("/{invoice_id}", response_model=ResponseModel)
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    InvoiceService.delete_invoice(db, invoice_id)
    return ResponseModel(message="删除成功")


@router.post("/{invoice_id}/archive", response_model=ResponseModel[InvoiceResponse])
def archive_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    invoice = InvoiceService.archive_invoice(db, invoice_id)
    return ResponseModel(data=invoice, message="归档成功")


@router.post("/archive/unarchive", response_model=ResponseModel[InvoiceResponse])
def unarchive_invoice(
    invoice_id: int = Query(..., description="发票ID"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    invoice = InvoiceService.unarchive_invoice(db, invoice_id)
    return ResponseModel(data=invoice, message="取消归档成功")


@router.post("/{invoice_id}/verify", response_model=ResponseModel[InvoiceResponse])
def verify_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    invoice = InvoiceService.verify_invoice(db, invoice_id)
    return ResponseModel(data=invoice, message="审核成功")
