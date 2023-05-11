from typing import Union
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

import pyodbc  # pip install pyodbc

templates = Jinja2Templates(directory="templates_bill")
app = FastAPI()


def connect():
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=TLE\CSDLPTN1;'
                        'Database=manh2_shopee;'
                        'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [bill]')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return cursor


@app.get("/")
async def home(request: Request, cursor: pyodbc.Cursor = Depends(connect)):
    cursor.execute('SELECT * FROM [bill]')
    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "bills": rows})

@app.post("/add")
async def add(request: Request, id_customer: str = Form(...),id_product: str = Form(...),quantity: str = Form(...), cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"insert into [bill] (name, id_headquarter, phone_number, address) values  ('{bill_name}', '{id_headquarter}', '{phone_number}', '{address}');")
    # cursor.execute("SELECT SCOPE_IDENTITY()")
    # new_object_id = cursor.fetchone()[0]
    maxx = cursor.execute(f"SELECT MAX([id]) FROM [manh2_shopee].[dbo].[bill]").fetchall()[0][0]
    print(maxx)
    cursor.execute(f"insert into [bill] (id, id_customer, id_product, quantity) values  ( '{maxx+1}', '{id_customer}', '{id_product}', '{quantity}');")
    cursor.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})

@app.get("/edit/{bill_id}")
async def edit(request: Request, bill_id: int, cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"SELECT * FROM [bill] WHERE id = {bill_id}")
    cursor.execute(f"SELECT * FROM [bill] WHERE id = {bill_id}")
    bill = cursor.fetchall()
    print(bill[0])
    return templates.TemplateResponse("edit.html", {"request": request, "bill": bill[0]})

@app.post("/update/{bill_id}/{id_product_old}")
async def update(request: Request, bill_id: int,id_product_old: int, id_customer: str = Form(...),id_product: str = Form(...),quantity: str = Form(...),  cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"UPDATE [bill] SET name = '{bill_name}', id_headquarter = '{id_headquarter}', phone_number = '{phone_number}', address = '{address}' WHERE id = {bill_id}")
    cursor.execute(f"UPDATE [bill] SET  id_customer = '{id_customer}', id_product = '{id_product}', quantity = '{quantity}'  WHERE id = {bill_id} and id_product = {id_product_old}")
    # UPDATE [bill] SET  id_customer = '{id_customer}', id_product = '{id_product}', quantity = '{quantity}'  WHERE id = {bill_id} and id_product = (select top(1) [id_product]  FROM [bill] where id = {bill_id});
    cursor.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"DELETE FROM [bill] WHERE id = {user_id}")
    cursor.execute(f"DELETE FROM [bill] WHERE id = {user_id}")
    cursor.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/bills")
async def get_bills():
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=TLE;'
                        'Database=shopee;'
                        'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [bill]')
    rows = cursor.fetchall()
    bills = []
    for row in rows:
        bills.append({
            "bill_id": row[0],
            "bill_name": row[1],
            "id_headquarter": row[2],
            "phone_number": row[3],
            "address": row[4],
        })
    return {"bills": bills}