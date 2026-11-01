import sys
sys.path.append('.')
from sqlmodel import Session, select
from app.db.session import engine
from app.models.recipe import Food

with Session(engine) as session:
    foods = session.exec(select(Food).limit(4)).all()
    for f in foods:
        f.featured = True
        session.add(f)
    session.commit()
    print("Set {} foods to featured!".format(len(foods)))
