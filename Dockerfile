FROM python:3.11.13-bullseye

# set work directory
WORKDIR /app

# install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy source code
COPY . .

# expose port for flask
EXPOSE 8004

VOLUME ["/app/resources"]
CMD ["gunicorn", "-b", "0.0.0.0:8004",  "app:create_app()"]