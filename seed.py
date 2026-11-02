
import random
import string

from main import app
from models import db, Group


def generate_group_name():
    letters = "".join(
        random.choices(string.ascii_uppercase, k=2)
    )
    numbers = "".join(
        random.choices(string.digits, k=2)
    )

    return f"{letters}-{numbers}"


def create_groups():
    with app.app_context():
        existing_names = {
            group.name for group in db.session.query(Group).all()
        }

        while db.session.query(Group).count() + len(
            db.session.new
        ) < 10:
            name = generate_group_name()

            if name in existing_names:
                continue

            group = Group(name=name)
            db.session.add(group)
            existing_names.add(name)

        db.session.commit()

        print("Groups created successfully!")


if __name__ == "__main__":
    create_groups()
