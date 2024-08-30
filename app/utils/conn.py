from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
from app.utils.config import get_settings

class DatabaseManager:
    def __init__(self):
        self.settings = get_settings()

        self.USER = self.settings.USER
        self.PASSWORD = self.settings.PASSWORD
        self.HOST = self.settings.HOST
        self.DATABASE_NAME = self.settings.DATABASE_NAME

        if not all([self.USER, self.PASSWORD, self.HOST, self.DATABASE_NAME]):
            raise ValueError("Faltan variables de entorno necesarias")

        self.DATABASE_URL = f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}/{self.DATABASE_NAME}"

        try:
            self.engine = create_engine(self.DATABASE_URL)
        except Exception as e:
            raise RuntimeError("Error al conectar con la base de datos") from e

        try:
            self.database = Database(self.DATABASE_URL)
        except Exception as e:
            raise RuntimeError("Error al conectar con la base de datos") from e

        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


    def get_db(self):
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()

db_manager = DatabaseManager()
