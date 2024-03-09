# Setup

## Client

1. Have node version 18 installed
2. Install dependencies with `npm install`
3. Run the client with `npm run dev`

## Server

1. Have python3 installed
2. Be sure to activate the virtual env
3. Install dependencies from requirements.txt using pip
4. Run the server with `python manage.py runserver`

## Database

1. Install PostgreSQL
2. Create a database
3. Create a user
4. Change the connection string for the server in `server/src/src/.pgpass`
5. Be sure to run the migrations from the server `python manage.py migrate` from `server/src`
6. Populate the database with the provided csv files

## Application setup

1. You will need to have both the server, client, and database runnig before attempting to use the application
2. On the client app you will need to create an account
3. There is already data for each user up to user id 610
4. You will need to login to the created account
5. You can view what ratings there are for that user id and rate recommendations
6. You can get new recommendations when you rate more for that user id
