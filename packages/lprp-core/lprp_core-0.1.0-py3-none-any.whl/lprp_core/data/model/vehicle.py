from __future__ import annotations

from dataclasses import field
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lprp_core.data.model.model_base import ModelBase

if TYPE_CHECKING:
    from lprp_core.data.model.user import User


class VehicleType(Enum):
    CAR = "car"
    TRUCK = "truck"
    BUS = "bus"
    MOTORBIKE = "motorbike"
    OTHER = "other"


class Vehicle(ModelBase):
    __tablename__ = "Vehicles"

    id: Mapped[int] = mapped_column(init=False, default=None, primary_key=True)

    vehicle_type: VehicleType = field(init=False, default=None)
    _vehicle_type: Mapped[str] = mapped_column(init=False, default=None)
    license_plate: Mapped[str] = mapped_column(init=False, default=None, unique=True)
    user_username: Mapped[str] = mapped_column(
        ForeignKey("Users.username"), init=False, default=None, repr=False
    )
    user: Mapped[User] = relationship(init=False, default=None)

    @property
    def vehicle_type(self):
        return self._vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, value):
        self._vehicle_type = value
