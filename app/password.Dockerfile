FROM python:3.7

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY password_generator/ /password_generator

EXPOSE 8080

# runs the production server
ENTRYPOINT ["python", "password_generator/manage.py"]
CMD ["runserver", "0.0.0.0:8080"]