#!/usr/bin/python3
import os, sys, argparse
from sqlalchemy import Table, Column, String, Integer, MetaData, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

DBFILE="library.db"
engine = create_engine('sqlite:///%s' % DBFILE)
Session = sessionmaker(bind=engine)
session = Session()

app = argparse.ArgumentParser()
app.add_argument("-a","--action",required=True,help="add/remove/update/find")
app.add_argument("-i","--isbn",required=False, action="store", dest="isbn",  help="book serial number")
app.add_argument("-n","--name",required=False, action="store", dest="name",  help="book name")
app.add_argument("-au","--author",required=False, action="store", dest="author",  help="author")
app.add_argument("-p","--publisher",required=False, action="store", dest="publisher",  help="publisher")
app.add_argument("-t","--booktype" ,required=False, dest="booktype",  help="book type")
app.add_argument("-pc","--pagecount",required=False, action="store", dest="pagecount",  help="page count")

args = vars(app.parse_args())

Base = declarative_base()

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    ISBN = Column(String(20), nullable=False)
    bookname = Column(String(100), nullable=False)
    authorname = Column(String(50), nullable=False)
    publisher = Column(String(50))
    booktype = Column(String(50))
    pagenumber = Column(Integer)      

if os.path.isfile(DBFILE) is False:
    Base.metadata.create_all(engine)

action = args["action"]
isbn = args["isbn"]
name = args["name"]
author= args["author"]
publisher = args["publisher"]
booktype = args["booktype"]
pagenumber = args["pagecount"]

if action == "add":
    #kitap ekle
    new_book=Book(ISBN=isbn, bookname=name, authorname=author, publisher=publisher, booktype=booktype, pagenumber=pagenumber)
    session.add(new_book)
    session.commit()

elif action == "remove":
    #kitap sil
    print("buraya geldi..")
    session.query(Book).filter(Book.ISBN == isbn).delete()
    session.commit()

elif action == "update":
    #kitap guncelle
    book=session.query(Book).filter(Book.ISBN == isbn).all()
    if name != None:
        book[0].bookname=name
    elif author != None:
        book[0].authorname=author
    elif publisher != None:
        book[0].publisher=publisher
    elif booktype != None:
        book[0].booktype=booktype
    elif pagenumber != None:
        book[0].pagenumber=pagenumber
    print(book[0].ISBN," - ",book[0].bookname)
    session.commit()
    session.refresh(book[0])    

elif action == "find":
    #kitap bul
    if name != None: 
       book=session.query(Book).filter(Book.bookname==name)

    elif author != None:
        book=session.query(Book).filter(Book.authorname==author)
    
    elif publisher != None:
        book=session.query(Book).filter(Book.publisher==publisher)
    
    elif booktype != None:
        book=session.query(Book).filter(Book.booktype==booktype)
    
    elif pagenumber != None:
        book=session.query(Book).filter(Book.pagenumber==pagenumber)
    
    elif isbn != None:
        book=session.query(Book).filter(Book.ISBN==isbn)
    
    print(book[0].ISBN)
    print(book[0].bookname)
    print(book[0].authorname)
    print(book[0].publisher)
    print(book[0].booktype)
    print(book[0].pagenumber)        
else: 
    print("add - update - remove - find | sadece bu 4 unden birini girin")  