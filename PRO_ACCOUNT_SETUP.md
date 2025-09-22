# Pro Account Setup Guide for AI Visibility Checker

This guide explains how to configure the AI Visibility Checker to work with pro versions of ChatGPT, Claude, and Perplexity for enhanced functionality and better results.

## 🔐 Setting Up Pro Account Credentials

### 1. Create Environment File

Create a `.env` file in your project root directory with the following content:

```bash
# Airtop Configuration
AIRTOP_API_KEY=your_airtop_key_here

# LLM Platform Credentials (for Pro versions)
LLM_EMAIL=your_email@example.com
LLM_PASSWORD=your_password_here

# Browser Automation Settings
AIRTOP_HEADLESS=false
AIRTOP_TIMEOUT=300

# Optional: Platform-specific credentials (if different accounts)
CHATGPT_EMAIL=your_chatgpt_email@example.com
CHATGPT_PASSWORD=your_chatgpt_password
CLAUDE_EMAIL=your_claude_email@example.com
CLAUDE_PASSWORD=your_claude_password
PERPLEXITY_EMAIL=your_perplexity_email@example.com
PERPLEXITY_PASSWORD=your_perplexity_password
```

### 2. Pro Account Requirements

#### ChatGPT Plus/Pro
- **URL**: https://chat.openai.com/
- **Features**: Web browsing, GPT-4, longer conversations
- **Benefits**: Better search results, more comprehensive responses
- **Cost**: $20/month

#### Claude Pro
- **URL**: https://claude.ai/
- **Features**: Web search, Claude 3.5 Sonnet, file uploads
- **Benefits**: Enhanced reasoning, better source citations
- **Cost**: $20/month

#### Perplexity Pro
- **URL**: https://www.perplexity.ai/
- **Features**: Unlimited searches, focus modes, file uploads
- **Benefits**: More detailed research, better source tracking
- **Cost**: $20/month

## 🚀 Running with Pro Accounts

### Method 1: Using the Test Script

```bash
python test_airtop_visibility.py
```

This will automatically detect your credentials and authenticate with all platforms.

### Method 2: Using the Main Simulator

```python
from airtop_llm_simulator import AirtopLLMSimulator
import asyncio
import os

async def run_pro_visibility_check():
    # Initialize simulator
    simulator = AirtopLLMSimulator()
    await simulator.initialize()
    
    # Authenticate with pro platforms
    credentials = {
        'email': os.getenv('LLM_EMAIL'),
        'password': os.getenv('LLM_PASSWORD')
    }
    
    # Authenticate with each platform
    platforms = ['chatgpt', 'claude', 'perplexity']
    authenticated_platforms = []
    
    for platform in platforms:
        print(f"🔐 Authenticating with {platform}...")
        success = await simulator.authenticate_platform(platform, credentials)
        if success:
            authenticated_platforms.append(platform)
            print(f"✅ Successfully authenticated with {platform}")
        else:
            print(f"❌ Failed to authenticate with {platform}")
    
    # Run visibility check with pro features
    results = await simulator.check_brand_visibility(
        brand_name="Your Brand",
        competitors=["Competitor 1", "Competitor 2"],
        prompts=[
            "What are the best AI tools for content optimization?",
            "Compare our brand vs competitors",
            "What AI solutions are trending in our industry?"
        ],
        platforms=authenticated_platforms
    )
    
    # Save results
    results.to_csv('pro_visibility_results.csv', index=False)
    print("✅ Pro visibility check completed!")
    
    await simulator.cleanup()

# Run the check
asyncio.run(run_pro_visibility_check())
```

### Method 3: Using the Web API

```bash
curl -X POST "http://localhost:8000/api/visibility/check" \
  -H "Content-Type: application/json" \
  -d '{
    "brand_name": "Your Brand",
    "competitors": ["Competitor 1", "Competitor 2"],
    "platforms": ["chatgpt", "claude", "perplexity"],
    "use_pro_accounts": true
  }'
```

## 🔧 Configuration Options

### Platform-Specific Settings

The system supports different configurations for each platform:

#### ChatGPT Pro
- **Web Browsing**: Enabled by default
- **Model**: GPT-4 with browsing
- **Rate Limit**: 20 requests/minute
- **Session Timeout**: 60 minutes

#### Claude Pro
- **Web Search**: Enabled by default
- **Model**: Claude 3.5 Sonnet
- **Rate Limit**: 15 requests/minute
- **Session Timeout**: 60 minutes

#### Perplexity Pro
- **Focus Modes**: Available (Academic, Writing, etc.)
- **Unlimited Searches**: Yes
- **Rate Limit**: 30 requests/minute
- **Session Timeout**: 30 minutes

### Customizing Selectors

If the login process fails, you may need to update the selectors in `airtop_config.json`:

```json
{
  "platforms": {
    "chatgpt": {
      "selectors": {
        "login_button": "button[data-testid='login-button']",
        "email_input": "input[name='username']",
        "password_input": "input[name='password']",
        "continue_button": "button[type='submit']"
      }
    }
  }
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check your credentials in `.env`
   - Ensure you have active pro subscriptions
   - Try logging in manually first

2. **Rate Limiting**
   - Pro accounts have higher rate limits
   - Check the rate limit settings in configuration

3. **Session Timeouts**
   - Pro accounts have longer session times
   - Sessions are automatically refreshed

4. **Web Search Not Working**
   - Ensure you have pro accounts with web search enabled
   - Check if web search is enabled in your account settings

### Debug Mode

Enable debug logging by setting the log level in `airtop_config.json`:

```json
{
  "logging": {
    "level": "DEBUG",
    "file": "airtop_simulator.log"
  }
}
```

## 📊 Pro vs Free Comparison

| Feature | Free Version | Pro Version |
|---------|-------------|-------------|
| Web Search | Limited | Unlimited |
| Response Quality | Basic | Enhanced |
| Rate Limits | Low | High |
| Session Time | Short | Extended |
| Model Access | Basic | Advanced |
| File Uploads | No | Yes |

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Use strong, unique passwords for each platform
- Consider using environment variables in production
- Regularly rotate your credentials

## 📈 Expected Improvements with Pro Accounts

1. **Better Search Results**: Pro accounts access more comprehensive web search
2. **Enhanced Responses**: Higher quality AI models provide better insights
3. **More Citations**: Better source tracking and citation extraction
4. **Longer Conversations**: Extended context for complex queries
5. **Faster Processing**: Higher rate limits for quicker results

## 🎯 Next Steps

1. Set up your `.env` file with pro credentials
2. Test authentication with each platform
3. Run a visibility check to verify pro features
4. Monitor results for improved quality and depth
5. Adjust configuration as needed for your use case 