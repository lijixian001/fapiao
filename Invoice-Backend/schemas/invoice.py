from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field


class InvoiceItemCreate(BaseModel):
    item_name: str = Field(..., description="商品名称")
    specification: Optional[str] = Field(default=None, description="规格型号")
    unit: Optional[str] = Field(default=None, description="单位")
    quantity: int = Field(default=1, description="数量")
    unit_price: float = Field(default=0, description="单价")
    amount: float = Field(default=0, description="金额")
    tax_rate: float = Field(default=0, description="税率")
    tax_amount: float = Field(default=0, description="税额")


class InvoiceItemResponse(BaseModel):
    id: int
    invoice_id: int
    item_name: str
    specification: Optional[str] = None
    unit: Optional[str] = None
    quantity: int
    unit_price: float
    amount: float
    tax_rate: float
    tax_amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InvoiceCreate(BaseModel):
    invoice_code: Optional[str] = Field(default=None, description="发票代码")
    invoice_number: str = Field(..., description="发票号码")
    invoice_date: Optional[date] = Field(default=None, description="开票日期")
    invoice_type: int = Field(default=1, description="发票类型")
    seller_name: Optional[str] = Field(default=None, description="销方名称")
    seller_tax_no: Optional[str] = Field(default=None, description="销方税号")
    buyer_name: Optional[str] = Field(default=None, description="购方名称")
    buyer_tax_no: Optional[str] = Field(default=None, description="购方税号")
    total_amount: float = Field(default=0, description="合计金额")
    total_tax: float = Field(default=0, description="合计税额")
    total_price_tax: float = Field(default=0, description="价税合计")
    check_code: Optional[str] = Field(default=None, description="校验码")
    remark: Optional[str] = Field(default=None, description="备注")
    items: List[InvoiceItemCreate] = Field(default_factory=list, description="发票明细")


class InvoiceUpdate(BaseModel):
    invoice_code: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    invoice_type: Optional[int] = None
    invoice_status: Optional[int] = None
    seller_name: Optional[str] = None
    seller_tax_no: Optional[str] = None
    buyer_name: Optional[str] = None
    buyer_tax_no: Optional[str] = None
    total_amount: Optional[float] = None
    total_tax: Optional[float] = None
    total_price_tax: Optional[float] = None
    check_code: Optional[str] = None
    remark: Optional[str] = None
    deduct_status: Optional[int] = None
    deduct_date: Optional[date] = None
    archive_location: Optional[str] = None


class InvoiceResponse(BaseModel):
    id: int
    invoice_code: Optional[str] = None
    invoice_number: str
    invoice_date: Optional[date] = None
    invoice_type: int
    invoice_status: int
    seller_name: Optional[str] = None
    seller_tax_no: Optional[str] = None
    buyer_name: Optional[str] = None
    buyer_tax_no: Optional[str] = None
    total_amount: float
    total_tax: float
    total_price_tax: float
    check_code: Optional[str] = None
    remark: Optional[str] = None
    deduct_status: int
    deduct_date: Optional[date] = None
    archive_location: Optional[str] = None
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InvoiceDetailResponse(InvoiceResponse):
    items: List[InvoiceItemResponse] = Field(default_factory=list, description="发票明细")
