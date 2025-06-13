FROM python:3.11.13-bullseye

# set work directory
WORKDIR /app

# install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy source code
COPY . .

# expose port for flask
EXPOSE 5000

VOLUME ["/app/resources"]
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]