from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from app.database.database import Base


class TaskHistory(Base):

    __tablename__ = "task_history"

    id = Column(Integer, primary_key=True, index=True)

    task = Column(String)

    selected_tool = Column(String)

    status = Column(String)

    result = Column(String)

    trace = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
