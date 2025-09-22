#!/usr/bin/env python3
"""
Test script for Pro Account Authentication
Tests login to ChatGPT, Claude, and Perplexity pro accounts
"""

import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from airtop_llm_simulator import AirtopLLMSimulator

async def test_pro_authentication():
    """Test authentication with pro accounts"""
    print("🔐 Testing Pro Account Authentication")
    print("=" * 50)
    
    # Check if credentials are available
    email = os.getenv('LLM_EMAIL')
    password = os.getenv('LLM_PASSWORD')
    
    if not email or not password:
        print("❌ Credentials not found!")
        print("   Please add LLM_EMAIL and LLM_PASSWORD to your .env file")
        print("\nExample .env file:")
        print("LLM_EMAIL=your_email@example.com")
        print("LLM_PASSWORD=your_password")
        return False
    
    print(f"✅ Found credentials for: {email}")
    
    # Initialize simulator
    print("\n🚀 Initializing browser simulator...")
    simulator = AirtopLLMSimulator()
    
    try:
        await simulator.initialize()
        print("✅ Browser initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize browser: {e}")
        return False
    
    # Test platforms
    platforms = ['chatgpt', 'claude', 'perplexity']
    credentials = {'email': email, 'password': password}
    
    authenticated_platforms = []
    
    for platform in platforms:
        print(f"\n🔐 Testing {platform.upper()} authentication...")
        
        try:
            success = await simulator.authenticate_platform(platform, credentials)
            
            if success:
                authenticated_platforms.append(platform)
                print(f"✅ Successfully authenticated with {platform}")
                
                # Test a simple query
                print(f"   Testing query on {platform}...")
                test_result = await simulator.simulate_query(
                    platform, 
                    "What are the best AI tools for content optimization?", 
                    enable_web_search=True
                )
                
                if test_result.success:
                    print(f"   ✅ Query successful! Response time: {test_result.response_time:.2f}s")
                    print(f"   📝 Response preview: {test_result.response[:100]}...")
                else:
                    print(f"   ⚠️ Query failed: {test_result.error_message}")
                    
            else:
                print(f"❌ Failed to authenticate with {platform}")
                
        except Exception as e:
            print(f"❌ Error testing {platform}: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 AUTHENTICATION SUMMARY")
    print("=" * 50)
    
    if authenticated_platforms:
        print(f"✅ Successfully authenticated with {len(authenticated_platforms)} platforms:")
        for platform in authenticated_platforms:
            print(f"   - {platform.upper()}")
        
        print(f"\n🎯 Ready to run visibility checks on: {', '.join(authenticated_platforms)}")
        
        # Test visibility check
        print("\n🧪 Testing brand visibility check...")
        try:
            results = await simulator.check_brand_visibility(
                brand_name="AIO Search",
                competitors=["Clearscope", "MarketMuse", "Surfer SEO"],
                prompts=[
                    "What are the best AI content optimization tools?",
                    "Compare AI tools for SEO content"
                ],
                platforms=authenticated_platforms
            )
            
            print(f"✅ Visibility check completed!")
            print(f"📊 Results: {len(results)} queries processed")
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pro_test_results_{timestamp}.csv"
            results.to_csv(filename, index=False)
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Visibility check failed: {e}")
    
    else:
        print("❌ No platforms authenticated successfully")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your credentials in .env file")
        print("2. Ensure you have active pro subscriptions")
        print("3. Try logging in manually to each platform first")
        print("4. Check if 2FA is enabled (may need to disable temporarily)")
        print("5. Verify your internet connection")
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    await simulator.cleanup()
    print("✅ Cleanup completed")
    
    return len(authenticated_platforms) > 0

async def test_single_platform(platform_name: str):
    """Test a single platform"""
    print(f"🔐 Testing {platform_name.upper()} only...")
    
    email = os.getenv('LLM_EMAIL')
    password = os.getenv('LLM_PASSWORD')
    
    if not email or not password:
        print("❌ Credentials not found in .env file")
        return False
    
    simulator = AirtopLLMSimulator()
    await simulator.initialize()
    
    credentials = {'email': email, 'password': password}
    
    try:
        success = await simulator.authenticate_platform(platform_name, credentials)
        
        if success:
            print(f"✅ Successfully authenticated with {platform_name}")
            
            # Test a query
            result = await simulator.simulate_query(
                platform_name,
                "What are the best AI tools for content optimization?",
                enable_web_search=True
            )
            
            if result.success:
                print(f"✅ Query successful!")
                print(f"📝 Response: {result.response[:200]}...")
                print(f"⏱️ Response time: {result.response_time:.2f}s")
            else:
                print(f"❌ Query failed: {result.error_message}")
        else:
            print(f"❌ Failed to authenticate with {platform_name}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await simulator.cleanup()
    
    return success

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test pro account authentication")
    parser.add_argument("--platform", choices=["chatgpt", "claude", "perplexity"], 
                       help="Test a single platform")
    
    args = parser.parse_args()
    
    if args.platform:
        success = asyncio.run(test_single_platform(args.platform))
    else:
        success = asyncio.run(test_pro_authentication())
    
    if success:
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main() 