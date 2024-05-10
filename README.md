# Calendar-project
Making a full project that interacts with google calendar api's to "Crud" events. Also have it to where you can share a link with someone and they can scheduele an event with you!


**Below are instruction on how to follow along** 

* first you want to fork the repo 
    * click on code ![alt text](<Screenshot 2024-05-10 at 9.08.14 AM.png>)

    * then click on ssh and copy the code 
    ![alt text](<Screenshot 2024-05-10 at 9.07.28 AM.png>)


* You should have some type of url copied 
**Next**
* Go to you terminal and enter this command where you want to have the files exist 
```Python
git clone git@github.com:Masterneo11/Calendar-project.git
```

* Go to the backend file and run this command in your terminal 

```Python
pip install -r requirements.txt
```
## **Installing google calendar Api**

* If you don't already have a google developer account and a project follow the link below
https://developers.google.com/calendar/api/quickstart/python
    * Use your email to create an account
    * Follow the tutorial

## Databases 
* I personally use Postgres and Pg admin
follow the link to use the same one 

* For pgadmin    https://www.pgadmin.org/download/pgadmin-4-macos/

* For postgres     https://postgresapp.com/downloads.html

    * I personally used the 16(Universal)
    
* in pgadmin you'll want to create a server if you don't already have one and in their create a database, I named mine schedueling to keep it simple. 

# alembic 

* technically speaking everything in alembic should be the same. If not then follow these commands 

create the first .ini
``` Python
alembic init alembic
```
next bash 
```Python
alembic -m revisions -m " create_table_"
```
## Starting localhost

* If your using VsCode you can go to the debugger run and debug and use fast api 

* If your  using the terminal bash 
```Python
uvicorn app.main:app
```
bash 
```Python
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```
* Go to google or safari and type in this url
http://localhost:8000/docs

# That is everything you need to do to get this running 
