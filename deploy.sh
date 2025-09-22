#!/bin/bash

echo "🚀 Deploying AIO Search Tool..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - AIO Search Tool"
fi

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Installing..."
    curl https://cli-assets.heroku.com/install.sh | sh
fi

# Create Heroku app if it doesn't exist
if ! heroku apps:info &> /dev/null; then
    echo "🌐 Creating Heroku app..."
    heroku create aio-search-tool-$(date +%s)
fi

# Deploy to Heroku
echo "📤 Deploying to Heroku..."
git add .
git commit -m "Deploy AIO Search Tool"
git push heroku main

# Open the app
echo "🌍 Opening deployed app..."
heroku open

echo "✅ Deployment complete!"
echo "🔗 Your app is now live at: $(heroku info -s | grep web_url | cut -d= -f2)" 