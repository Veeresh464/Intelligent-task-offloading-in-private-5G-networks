FROM manojpandekamat/fastapi-application
# FROM python:3.11-slim


# # Set working directory
WORKDIR /app

# # Copy requirements (assuming you have a requirements.txt)
COPY requirements.txt .
COPY cnn_model_converted.h5 .
COPY server.py .

# # Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# # Copy app code
RUN pip install python-multipart


# # # Expose port
EXPOSE 8000

# # # Run the app with uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
# # /**********************************
