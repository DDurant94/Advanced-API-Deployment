from database import db,Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

# Customer Account database table
class CustomerAccount(Base):
  __tablename__ = 'Customer_Accounts'
  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(db.String(255), nullable=False)
  customer_id: Mapped[int] = mapped_column(db.ForeignKey('Customers.id'))
  role: Mapped[str] = mapped_column(db.String(80),nullable=False)
  
  customer: Mapped["Customer"] = db.relationship(back_populates="customer_account")
  
  roles: Mapped[List["Role"]] = db.relationship(secondary = "Customer_Management_Roles",lazy='joined')