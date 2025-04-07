import zoneinfo
from datetime import datetime


from fastapi import FastAPI
from models import Customer,CustomerCreate, Transaction, Invoice

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola, Luis!"}


country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

current_id: int = 0
db_customers: list[Customer] = []

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate):
    customer = Customer.model_validate(customer_data.model_dump())
    customer.id = len(db_customers) + 1
    db_customers.append(customer)
    # Simulate a database operation
    return customer

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    # Simulate a database operation
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    # Simulate a database operation
    return invoice_data