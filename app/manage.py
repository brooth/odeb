
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import *

class OdebDb():
    """
    manage db
    """
    engine = create_engine('sqlite:///odeb.db', echo=True)
    session = sessionmaker(bind=engine)

    def create(self):
        s = self.session()
        Base.metadata.bind = self.engine
        Base.metadata.drop_all()
        Base.metadata.create_all()
        s.commit()

    def add(self, models):
        s = self.session()
        if isinstance(models, list):
            s.add_all(models)
        else:
            s.add(models)
        s.commit()

class OdebProject():
    """
    manage projec
    """
    db = OdebDb()

    def get(self, name):
        s = self.db.session()
        try:
            return s.query(Project).filter(Project.name == name).get()
        except:
            pass
        finally:
            s.close()


