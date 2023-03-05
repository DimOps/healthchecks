from sqlalchemy import create_engine, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from typing import List

engine = create_engine("sqlite:///healthchecks.db", echo=True)
Base = declarative_base()


class Check(Base):
    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column()
    host: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()

    current_state: Mapped[List["Status"]] = relationship(back_populates="checking")


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ping_id: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column()
    last_down_start: Mapped[int] = mapped_column()
    last_down_end: Mapped[int] = mapped_column()
    check_id = mapped_column(ForeignKey("checks.id"))

    checking: Mapped["Check"] = relationship(back_populates="current_state")


Base.metadata.create_all(engine)
