"""Customer / KYC endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from cbs.database import get_db
from cbs.models.customer import Customer
from cbs.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from cbs.utils.iban import generate_reference

router = APIRouter(prefix="/customers", tags=["Customers & KYC"])


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    customer = Customer(
        external_id=generate_reference("CUS"),
        customer_type=data.customer_type,
        first_name=data.first_name,
        last_name=data.last_name,
        company_name=data.company_name,
        tax_id=data.tax_id,
        email=data.email,
        phone=data.phone,
        country=data.country,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/", response_model=list[CustomerResponse])
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, data: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)
    db.commit()
    db.refresh(customer)
    return customer
