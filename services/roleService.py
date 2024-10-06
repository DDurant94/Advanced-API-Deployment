from sqlalchemy.orm import Session
from database import db
from sqlalchemy import select

from models.role import Role

# adding role
def save(role_data):
  with Session(db.engine) as session:
    with session.begin():
      new_role = Role(role_name = role_data['role_name'])
      session.add(new_role)
      session.commit()
    session.refresh(new_role)
  return new_role

# getting all roles
def find_all():
  query= select(Role)
  roles = db.session.execute(query).scalars().all()
  return roles

# changing role information
def update(role_update_data, id):
  with Session(db.engine) as session:
    with session.begin():
      role = db.session.execute(db.select(Role).where(Role.id == id)).unique().scalar_one_or_none()
      role.id = role_update_data['id']
      role.role_name = role_update_data['role_name']
    db.session.commit()
  return role