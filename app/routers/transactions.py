
from fastapi import APIRouter, status, HTTPException
from models import Transaction, TransactionCreate, Customer
from db import SessionDep
from sqlmodel import select

router = APIRouter()


@router.post("/transactions", status_code=status.HTTP_201_CREATED, tags=["transactions"])
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict["customer_id"])
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer not found",
        )
        
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@router.get("/transactions", tags=["transactions"])
async def list_transactions(session: SessionDep):
    query = select(Transaction)
    transaction = session.exec(query).all()
    return transaction