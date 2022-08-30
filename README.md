# Blogr Overview
## Functionality
### Users should be able to make and edit publicly viewable blog posts within a login session using the following functionalities...

- Create and login to a custom profile
- View their own posts
- Create new posts
- Edit existing posts
- View other users' posts 
- Logout of a session

___
## Creating a Development Environment
### Languages and framework used

1. Html
2. CSS
3. Javascript
4. Micro-framework (Flask)
5. sqlite

List of libraries can be found in requirements.txt <br>

Create a **virtual enviournment** to install dependancies on <br>

```
python -m venv env
```
Activate virtual environment
```
source ./env/Scripts/activate
```

Installing dependancies... <br>

```
pip -r requirements.txt
```
Create new database (if neccessary). In python, <br>
```
import db from app
```
```
db.create_all()
```
Start server. <br>
```
python app.py
```
Copy the address in terminal to the browser










