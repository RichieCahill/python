from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Name(Base):
    __tablename__ = 'names'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Age(Base):
    __tablename__ = 'ages'
    id = Column(Integer, primary_key=True)
    age = Column(Integer, unique=True)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name_id = Column(Integer, ForeignKey('names.id'))
    name = relationship("Name", backref="users")

    age_id = Column(Integer, ForeignKey('ages.id'))
    age = relationship("Age", backref="users")

engine = create_engine('sqlite://')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db_session = Session()

name1 = Name(name='John')
name2 = Name(name='Jane')
name3 = Name(name='Doe')

age1 = Age(age=25)
age2 = Age(age=30)
age3 = Age(age=50)

db_session.add_all([age1, age2, age3, name1, name2, name3])
db_session.commit()

user1 = User(name=name1, age=age1)
user2 = User(name=name2, age=age2)
user3 = User(name=name1, age=age2)
user4 = User(name=name1, age=age3)
user5 = User(name=name3, age=age2)

db_session.add_all([user1, user2, user3])
db_session.commit()

def create_dynamic_filter(filters:dict):
    conditions = []
    cls_mapping     = {'name': Name, 'age': Age}
    user_id_mapping = {'name': User.name_id, 'age': User.age_id}
    for key, values in filters.items():
        if type(values) in (str, int):
            values = (values,)

        relationship_cls = cls_mapping.get(key)
        relationship_name = getattr(relationship_cls, key)
        relationship_ids = [relationship.id for relationship in
            db_session.query(relationship_cls.id).filter(relationship_name.in_(set(values)))
        ]
        conditions.append(user_id_mapping.get(key).in_(relationship_ids))
    return and_(*conditions)

filters = {
    # 'name': ('John', 'Jane'),
    'name': ('John', 'Jane', "Doe"),
    # 'name': ('John', ),
    # 'name': 'John',
    # 'age': (25, 30)
    'age': 30
}



dynamic_filter = create_dynamic_filter(filters)
result = db_session.query(User).filter(dynamic_filter).all()
for user in result:
    print(user.id, user.name.name, user.age.age)