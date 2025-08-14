
FROM python:3.11.12-slim

# # Set working directory
WORKDIR /app


# # Install dependencies with exact versions
RUN pip install \
    numpy==2.0.2 \
    pandas==2.2.2 \
    tensorflow==2.18.0 \
    scikit-learn
    
RUN pip install fastapi uvicorn python-multipart


# # Copy your application code to the container
COPY . /app

# # Expose port (default uvicorn port)
EXPOSE 5001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]