# Calendar-project
Making a full project that interacts with google calendar api's to "Crud" events. Also have it to where you can share a link with someone and they can scheduele an event with you!


**Below are instruction on how to follow along** 

* first you want to clone the repo
    * then click on ssh and copy the code 
    ![alt text](<images_for_readme/github_cloneurl.png>)


* You should have some type of url copied 
**Next**
* Go to you terminal and enter this command where you want to have the files exist 
```bash
git clone git@github.com:Masterneo11/Calendar-project.git
```

* Go to the backend file and run this command in your terminal 
* Create a virutual environment
```bash
python -m venv .venv
source .venv/bin/activate
```
 * Now install dependencies
```bash
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

### alembic 

```bash
alembic upgrade head
```
## Starting localhost

* If your using VsCode you can go to the debugger run and debug and use fast api 

* If your  using the terminal bash 
```bash
uvicorn app.main:app
```
bash 
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```
* Go to google or safari and type in this url
http://localhost:8000/docs

# That is everything you need to do to get this running 
