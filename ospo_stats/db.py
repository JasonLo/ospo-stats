import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

load_dotenv()
TURSO_DB_URL = os.getenv("TURSO_DB_URL")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")
ENGINE = create_engine(
    f"sqlite+{TURSO_DB_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true",
    connect_args={"check_same_thread": False},
    echo=True,
)


class Base(DeclarativeBase):
    pass


class Repo(Base):
    """Repo table ORM definition."""

    __tablename__ = "repo"
    url: Mapped[str] = mapped_column(String(1024), primary_key=True)
    crawl_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.current_timestamp()
    )
    created_at: Mapped[datetime] = mapped_column(DateTime)
    owner: Mapped[str] = mapped_column(String(256))
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[Optional[str]] = mapped_column(Text)
    homepage_url: Mapped[Optional[str]] = mapped_column(String(1024))
    last_pushed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    license_key: Mapped[Optional[str]] = mapped_column(String(256))
    license_name: Mapped[Optional[str]] = mapped_column(String(256))
    readme: Mapped[Optional[str]] = mapped_column(Text)
    readme_has_image: Mapped[Optional[bool]] = mapped_column(Boolean)
    total_stargazer_count: Mapped[int] = mapped_column(Integer)
    total_issues_count: Mapped[int] = mapped_column(Integer)
    total_open_issues_count: Mapped[int] = mapped_column(Integer)
    total_forks_count: Mapped[int] = mapped_column(Integer)
    total_watchers_count: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"Repo({self.owner}/{self.name})"


def hard_reset() -> None:
    """Wipe the database and re-create."""
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)
