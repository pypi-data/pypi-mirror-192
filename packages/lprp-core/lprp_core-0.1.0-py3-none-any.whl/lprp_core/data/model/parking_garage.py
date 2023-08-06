from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column

from lprp_core.data.model.model_base import ModelBase

if TYPE_CHECKING:
    pass


class ParkingGarage(ModelBase):
    __tablename__ = 'ParkingGarages'

    id: Mapped[int] = mapped_column(default=None, primary_key=True)
    garage_name: Mapped[str] = mapped_column(default=None)
    car_space: Mapped[int] = mapped_column(default=0)
    car_current: Mapped[int] = mapped_column(default=0)
    motorbike_space: Mapped[int] = mapped_column(default=0)
    motorbike_current: Mapped[int] = mapped_column(default=0)
    bus_space: Mapped[int] = mapped_column(default=0)
    bus_current: Mapped[int] = mapped_column(default=0)
    truck_space: Mapped[int] = mapped_column(default=0)
    truck_current: Mapped[int] = mapped_column(default=0)
    other_space: Mapped[int] = mapped_column(default=0)
    other_current: Mapped[int] = mapped_column(default=0)

