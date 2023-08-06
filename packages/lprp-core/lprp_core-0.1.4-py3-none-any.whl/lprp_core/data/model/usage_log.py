from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lprp_core.data.model.model_base import ModelBase

if TYPE_CHECKING:
    from lprp_core.data.model.user import User
    from lprp_core.data.model.client import Client
    from lprp_core.data.model.vehicle import Vehicle


class UsageLog(ModelBase):
    __tablename__ = "UsageLog"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True)
    timestamp: Mapped[float] = mapped_column(default=None)
    user_username: Mapped[str] = mapped_column(
        ForeignKey("Users.username"), init=False, default=None, repr=False
    )
    user: Mapped[User] = relationship(init=False, default=None)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("Vehicles.id"), init=False, default=None, repr=False
    )
    vehicle: Mapped[Vehicle] = relationship(init=False, default=None)
    client_id: Mapped[str] = mapped_column(
        ForeignKey("Client.uuid"), init=False, default=None, repr=False
    )
    client: Mapped[Client] = relationship(init=False, default=None)
    image_path: Mapped[str] = mapped_column(default=None)