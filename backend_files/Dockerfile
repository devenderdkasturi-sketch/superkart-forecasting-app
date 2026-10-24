# Step 1: Secure official lightweight base image configuration blueprint
FROM python:3.10-slim

# Step 2: Establish isolated application runtime environment pathing boundaries
WORKDIR /app

# Step 3: Inject package dependency limits ahead of heavy dataset layers
COPY requirements.txt .

# Step 4: Execute infrastructure compilation blocks and optimize python binaries cache
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the frozen estimator pipeline and API logic arrays into app workspace
COPY app.py .
COPY superkart_model.joblib .

# Step 6: Expose localized container communication port interface handles
EXPOSE 7860

# Step 7: Launch application loop backend listener process routine on initialization
CMD ["python", "app.py"]