# PremPredict - Frontend

### Environment Variables
Add the following to a .env file.
```sh
DATABASE_URL='' # Your database connection string (from cockroachDB)
FBAPI_KEY='' # Football-data ApiKey 
BASE_URL='http://127.0.0.1:8000/' # URL of local/production index route
SECRET_KEY='' # A random string, generate one yourself
DEBUG='TRUE' # False in productions
MJ_APIKEY_PRIVATE='' # MailJet private ApiKey
MJ_APIKEY_PUBLIC='' # MailJet public ApiKey
ADMIN_USERNAME='' # Admin login username
ADMIN_EMAIL='' # Admin email
ADMIN_PASSWORD='' # Admin password
```

## Commands

- Please ensure you are located in the "frontend" folder and the virtual environment is activated before running any of the commands below.

### Update Tailwindcss
#### Tailwind Update
```shell
npx tailwindcss -i prempredict/static/css/main.css -o prempredict/static/css/tailwind.css --watch
```
#### Tailwind Minify
```shell
npx tailwindcss -o ./prempredict/static/css/tailwind.css --minify
```

### Commit Tailwind + Static files
#### Django Collectstatic
```shell
python manage.py collectstatic
```

### Manage Migrations
#### Django Make Migration
```shell
python manage.py makemigrations 
```
#### Django Migrate
```shell
python manage.py migrate
```

### PIP 
#### Install 
```shell
pip install ____
```
#### Uninstall  
```shell
pip uninstall ____
```
#### Freeze to requirements.txt
```shell
pip freeze > requirements.txt
```

### Deployment 
#### Production
```shell
vercel --prod
```
#### Local  
```shell
python manage.py runserver
```

### Tests 

-  If tests fail due to "Error loading bootstrap-static route" please update the fantasy_headers variable with a new user agent within /views/load/load_api_season_competition.py file.

#### Run all
```shell
python manage.py test ./prempredict/tests/ 
```
#### Models
```shell
python manage.py test ./prempredict/tests/models
```
#### Templates Routes
```shell
python manage.py test ./prempredict/tests/template-routes
```
#### Functions
```shell
python manage.py test ./prempredict/tests/functions
```
#### Api Routes
```shell
python manage.py test ./prempredict/tests/api-routes
```
