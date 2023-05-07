from typing import Union
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

import pyodbc  # pip install pyodbc

templates = Jinja2Templates(directory="templates")
app = FastAPI()

def connect():
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=TLE;'
                        'Database=shopee;'
                        'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [shopee].[dbo].[customer]')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return cursor


@app.get("/")
async def home(request: Request, cursor: pyodbc.Cursor = Depends(connect)):
    cursor.execute('SELECT * FROM [shopee].[dbo].[customer]')
    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "customers": rows})

@app.post("/add")
async def add(request: Request, customer_name: str = Form(...), id_headquarter: str = Form(...), phone_number: str = Form(...), address: str = Form(...), cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"insert into [customer] (name, id_headquarter, phone_number, address) values  ('{customer_name}', '{id_headquarter}', '{phone_number}', '{address}');")
    cursor.execute(f"insert into [customer] (name, id_headquarter, phone_number, address) values  ('{customer_name}', '{id_headquarter}', '{phone_number}', '{address}');")
    cursor.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})

@app.get("/edit/{customer_id}")
async def edit(request: Request, customer_id: int, cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"SELECT * FROM [shopee].[dbo].[customer] WHERE id = {customer_id}")
    cursor.execute(f"SELECT * FROM [shopee].[dbo].[customer] WHERE id = {customer_id}")
    customer = cursor.fetchall()
    print(customer[0])
    return templates.TemplateResponse("edit.html", {"request": request, "customer": customer[0]})

@app.post("/update/{customer_id}")
async def update(request: Request, customer_id: int, customer_name: str = Form(...), id_headquarter: str = Form(...), phone_number: str = Form(...), address: str = Form(...), cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"UPDATE [shopee].[dbo].[customer] SET name = '{customer_name}', id_headquarter = '{id_headquarter}', phone_number = '{phone_number}', address = '{address}' WHERE id = {customer_id}")
    cursor.execute(f"UPDATE [shopee].[dbo].[customer] SET name = '{customer_name}', id_headquarter = '{id_headquarter}', phone_number = '{phone_number}', address = '{address}' WHERE id = {customer_id}")
    cursor.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"DELETE FROM [shopee].[dbo].[customer] WHERE id = {user_id}")
    cursor.execute(f"DELETE FROM [shopee].[dbo].[customer] WHERE id = {user_id}")
    cursor.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/customers")
async def get_customers():
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=TLE;'
                        'Database=shopee;'
                        'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [shopee].[dbo].[customer]')
    rows = cursor.fetchall()
    customers = []
    for row in rows:
        customers.append({
            "customer_id": row[0],
            "customer_name": row[1],
            "id_headquarter": row[2],
            "phone_number": row[3],
            "address": row[4],
        })
    return {"customers": customers}