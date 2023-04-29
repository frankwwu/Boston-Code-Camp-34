FROM python:3.9.7

# Create a work directory called /app
WORKDIR /app

# Copy requirements.txt into the work directory
COPY ./requirements.txt /app/requirements.txt

# Install Python packages
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the code and model into work directory
COPY . /app/

EXPOSE 8000

# CMD launches the server when the container is started
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
