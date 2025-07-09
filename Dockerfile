# Use official Python image
FROM python:3.12

# Set work directory
WORKDIR /app

# Copy all files into container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (adjust if your app uses a different port)
EXPOSE 8000

# Command to run your app
CMD ["sh", "run.sh"]
