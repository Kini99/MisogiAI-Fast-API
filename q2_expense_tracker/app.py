from fastapi import FastAPI, HTTPException, Depends, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import List, Optional
import os

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./expenses.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model
class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic models
class ExpenseBase(BaseModel):
    description: str
    amount: float
    category: str
    date: date
    
    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v
    
    @validator('category')
    def category_must_be_valid(cls, v):
        valid_categories = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Bills', 'Other']
        if v not in valid_categories:
            raise ValueError(f'Category must be one of: {", ".join(valid_categories)}')
        return v

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CategoryTotal(BaseModel):
    category: str
    total: float

class TotalResponse(BaseModel):
    total_amount: float
    category_breakdown: List[CategoryTotal]

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(title="Expense Tracker", version="1.0.0")

# Templates
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Sample data
def add_sample_data(db: Session):
    if db.query(Expense).count() == 0:
        sample_expenses = [
            Expense(description="Lunch", amount=15.50, category="Food", date=date(2025, 1, 15)),
            Expense(description="Gas", amount=45.00, category="Transport", date=date(2025, 1, 16)),
            Expense(description="Movie tickets", amount=25.00, category="Entertainment", date=date(2025, 1, 17)),
            Expense(description="Groceries", amount=75.30, category="Food", date=date(2025, 1, 18)),
            Expense(description="Electricity bill", amount=120.00, category="Bills", date=date(2025, 1, 19)),
        ]
        db.add_all(sample_expenses)
        db.commit()

# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    expenses = db.query(Expense).order_by(Expense.date.desc()).all()
    categories = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Bills', 'Other']
    
    # Calculate totals
    total_amount = sum(expense.amount for expense in expenses)
    category_totals = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "expenses": expenses,
        "categories": categories,
        "total_amount": total_amount,
        "category_totals": category_totals
    })

@app.get("/api/expenses", response_model=List[ExpenseResponse])
async def get_expenses(
    db: Session = Depends(get_db),
    start_date: Optional[date] = Query(None, description="Start date for filtering"),
    end_date: Optional[date] = Query(None, description="End date for filtering")
):
    query = db.query(Expense)
    
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    
    return query.order_by(Expense.date.desc()).all()

@app.post("/api/expenses", response_model=ExpenseResponse)
async def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.put("/api/expenses/{expense_id}", response_model=ExpenseResponse)
async def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    for key, value in expense.dict().items():
        setattr(db_expense, key, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.delete("/api/expenses/{expense_id}")
async def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted successfully"}

@app.get("/api/expenses/category/{category}", response_model=List[ExpenseResponse])
async def get_expenses_by_category(category: str, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.category == category).order_by(Expense.date.desc()).all()
    return expenses

@app.get("/api/expenses/total", response_model=TotalResponse)
async def get_total_expenses(db: Session = Depends(get_db)):
    total_amount = db.query(func.sum(Expense.amount)).scalar() or 0
    
    category_totals = db.query(
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).group_by(Expense.category).all()
    
    breakdown = [CategoryTotal(category=cat, total=total) for cat, total in category_totals]
    
    return TotalResponse(total_amount=total_amount, category_breakdown=breakdown)

# Web UI endpoints
@app.post("/expenses/add")
async def add_expense_web(
    description: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        expense_date = datetime.strptime(date, "%Y-%m-%d").date()
        expense = ExpenseCreate(
            description=description,
            amount=amount,
            category=category,
            date=expense_date
        )
        db_expense = Expense(**expense.dict())
        db.add(db_expense)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/expenses/{expense_id}/delete")
async def delete_expense_web(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(db_expense)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/expenses/filter")
async def filter_expenses(
    request: Request,
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Expense)
    if category:
        query = query.filter(Expense.category == category)
    
    expenses = query.order_by(Expense.date.desc()).all()
    categories = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Bills', 'Other']
    
    total_amount = sum(expense.amount for expense in expenses)
    category_totals = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "expenses": expenses,
        "categories": categories,
        "total_amount": total_amount,
        "category_totals": category_totals,
        "selected_category": category
    })

# Startup event
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        add_sample_data(db)
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 