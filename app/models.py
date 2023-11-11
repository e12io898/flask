import datetime

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy import create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import sessionmaker, relationship, mapped_column


DSN = 'sqlite:///db.sqlite'
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False)


class Ads(Base):
    __tablename__ = 'ads'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user = relationship(User, backref='ads')

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
        }


Base.metadata.create_all(bind=engine)
