## vision
:ski: users who rent or by skies can input there ski specs and get valuable insights on their equipment (compared to user height and weight). like suitable terrain, ski level etc...
the ski is saved securly so the user can reffer to older gear and compare both specs and insights.

## overveiw
- **Server:** using flask: api's (sign in ,register, user & ski CURD)    {flask-cors, flask-restx}
- **Auth:** JWT haddled completly on server side, the user password is saved hashed.    {Flask-Bcrypt, PyJWT, Flask-JWT-Extended}
- **DB** posgreSQL: Table structure feild types api in & outputs are all defined and changble in the "model" folder.(table versions are saved)  {SQLAlchemy, Flask-Migrate, alembic}
- **Insight logic:** using both ML and manual logic the produce insights. (the ML.pkl model is to big for github contact me if relevant)   {scikit-learn, pandas, numpy}
- **Container:** using docker-compose to build both python and DB enviroments.
- **Api testing:** Swagger for api's on the server side. (very usful, insted of postman)
- **Front:** using next.js, TypeScript saved in different repo - "/SkiApp_Front-Next.js"
### notes & usful commands
- Change JWT margin for security (app/main/util/config.py)
- Change DATABASE_URI to your db user,pass,port,etc.
```
# DB Commands:
only when connectind to a new DB. run: python manage.py db init
python manage.py db migrate --message"<MESSAGE>"  # checkout Data Base migrations after aplyed change.
python manage.py db upgrade  # Update (commit) to DB migrations.
# Docker Commands:
docker-compose up  # create & run a container.
docker-compose up -d  # Detached mode: Run containers in the background
docker-compose ps  # to see curently running containers.
docker-compose down  # stop container.
```
