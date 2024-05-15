from flask import Flask, request
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# Configuração básica do SQLAlchemy para conectar ao PostgreSQL
DATABASE_URI = 'postgresql://user:password@localhost/mydatabase'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

Base = declarative_base()

# Modelo de exemplo
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

@app.route('/<tenant_id>')
def index(tenant_id):
    # Conectar ao esquema do tenant especificado
    connection = engine.connect()
    connection.execute(f'SET search_path TO {tenant_id}')
    session = Session(bind=connection)

    # Consulta simples para pegar todos os usuários
    users = session.query(User).all()
    session.close()
    return {'users': [user.name for user in users]}

if __name__ == '__main__':
    app.run(debug=True)
