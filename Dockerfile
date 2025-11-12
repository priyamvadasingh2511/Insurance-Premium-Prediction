#base image
FROM python:3.11-slim

#workdir
WORKDIR /app

#copy the files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of application code
COPY . .

#port
EXPOSE 8080

#command to run app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


