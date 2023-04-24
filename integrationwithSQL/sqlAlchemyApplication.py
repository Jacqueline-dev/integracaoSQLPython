from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("user", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id}, email={self.email_address})"


print(User.__tablename__)
print(Address.__tablename__)


# conexão com o banco de dados

engine = create_engine("sqlite://")

# criando as classes como tabela no banco de dados
Base.metadata.create_all(engine)

# depreciado - será removido em futuro release
# print(engine.table_names())

# investiga o esquema de banco de dados
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("user_account"))

print(inspetor_engine.get_table_names())
print(inspetor_engine.defaut_schema_name)

with Session(engine) as sessions:
    juliana = User (
        name='jacqueline',
        fullname = 'Jacqueline Ferreira',
        address = [Address(email_address='codejacque@gmail.com')]

    )

    sandy = User(
        name='sandy',
        fullname='Sandy Cardoso',
        address=[Address(email_address='sandy@emial.br'),
                 Address(email_address='sandyc@emial.org')]
    )

    patrick = User(name='patrick', fullname='Patrick Cardoso')

    # enviando para o BD (persistência de dados)
    session.add_all([jacqueline, sandy, patrick])

    session.commit()


stmt = select(User).where(User.name.in_(['jacqueline', 'sandy']))
print('\nRecuperando usuários a partir de condição de filtragem')
for user in session.scalars(stmt):
    print(user)


stmt_address = select(Address).where(Address.user_id.in_([2]))
print('\nRecuperando os endereços de e-mail de sandy')
for address in session.scalars(stmt_address):
    print(address)


stmt_order = select(User).order_by(User.fullname.desc())
print("\nRecuperando info de maneira ordenada")
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
for result in session.scalars(stmt_join):
    print(result)

# print(select(User.fullname, Address.email_address).join_from(Address, User))

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(User)
print('\nTotal de instância em Use')
for result in session.scalars(stmt_count):
    print(result)