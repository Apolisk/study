import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime, text, join, outerjoin, func, desc
from sqlalchemy.orm import declarative_base, Session, join
from sqlalchemy.types import JSON

Base = declarative_base()
# Donataions
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/test_donate")

session = Session(bind=engine)



with engine.connect() as connection:
    res = connection.execute(text("SELECT VERSION()"))
    print(f"{res=}")

class users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

class cards(Base):
    __tablename__ = 'cards'
    card_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('usersss.id'))
    card_mask = Column(String)
    status = Column(String)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

class campaigns(Base):
    __tablename__ = 'campaigns'
    campaign_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('usersss.id'))
    card_id = Column(Integer, ForeignKey('cards.card_id'))
    registration_date = Column(DateTime(), default=datetime.datetime.now)
    start_date = Column(DateTime())
    end_date = Column(DateTime())
    target_amount = Column(Integer)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

class collectors(Base):
    __tablename__ = 'collectors'
    collector_id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.campaign_id'))
    status = Column(String)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)


class comments(Base):
    __tablename__ = 'comments'
    commen_id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.campaign_id'))
    userss_id = Column(Integer, ForeignKey('usersss.id'))
    comment_text = Column(String)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

class benefits(Base):
    __tablename__ = 'benefits'
    benefit_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('usersss.id'))
    benefit_name = Column(String)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

class benefits_campaign(Base):
    __tablename__ = 'benefits_campaign'
    benefit_id = Column(Integer, ForeignKey('benefits.benefit_id'), primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.campaign_id'), primary_key=True)

class donates(Base):
    __tablename__ = 'donates'
    donate_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usersss.id'))
    status = Column(String)
    campaign_id = Column(Integer, ForeignKey('campaigns.campaign_id'))
    card_id = Column(Integer, ForeignKey('cards.card_id'))
    amount = Column(Integer)
    details = Column(JSON)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

class donate_history(Base):
    __tablename__ = 'donate_history'
    id = Column(Integer, primary_key=True)
    donate_id = Column(Integer, ForeignKey('donates.donate_id'))
    response = Column(String)
    status = Column(String)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

class transfers(Base):
    __tablename__ = 'transfer'
    transfer_id = Column(Integer, primary_key=True)
    collector_id = Column(Integer, ForeignKey('collectors.collector_id'))
    card_id = Column(Integer, ForeignKey('cards.card_id'))
    campaign_id = Column(Integer, ForeignKey('campaigns.campaign_id'))
    amount = Column(Integer)
    details = Column(JSON)
    status = Column(String)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)


Base.metadata.create_all(engine)

# users = session.query(users).all()
#
# for user in users:
#     print(f"{user.first_name} {user.last_name}")


# Simple SELECT
session.query(donates).filter(donates.amount > 1000).all()

session.query(donates).filter(donates.amount > 1000, donates.created_at > '2022-01-08').all()

session.query(donates).filter(donates.amount.between(10, 1000)).all()

session.query(donates.card_id).filter(donates.amount > 0).all()

session.query(users).filter(users.first_name.like('Jack%')).all()

session.query(users).filter(users.id.in_([2, 3])).all()


# joins

(session.query(
    (users.first_name + ' ' + users.last_name).label('full_name'),
    comments.comment_text.label('campaign_description'),
    donates.amount.label('donation_amount')
).join(users, donates.user_id == users.id)
 .join(comments, donates.campaign_id == comments.campaign_id)
 .all())

(session.query(
    (users.first_name + ' ' + users.last_name).label('full_name'),
    comments.comment_text.label('campaign_description')
 ).join(cards, users.id == cards.card_id)
  .join(campaigns, cards.card_id == campaigns.card_id)
  .join(comments, campaigns.campaign_id == comments.campaign_id)
  .all()
)



# limit, offset, order by, asc, desc
session.query(donates).order_by(donates.amount.asc()).limit(5).all()

session.query(donates).order_by(donates.created_at.desc()).offset(2).limit(3).all()


# group by, having, count, sum
(session.query(
        campaigns.author_id.label('user'),
        func.sum(donates.amount).label('total')
    )
    .join(donates, campaigns.campaign_id == donates.campaign_id)
    .group_by(campaigns.campaign_id)
    .having(func.count(donates.donate_id) > 0)
    .order_by(desc(func.sum(donates.amount)))
    .all()
)



