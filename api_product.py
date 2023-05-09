from typing import Union
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

import pyodbc  # pip install pyodbc

templates = Jinja2Templates(directory="templates_product")
app = FastAPI()

def connect():
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=TLE;'
                        'Database=shopee;'
                        'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [shopee].[dbo].[product]')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return cursor


@app.get("/")
async def home(request: Request, cursor: pyodbc.Cursor = Depends(connect)):
    cursor.execute('SELECT * FROM [shopee].[dbo].[product]')
    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "products": rows})

@app.post("/add")
async def add(request: Request, product_name: str = Form(...), id_provider: str = Form(...), quantity: str = Form(...), price: str = Form(...), cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"insert into [product] (name, id_headquarter, phone_number, address) values  ('{product_name}', '{id_headquarter}', '{phone_number}', '{address}');")
    cursor.execute(f"insert into [product] (name, id_provider, quantity, price) values  ('{product_name}', '{id_provider}', '{quantity}', '{price}');")
    cursor.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})

@app.get("/edit/{product_id}")
async def edit(request: Request, product_id: int, cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"SELECT * FROM [shopee].[dbo].[product] WHERE id = {product_id}")
    cursor.execute(f"SELECT * FROM [shopee].[dbo].[product] WHERE id = {product_id}")
    product = cursor.fetchall()
    print(product[0])
    return templates.TemplateResponse("edit.html", {"request": request, "product": product[0]})

@app.post("/update/{product_id}")
async def update(request: Request, product_id: int, product_name: str = Form(...), id_provider: str = Form(...), quantity: str = Form(...), price: str = Form(...), cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"UPDATE [shopee].[dbo].[product] SET name = '{product_name}', id_headquarter = '{id_headquarter}', phone_number = '{phone_number}', address = '{address}' WHERE id = {product_id}")
    cursor.execute(f"UPDATE [shopee].[dbo].[product] SET name = '{product_name}', id_provider = '{id_provider}', quantity = '{quantity}', price = '{price}' WHERE id = {product_id}")
    cursor.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"DELETE FROM [shopee].[dbo].[product] WHERE id = {user_id}")
    cursor.execute(f"DELETE FROM [shopee].[dbo].[product] WHERE id = {user_id}")
    cursor.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/products")
async def get_products():
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=TLE;'
                        'Database=shopee;'
                        'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [shopee].[dbo].[product]')
    rows = cursor.fetchall()
    products = []
    for row in rows:
        products.append({
            "product_id": row[0],
            "product_name": row[1],
            "id_provider": row[2],
            "quantity": row[3],
            "price": row[4],
        })
    return {"products": products}