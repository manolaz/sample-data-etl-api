from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

# LOAD Folder PATH
dirname = os.path.dirname(__file__)
# LOAD DATA FILE from relative PATH
file_path = os.path.join(dirname, "data/20190207_transactions.txt")

# init list of transaction
my_list = []

# open file
with open(file_path) as f:
    # the data are LINEs delimited, so read one by one
    for line in f:
        # read JSON data
        j_content = json.loads(line)
        # loading list of transaction
        my_list.append(j_content)

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/freq/")
def count_frequency():
    # Creating an empty dictionary
    count = {}
    for trans in my_list:
        for item in trans.get('products'):
            # print(item)
            count[item] = count.get(item, 0) + 1
    return count


@app.get("/freq/{item_id}")
def count_item_frequency(item_id: int):
    count = {}
    for trans in my_list:
        for item in trans.get('products'):
            if item == item_id:
                count[item] = count.get(item, 0) + 1
    return count
