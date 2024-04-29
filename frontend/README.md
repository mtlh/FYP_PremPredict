# PremPredict - Frontend

### Environment Variables
Add the following to a .env file.
```sh
DATABASE_URL='' # Your database connection string
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
** Please ensure you are located in the frontend folder

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
#### Run all
```shell
python manage.py test ./prempredict/tests/ 
```
#### Models
```shell
python manage.py test ./prempredict/tests/model
```
#### URLs
```shell
python manage.py test ./prempredict/tests/url
```
#### Functions
```shell
python manage.py test ./prempredict/tests/function
```
