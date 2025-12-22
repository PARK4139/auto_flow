import logging
from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import Base and models from the models file to ensure they are registered
from pk_internal_tools.pk_objects.pk_db_models import Base, PkGenericState, PkMediaFileState # Added PkMediaFileState

logger = logging.getLogger(__name__)

class PkDatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PkDatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name="pk_system_state.db"):
        # Prevent re-initialization
        if hasattr(self, '_initialized') and self._initialized:
            return

        from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN
        db_path = D_PK_ROOT_HIDDEN / "pk_databases" / db_name
        
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.database_url = f"sqlite:///{db_path}"
        self.engine = create_engine(self.database_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        self._initialized = True
        logger.info(f"DatabaseManager initialized for database at: {db_path}")
        self.create_tables()

    def create_tables(self):
        """
        Create all tables in the database that are defined in the Base metadata.
        """
        logger.info("Creating database tables if they don't exist...")
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Tables created successfully.")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}", exc_info=True)

    def get_db(self) -> Session:
        """
        Provides a database session.
        """
        return self.SessionLocal()

    def upsert_state(self, state_key: str, state_data: dict) -> bool:
        """
        Inserts a new state or updates an existing one in the pk_generic_states table.
        """
        db = self.get_db()
        try:
            # Check if the state already exists
            existing_state = db.query(PkGenericState).filter(PkGenericState.state_key == state_key).first()
            
            if existing_state:
                # Update existing state
                existing_state.state_value = state_data
                logging.debug(f"Updating state for key: {state_key}")
            else:
                # Insert new state
                new_state = PkGenericState(state_key=state_key, state_value=state_data)
                db.add(new_state)
                logging.debug(f"Inserting new state for key: {state_key}")
                
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error in upsert_state for key '{state_key}': {e}", exc_info=True)
            return False
        finally:
            db.close()

    def get_state(self, state_key: str) -> Optional[dict]:
        """
        Retrieves a state from the pk_generic_states table by its key.
        """
        db = self.get_db()
        try:
            state = db.query(PkGenericState).filter(PkGenericState.state_key == state_key).first()
            if state:
                logging.debug(f"State retrieved for key: {state_key}")
                return state.state_value
            else:
                logging.debug(f"No state found for key: {state_key}")
                return None
        except Exception as e:
            logger.error(f"Error in get_state for key '{state_key}': {e}", exc_info=True)
            return None
        finally:
            db.close()

    def update_file_state(self, file_path: str, status: str, window_title: Optional[str] = None) -> bool:
        """
        Updates the state of a media file.
        Inserts if not exists, updates if exists.
        """
        db = self.get_db()
        try:
            file_state = db.query(PkMediaFileState).filter(PkMediaFileState.file_path == file_path).first()
            if file_state:
                file_state.status = status
                file_state.window_title = window_title
                logging.debug(f"Updating file state for '{file_path}': status={status}, window_title={window_title}")
            else:
                new_file_state = PkMediaFileState(file_path=file_path, status=status, window_title=window_title)
                db.add(new_file_state)
                logging.debug(f"Inserting new file state for '{file_path}': status={status}, window_title={window_title}")
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error in update_file_state for '{file_path}': {e}", exc_info=True)
            return False
        finally:
            db.close()

    def get_file_state(self, file_path: str) -> Optional[dict]:
        """
        Retrieves the state of a media file.
        Returns a dictionary representation of PkMediaFileState or None if not found.
        """
        db = self.get_db()
        try:
            file_state = db.query(PkMediaFileState).filter(PkMediaFileState.file_path == file_path).first()
            if file_state:
                logging.debug(f"File state retrieved for '{file_path}': status={file_state.status}")
                return file_state.to_dict()
            else:
                logging.debug(f"No file state found for '{file_path}'.")
                return None
        except Exception as e:
            logger.error(f"Error in get_file_state for '{file_path}': {e}", exc_info=True)
            return None
        finally:
            db.close()

# Singleton instance for easy access
db_manager = PkDatabaseManager()

