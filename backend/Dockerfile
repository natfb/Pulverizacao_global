# Use the official Python runtime image
FROM python:3.13-slim  
 
# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
COPY requirements.txt  /app/
 
# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the Django project to the container
COPY . /app/
 
# Expose the Django port
EXPOSE 8000

# Copy the entrypoint.sh script and make it executable
# COPY ./entrypoint.sh /app/entrypoint.sh
# RUN sed -i 's/\r$//g' /app/entrypoint.sh
# RUN chmod +x /app/entrypoint.sh

# Copy the rest of the application files
#COPY . /app/

# Set the entrypoint script
#ENTRYPOINT ["/app/entrypoint.sh"]

# Run Django’s development server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["entrypoint.sh"]