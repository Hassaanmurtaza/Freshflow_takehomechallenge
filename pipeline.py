import json
import os
import argparse
#from pathlib import Path
from time import time as time1
import time
import shutil
import pandas as pd
# from sqlalchemy import create_engine
import sqlite3
import pandas as pd
# Create your connection.

import flask
from flask import request, jsonify


def main():

    

    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    cnx = sqlite3.connect('data.db')
    df = pd.read_sql_query('''select orderable_items.item_number, orderable_items.ordering_day, orderable_items.delivery_day,
orderable_items.suggested_retail_price as sales_price_suggestion, orderable_items.profit_margin, 
orderable_items.purchase_price, orderable_items.item_categories, orderable_items.tags as labels, orderable_items.case_content_quantity as 'case.quantity',
 orderable_items.case_content_unit as 'case.unit',
CAST(((sales_predictions.sales_quantity-inventory.inventory) / orderable_items.case_content_quantity) as int) as 'order.quantity', 
 order_intake.unit as 'order.unit', inventory.inventory as 'inventory.quantity', order_intake.unit as 'inventory.unit'
from orderable_items left join inventory on orderable_items.item_number=inventory.item_number and orderable_items.ordering_day=strftime('%Y-%m-%d', inventory.day)
 left join (select item_number,day,sum(sales_quantity) as sales_quantity  from sales_predictions group by 1,2 ) sales_predictions
 on orderable_items.item_number=sales_predictions.item_number and orderable_items.delivery_day=strftime('%Y-%m-%d', sales_predictions.day)
 left join order_intake on orderable_items.item_number=order_intake.item_number and orderable_items.delivery_day=order_intake.day
 ''', cnx)

    json_dict=df.to_dict('records')

    @app.route('/', methods=['GET'])
    def home():
        return json_dict

    app.run()
    
if __name__ == '__main__':

    main()