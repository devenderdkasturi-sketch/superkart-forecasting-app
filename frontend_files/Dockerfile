# Step 1: Secure official lightweight base image configuration blueprint
FROM python:3.10-slim

# Step 2: Establish isolated application runtime environment pathing boundaries
WORKDIR /app

# Step 3: Inject package dependency limits ahead of heavy app logic blocks
COPY requirements.txt .

# Step 4: Execute infrastructure compilation blocks and clear runtime binary caches
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the Streamlit view component application logic into workspace
COPY app_frontend.py .

# Step 6: Expose standard localized web communication port interface handles
EXPOSE 8501

# Step 7: Launch application loop client server dashboard on initialization
ENTRYPOINT ["streamlit", "run", "app_frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]