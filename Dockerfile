# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the code
COPY . .

# Expose port (if your app needs to listen, optional for Telegram bot)
EXPOSE 8080

# Command to run the bot
CMD ["python", "bot.py"]
