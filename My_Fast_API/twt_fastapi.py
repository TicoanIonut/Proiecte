import json
from  typing import Optional
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
	name: str
	price: int
	brand: Optional[str] = None


class UpdateItem(BaseModel):
	name: Optional[str] = None
	price: Optional[int] = None
	brand: Optional[str] = None


inventory = {}


@app.get('/')
def home():
	return {'Data': 'Testing'}


@app.get('/about')
def about():
	return {"Data": 'About'}


@app.get('/get-item/{p_id}')
def get_item(p_id: int = Path(description="The id of the person you like", gt=0, lt=99)):
	return inventory[p_id]


@app.get('/get-by-name/{item_id}')
def get_item(*, item_id: int, name: Optional[str] = None, test: int):
	for item_id in inventory:
		if inventory[item_id].name == name:
			return inventory[item_id]
		return {'Data': 'not found'}


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
	if item_id in inventory:
		return {"Error": "Item id exists"}
	inventory[item_id] = item
	return inventory[item_id]


@app.put('/update-item/{item_id}')
def update_item(item_id: int, item: Item):
	if item_id not in inventory:
		return {'Error': 'item id does not exist'}
	if item.name != None:
		inventory[item_id].name = item.name
	if item.price != None:
		inventory[item_id].price = item.price
	if item.brand != None:
		inventory[item_id].brand = item.brand
	return inventory[item_id]


@app.delete('/delete-item')
def delete_item(item_id: int = Query(..., description='The id of the item do delete')):
	if item_id not in inventory:
		return {'Errorr': 'Id does not exist'}
	del inventory[item_id]
	return {'success': 'Item deleted'}