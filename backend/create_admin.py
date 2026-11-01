"""Create or reset an admin user.

Credentials are never stored in source. Pass them as arguments or environment
variables:

    python create_admin.py <username> <password>

    # or
    ADMIN_USERNAME=admin ADMIN_PASSWORD=... python create_admin.py

If an account with the username already exists, it is deleted and recreated so
the password is reset.
"""

import os
import sys

from sqlmodel import Session, select

from app.core.security import get_password_hash
from app.db.session import engine
from app.models.user import User


def resolve_credentials() -> tuple[str, str]:
    username = sys.argv[1] if len(sys.argv) > 1 else os.getenv("ADMIN_USERNAME")
    password = sys.argv[2] if len(sys.argv) > 2 else os.getenv("ADMIN_PASSWORD")

    if not username or not password:
        sys.exit(
            "Missing credentials. Usage: python create_admin.py <username> <password>\n"
            "or set ADMIN_USERNAME and ADMIN_PASSWORD."
        )

    return username, password


def main() -> None:
    username, password = resolve_credentials()

    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            session.delete(existing)
            session.commit()
            print(f"Removed existing user '{username}'.")

        session.add(User(username=username, hashed_password=get_password_hash(password)))
        session.commit()
        print(f"Admin '{username}' created.")


if __name__ == "__main__":
    main()
