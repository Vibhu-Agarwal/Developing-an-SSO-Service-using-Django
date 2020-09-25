# Single-Sign-On

## Set-Up the Repository
```
$ cd Single-Sign-On/
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
```

## Set Environment Variables

#### Superuser Password
```
VIGA_HOST_PASSWORD="..."
```
#### Database Configuration
```
USE_FILE_BASED_DB=1
```
**OR**
```
DATABASE_NAME="..."
DATABASE_USERNAME="..."
DATABASE_PASSWORD="..."
DATABASE_HOST="..."
DATABASE_PORT="..."
```

### Apply Migrations
```
$ source venv/bin/activate
(venv)$ cd src/
(venv)$ python manage.py migrate
```

### Create the Admin
```
(venv)$ cd src/
(venv)$ python manage.py viga_setup
```

## Running-Up Server
```
$ source venv/bin/activate
(venv)$ cd src/
(venv)$ python manage.py runserver
```

## Integrating a `Service`
### Step 1
- Create a Service
### Step 2
- Reserve a `callback_url` which receives **`POST`** request
- The `callback_url` will receive User-Profile Data as fields specified in **[UserSerializer](./src/users/serializers.py)**
- This `callback_url` will be hit on two triggers: 1) `Service` Creation 2) `Connection` Creation
- On Service Creation, it will receive SSO-Admin Details (which will be used to authenticate any requests from the SSO in future)
- On Connection Creation, it will receive the User's details which got connected to the service
### Step 3
- Hit [the URL](./src/services/urls.py) for Service Creation
