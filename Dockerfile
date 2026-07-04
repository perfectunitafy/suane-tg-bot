FROM python:3.12-slim
WORKDIR /app
RUN pip install --upgrade pip
# Удаляем всё, что может конфликтовать
RUN pip uninstall -y google-generativeai google-cloud-aiplatform
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
