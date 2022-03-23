from typing import List

import sqlalchemy as sa
from sqlalchemy import Column, DateTime, BigInteger, String, sql, Text, Boolean

from loader import db


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db.func.now())
    updated_at = Column(
        DateTime(True),
        default=db.func.now(),
        onupdate=db.func.now(),
        server_default=db.func.now(),
    )


class ParseChannel(BaseModel):
    __tablename__ = 'tg_channels'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200))
    channel_input = Column(String(100), nullable=False)
    channel_id = Column(BigInteger)
    last_max_id = Column(BigInteger, default=0)
    dt = Column(DateTime)

    query: sql.Select


class TgMessage(TimedBaseModel):
    __tablename__ = 'tg_messages'
    id = Column(String(20), primary_key=True)
    channel_id = Column(BigInteger, index=True)
    msg_id = Column(BigInteger, index=True)
    group_id = Column(BigInteger, index=True)
    date = Column(DateTime)
    text = Column(Text)


class TgMedia(TimedBaseModel):
    __tablename__ = 'tg_media'
    id = Column(BigInteger, primary_key=True)
    channel_id = Column(BigInteger, index=True)
    message_id = Column(String(20), index=True)
    msg_id = Column(BigInteger, index=True)
    group_id = Column(BigInteger, index=True)
    file = Column(String(255))
    storage = Column(Boolean, index=True)
    date = Column(DateTime)
