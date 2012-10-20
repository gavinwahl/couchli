# couchli
Interactive shell for couch

# example

```
> use http://localhost:5984  # use this prefix from now on
> get
GET http://localhost:5984/ {}
200 {
    "couchdb": "Welcome", 
    "version": "1.2.0"
}
> put testdb {}  # create a databse
PUT http://localhost:5984/testdb {'content-type': 'application/json'}
201 {
    "ok": true
}
> use testdb  # use this databse from now on
> get _all_docs
GET http://localhost:5984/testdb/_all_docs {}
200 {
    "offset": 0, 
    "rows": [], 
    "total_rows": 0
}
> post .  # create document. this will open your $EDITOR.
POST http://localhost:5984/testdb/ {'content-type': 'application/json'}
201 {
    "id": "6c36e9fdbed957bdc27c104f80005f34", 
    "ok": true, 
    "rev": "1-4c6114c65e295552ab1019e2b046b10e"
}
> get  # look at the document we just created
GET http://localhost:5984/testdb/6c36e9fdbed957bdc27c104f80005f34 {}
200 {
    "_id": "6c36e9fdbed957bdc27c104f80005f34", 
    "_rev": "1-4c6114c65e295552ab1019e2b046b10e", 
    "foo": "bar"
}
> delete  # delete the document we just created
DELETE http://localhost:5984/testdb/6c36e9fdbed957bdc27c104f80005f34 {'if-match': u'1-4c6114c65e295552ab1019e2b046b10e'}
200 {
    "id": "6c36e9fdbed957bdc27c104f80005f34", 
    "ok": true, 
    "rev": "2-185ccf92154a9f24a4f4fd12233bf463"
}
```
