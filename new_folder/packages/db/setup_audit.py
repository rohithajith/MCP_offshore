import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../..'))

from packages.db.session import engine
from packages.db.models.audit import ActionAudit
from packages.db.base import Base

def setup_audit_table():
    print("Creating action_audits table...")
    Base.metadata.create_all(bind=engine, tables=[ActionAudit.__table__])
    print("Audit table setup complete!")

if __name__ == "__main__":
    setup_audit_table()
