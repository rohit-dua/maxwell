# todo-list REST API

---

#####  Docker Run
1. `docker build -t maxwell:latest .`
2. `docker run  -p 8080:8080 maxwell`
3. `curl http://localhost:8080`

---

##### Routes

* GET `/fetchAccessToken`
	* fetch api access token for registered username/password.
	* Expiry: 1 day

* POST `/register`
	* Register the user. (input: username/password)

* POST `/addList`
	* Add a new list (input: listName)

* POST `/addItem`
	* Add a new item the existing list (input: listId)

* GET `/getLists`
	* Get all list names/ids for the user

* GET `/getList`
	* Get all items of the given list (input: listId)

---

### tests
* `pytest --disable-pytest-warnings app/test.py -vv`
