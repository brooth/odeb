
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from functools import wraps

from .models import Base, Project


def call_in_transaction(function=None, commit=True):
    """ Call in transaction decorator """
    def decorator(fun):
        @wraps(fun)
        def wrapper(self, *args, **kwargs):
            s = self.session()
            kwargs['session'] = s
            try:
                return fun(self, *args, **kwargs)
            finally:
                if commit:
                    s.commit()
                s.close()
        return wrapper
    return decorator if not function else decorator(function)


class OdebProject:
    """ ODEB Project """

    def __init__(self, engine_str):
        self.engine = create_engine(engine_str, echo=False)
        self.session = sessionmaker(bind=self.engine)

    @call_in_transaction
    def __add(self, element, session):
        session.add(element)

    @call_in_transaction
    def create(self, name, path, session):
        Base.metadata.bind = self.engine
        Base.metadata.create_all()

        p = Project()
        p.id = 1
        p.name = name
        p.path = path
        self.__add(p)

    @call_in_transaction
    def delete(self, session):
        Base.metadata.bind = self.engine
        Base.metadata.drop_all()

    @call_in_transaction(commit=False)
    def get(self, session):
        model = session.query(Project).filter(Project.id == 1).first()
        session.expunge(model)
        return model


def get_project(engine_str):
    return OdebProject(engine_str)
