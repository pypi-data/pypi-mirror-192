from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker
from lprp_core.data.model import *
from lprp_core.data.model.model_base import ModelBase


def subclasses_recursive(cls: type) -> list[type]:
    direct = cls.__subclasses__()
    indirect = []
    for subclass in direct:
        indirect.extend(subclasses_recursive(subclass))
    return direct + indirect


class PersistenceManager:
    def __init__(self, engine_string: str = "sqlite:///data.sqlite"):
        # init persistent relational db
        self._engine = create_engine(engine_string, echo=True)
        self._map_orm()
        self._session_maker = sessionmaker(bind=self._engine)
        self._session = self._session_maker()

    def _map_orm(self):
        mapper_registry = registry()
        # register every model class
        for cls in subclasses_recursive(ModelBase):
            print(f"[INFO]: mapping class {cls.__name__}")
            mapper_registry.mapped_as_dataclass(cls)
        mapper_registry.metadata.create_all(bind=self._engine)

    def get_object(self, cls: type, id) -> ModelBase:
        """returns an object of type cls with id id"""
        session = self._session
        obj = session.query(cls).get(id)
        return obj


    def get_objects(self, cls: type) -> list[ModelBase]:
        """returns all objects of type cls"""
        session = self._session
        objs = session.query(cls).all()
        return objs

    def save_object(self, obj: ModelBase):
        """saves an object"""
        session = self._session
        session.add(obj)
        session.commit()

    def save_objects(self, objs: list[ModelBase]):
        """saves a list of objects"""
        session = self._session
        for obj in objs:
            session.add(obj)
        session.commit()

    def delete_object(self, obj: ModelBase):
        """deletes an object"""
        session = self._session
        session.delete(obj)
        session.commit()

    def delete_objects(self, objs: list[ModelBase]):
        """deletes a list of objects"""
        session = self._session
        for obj in objs:
            session.delete(obj)
        session.commit()
