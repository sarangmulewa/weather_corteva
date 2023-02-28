# Code Challenge Template

# Frameworks

- Django
- Django Rest Framework

# Database

- SQLite
  <br>

# Prerequisites

The following prerequisites are required to use this API:

```
Python (3.7 or higher)
Virtualenv
SQLite (or PostgreSQL if deploying to AWS)
AWS account (if deploying to AWS)
```

# Structure

- wx_data - Weather data (txt files)
- src - Source Code (python)
- answers - debug.log (debug logs)

# Steps to run the program

- Create and run the virtual environment using commands: <br>

  ```bash
  pip3 install virtualenv
  virtualenv env
  ```

  To activate virtual environment :

  ```bash
  env/Scripts/activate (in Windows)
  source env/bin/activate (in Linux and Mac)
  ```

- Install all the requirements using command <br>

```bash
  pip3 install -r requirements.txt
```

- Navigate to “src” directory using command cd in terminal

- Migrate the models: <br>

```bash
  python src/manage.py makemigrations
  python src/manage.py migrate
```

- Ingesting the data:<br>

```bash
    python src/manage.py ingest wx_data_directory_path
```

- Run the python server using command: <br>

```bash
  python src/manage.py runserver
```

- And other functionalities can be accessed through these API links: <br>
  http://127.0.0.1:8000/swagger/<br>
  http://127.0.0.1:8000/api/weather<br>
  http://127.0.0.1:8000/api/weather/stats/

- With query params it can also be accessed such as : <br>
  http://127.0.0.1:8000/api/weather/?date=20100202
  http://127.0.0.1:8000/api/weather/?station__name=USC00257715
  http://127.0.0.1:8000/api/weather/?station__name=USC00257715&date=20100202
  <br><br>

# Tests

```bash
  cd src
  python manage.py test
```

# AWS Deployment

### Deploy Django API:

To deploy the Django API and database on AWS:

1. Use AWS Elastic Beanstalk to deploy and run the web application.
2. Configure a load balancer to handle incoming traffic and distribute it to multiple instances of the Django application.
3. Use Amazon RDS to host a PostgreSQL database. Configure database access in Django to securely connect to the RDS instance.
4. Use AWS S3 to store text files.
5. Store the ingested data in the RDS database.

### Conclusion

- This approach provides a scalable, secure, and easily managed deployment of the Django API, database, and data ingestion code

- The load balancer and auto-scaling features of AWS Elastic Beanstalk and Amazon RDS ensure that the API and database can handle changing levels of traffic.
