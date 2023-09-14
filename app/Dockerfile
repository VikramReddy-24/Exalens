# Use an official Python runtime as a parent image
FROM python:3.8

RUN apt-get update && apt-get install -y supervisor

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

CMD ["supervisord", "-c", "supervisor.conf"]


# # Run app.py when the container launches
# CMD ["python", "main.py"]