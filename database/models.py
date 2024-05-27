from sqlalchemy import Column, BigInteger, Text


from . import Base


class Auth(Base):
    __tablename__ = "auth"

    tg_id = Column(BigInteger, primary_key=True)
    api_key = Column(Text, nullable=False)
