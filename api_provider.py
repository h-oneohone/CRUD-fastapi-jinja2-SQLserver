from typing import Union
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

import pyodbc  # pip install pyodbc

templates = Jinja2Templates(directory="templates_provider")
app = FastAPI()

def connect():
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=TLE;'
                        'Database=shopee;'
                        'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [shopee].[dbo].[provider]')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return cursor


@app.get("/")
async def home(request: Request, cursor: pyodbc.Cursor = Depends(connect)):
    cursor.execute('SELECT * FROM [shopee].[dbo].[provider]')
    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "providers": rows})

@app.post("/add")
async def add(request: Request, provider_name: str = Form(...), phone_number: str = Form(...), cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"insert into [provider] (name, id_headquarter, phone_number, address) values  ('{provider_name}', '{id_headquarter}', '{phone_number}', '{address}');")
    cursor.execute(f"insert into [provider] (name, id_headquarter, phone_number) values  ('{provider_name}', '{1}', '{phone_number}');")
    cursor.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})

@app.get("/edit/{provider_id}")
async def edit(request: Request, provider_id: int, cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"SELECT * FROM [shopee].[dbo].[provider] WHERE id = {provider_id}")
    cursor.execute(f"SELECT * FROM [shopee].[dbo].[provider] WHERE id = {provider_id}")
    provider = cursor.fetchall()
    print(provider[0])
    return templates.TemplateResponse("edit.html", {"request": request, "provider": provider[0]})

@app.post("/update/{provider_id}")
async def update(request: Request, provider_id: int, provider_name: str = Form(...), phone_number: str = Form(...),cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"UPDATE [shopee].[dbo].[provider] SET name = '{provider_name}', id_headquarter = '{id_headquarter}', phone_number = '{phone_number}', address = '{address}' WHERE id = {provider_id}")
    cursor.execute(f"UPDATE [shopee].[dbo].[provider] SET name = '{provider_name}', id_headquarter = '{1}', phone_number = '{phone_number}' WHERE id = {provider_id}")
    cursor.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, cursor: pyodbc.Cursor = Depends(connect)):
    # print(f"DELETE FROM [shopee].[dbo].[provider] WHERE id = {user_id}")
    cursor.execute(f"DELETE FROM [shopee].[dbo].[provider] WHERE id = {user_id}")
    cursor.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/providers")
async def get_providers():
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=TLE;'
                        'Database=shopee;'
                        'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [shopee].[dbo].[provider]')
    rows = cursor.fetchall()
    providers = []
    for row in rows:
        providers.append({
            "provider_id": row[0],
            "provider_name": row[1],
            "id_headquarter": row[2],
            "phone_number": row[3],
            "address": row[4],
        })
    return {"providers": providers}