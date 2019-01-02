from app import app, request
from app.models import User, List, Item, db
from common import checkAuth
import json
import uuid

@app.route('/getList',methods = ['GET'])
@checkAuth
def getList():
    """Get all items of the given list"""
    listId = request.args.get('listId')
    if listId == None:
        return json.dumps({"status": "fail", "message": "missing listId"}), 401
    userId = userData[u'userId']
    list = List.query.filter_by(id=listId).first()
    if list == None:
        return json.dumps({"status": "fail", "message": "list does not exist"}), 400
    items = db.session.query(Item).filter(List.userId == User.id).filter(List.id == Item.listId).filter(User.id == userId).filter(List.id == listId).all()
    itemsArray = []
    for item in items:
        itemsArray.append({"id": item.id, "listId": item.listId, "value": item.value, "completed":item.completed})
    return json.dumps({"status": "success", "data": {"items": itemsArray, "listId": listId}}), 200


@app.route('/addItem', methods = ['POST'])
@checkAuth
def addItem():
    """Add a new item the existing list (input: listId)"""
    req_data = request.get_json()
    listId = req_data['listId']
    item = req_data['item']
    newItem = Item(listId=listId, value=item)
    list = List.query.filter_by(id=listId).first()
    if list == None:
        return json.dumps({"status": "fail", "message": "list does not exist"}), 400
    db.session.add(newItem)
    db.session.commit()
    return json.dumps({"status": "success", "message": "item added"}), 200

@app.route('/addList', methods = ['POST'])
@checkAuth
def addList():
    """Add a new list (input: listName)"""
    req_data = request.get_json()
    listName = req_data['listName']
    username = userData[u'username']
    userId = userData[u'userId']
    id = uuid.uuid4().hex
    newList = List(id=id,name=listName, userId=userId)
    db.session.add(newList)
    db.session.commit()
    return json.dumps({"status": "success", "message": "list added", "id":id}), 200

@app.route('/getLists',methods = ['GET'])
@checkAuth
def getLists():
    """Get all list names/ids for the user"""
    userId = userData[u'userId']
    lists = List.query.filter_by(userId=userId).all()
    listsArray = []
    for list in lists:
        listsArray.append({"name": list.name, "listId": list.id, "createdAt": str(list.createdAt)})
    return json.dumps({"status": "success", "data": {"lists": listsArray}}), 200
