from sqlalchemy import create_engine, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from typing import List

engine = create_engine("sqlite:///healthchecks.db", echo=True)
Base = declarative_base()


class Check(Base):
    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    host: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)

    current_state: Mapped[List["Status"]] = relationship(back_populates="checking",
                                                         cascade='all,delete,delete-orphan')


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ping_id: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, default="unknown")
    lastdownstart: Mapped[int] = mapped_column(nullable=True)
    lastdownend: Mapped[int] = mapped_column(nullable=True)
    check_id = mapped_column(ForeignKey("checks.id"))

    checking: Mapped["Check"] = relationship(back_populates="current_state")


Base.metadata.create_all(engine)
