from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table

from sqlalchemy.orm import registry, relationship

mapper_registry = registry()
Base = mapper_registry.generate_base()

insurer_category_table = Table(
    'insurer_category', Base.metadata,
    Column('insurer_id', ForeignKey('insurers.id')),
    Column('category_id', ForeignKey('categories.id')),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)

    insurances = relationship("Insurance", back_populates="user")


class Insurer(Base):
    __tablename__ = "insurers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    telephone = Column(String)

    insurances = relationship("Insurance", back_populates="insurer")
    categories = relationship("Category", secondary=insurer_category_table)


class Insurance(Base):
    __tablename__ = "insurances"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'))
    insurer_id = Column(ForeignKey('insurers.id'))
    insurance_amount = Column(Float)
    insurance_category_id = Column(ForeignKey('categories.id'))
    regularity = Column(Integer)
    detail = Column(Integer)
    coverage_end_date = Column(Integer)

    user = relationship("User", back_populates="insurances")
    insurer = relationship("Insurer", back_populates="insurances")
    category = relationship("Category", back_populates="insurances")


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column('name', String)

    insurances = relationship("Insurance", back_populates="category")
