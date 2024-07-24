# Initialize the database
import os

from sqlalchemy import create_engine

from models.reminder import Base, ReminderDAO

POSTGRES_URL = "postgresql://default:L1XCYNxpHO5J@ep-fragrant-art-015615-pooler.us-east-1.aws.neon.tech"
engine = create_engine(POSTGRES_URL)  # ('sqlite:///reminders.db')
Base.metadata.create_all(engine)

reminder_dao = ReminderDAO(engine)
