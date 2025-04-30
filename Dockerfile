# Use Python 3.9 slim image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false \
    STREAMLIT_BROWSER_SERVER_ADDRESS=localhost \
    STREAMLIT_THEME_BASE=light \
    STREAMLIT_THEME_PRIMARY_COLOR=#2196F3 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200 \
    STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true \
    STREAMLIT_SERVER_ENABLE_SESSION_STATE=true \
    STREAMLIT_SERVER_MAX_MESSAGE_SIZE=200 \
    APP_VERSION=1.0.4

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    fonts-liberation \
    libappindicator1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Font Awesome
RUN mkdir -p /app/static/fontawesome && \
    wget -q https://use.fontawesome.com/releases/v5.15.4/fontawesome-free-5.15.4-web.zip -O /tmp/fontawesome.zip && \
    unzip /tmp/fontawesome.zip -d /tmp && \
    cp -r /tmp/fontawesome-free-5.15.4-web/css /app/static/fontawesome/ && \
    cp -r /tmp/fontawesome-free-5.15.4-web/webfonts /app/static/fontawesome/ && \
    rm -rf /tmp/fontawesome.zip /tmp/fontawesome-free-5.15.4-web

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p data .streamlit

# Create Streamlit config with enhanced settings
RUN echo "\
[server]\n\
port = 8501\n\
address = '0.0.0.0'\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
maxUploadSize = 200\n\
enableStaticServing = true\n\
enableSessionState = true\n\
maxMessageSize = 200\n\
\n\
[browser]\n\
serverAddress = 'localhost'\n\
gatherUsageStats = false\n\
\n\
[theme]\n\
base = 'light'\n\
primaryColor = '#2196F3'\n\
secondaryBackgroundColor = '#F0F2F6'\n\
textColor = '#262730'\n\
font = 'sans serif'\n\
\n\
[client]\n\
showErrorDetails = true\n\
toolbarMode = 'minimal'\n\
\n\
[runner]\n\
fastReruns = true\n\
\n\
[logger]\n\
level = 'info'\n\
messageFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'\n\
\n\
[global]\n\
developmentMode = false\n\
" > .streamlit/config.toml

# Copy the application code
COPY . .

# Add debug information
RUN echo "Debug: Version file exists: $(ls -la version.txt)" && \
    echo "Debug: App.py exists: $(ls -la app.py)" && \
    echo "Debug: App.py content (first 10 lines):" && \
    head -n 10 app.py

# Clear any cached files and set permissions
RUN rm -rf /root/.streamlit/ && \
    chmod -R 755 /app && \
    chown -R root:root /app

# Create cache directory for Streamlit
RUN mkdir -p /root/.streamlit/cache && \
    chmod -R 777 /root/.streamlit

# Expose the port Streamlit runs on
EXPOSE 8501

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Command to run the application with optimized settings
CMD ["streamlit", "run", "app.py", \
     "--server.runOnSave=true", \
     "--logger.level=info"] 