
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from sqlalchemy import Sequence, Column, Integer, String
from sqlalchemy.types import DateTime, Boolean
from sqlalchemy.schema import ForeignKey

from .app_utils import to_lower_camel_case

Base = declarative_base()


class BaseModel(object):
    id = Column(Integer, Sequence(__name__.lower() + '_id_seq'), primary_key=True)

    @declared_attr
    def __tablename__(self):
        return to_lower_camel_case(self.__name__) + 's'


class Project(BaseModel, Base):
    name = Column(String(50), nullable=False, unique=True)
    path = Column(String, nullable=False, unique=True)

    def __init__(self):
        self.id = 1


class SourceSet(BaseModel, Base):
    project_id = Column(Integer, ForeignKey(Project.id), nullable=False, default=1)

    name = Column(String(50), nullable=False)
    path = Column(String, nullable=False)
    test = Column(Boolean, nullable=False, default=False)


class Package(BaseModel, Base):
    source_set_id = Column(Integer, ForeignKey(SourceSet.id), nullable=False)
    parent_id = Column(Integer, ForeignKey('packages.id'))

    name = Column(String(50), nullable=False)


class SourceKind(BaseModel, Base):
    name = Column(String(50), nullable=False)


class Source(BaseModel, Base):
    source_set_id = Column(Integer, ForeignKey(SourceSet.id), nullable=False)
    kind_id = Column(Integer, ForeignKey(SourceKind.id), nullable=False)

    path = Column(String, nullable=False)
    modified_ts = Column(DateTime, nullable=False)


class TypeKind(BaseModel, Base):
    name = Column(String(50), nullable=False)


class TypeVisibility(BaseModel, Base):
    name = Column(String(50), nullable=False)


class Type(BaseModel, Base):
    source_id = Column(Integer, ForeignKey(Source.id), nullable=False)
    parent_id = Column(Integer, ForeignKey('types.id'))
    package_id = Column(Integer, ForeignKey(Package.id), nullable=False)
    kind_id = Column(Integer, ForeignKey(TypeKind.id), nullable=False)
    visibility_id = Column(Integer, ForeignKey(TypeVisibility.id), nullable=False)

    name = Column(String(100), nullable=False)
    final = Column(Boolean, nullable=False)
    static = Column(Boolean, nullable=False)
    line_begin = Column(Integer, nullable=False)
    line_end = Column(Integer, nullable=False)
    column_begin = Column(Integer, nullable=False)
    column_end = Column(Integer, nullable=False)


class PropertyVisibility(BaseModel, Base):
    name = Column(String(50), nullable=False)


class Property(BaseModel, Base):
    host_id = Column(Integer, ForeignKey(Type.id), nullable=False)
    visibility_id = Column(Integer, ForeignKey(PropertyVisibility.id), nullable=False)

    type_str = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    final = Column(Boolean, nullable=False)
    static = Column(Boolean, nullable=False)
    line_begin = Column(Integer, nullable=False)
    line_end = Column(Integer, nullable=False)
    column_begin = Column(Integer, nullable=False)
    column_end = Column(Integer, nullable=False)


class FunctionVisibility(BaseModel, Base):
    name = Column(String(50), nullable=False)


class Function(BaseModel, Base):
    host_id = Column(Integer, ForeignKey(Type.id), nullable=False)
    parent_id = Column(Integer, ForeignKey('functions.id'))
    visibility_id = Column(Integer, ForeignKey(FunctionVisibility.id), nullable=False)

    type_str = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    final = Column(Boolean, nullable=False)
    static = Column(Boolean, nullable=False)
    line_begin = Column(Integer, nullable=False)
    line_end = Column(Integer, nullable=False)
    column_begin = Column(Integer, nullable=False)
    column_end = Column(Integer, nullable=False)
