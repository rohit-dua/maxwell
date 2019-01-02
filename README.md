# todo-list REST API
---
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
