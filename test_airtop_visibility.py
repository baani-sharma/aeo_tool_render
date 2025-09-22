#!/usr/bin/env python3
"""
Test Airtop LLM Simulator - Brand Visibility Check
==================================================

This script demonstrates the Airtop LLM Simulator by performing
real brand visibility checks across multiple LLM platforms.
"""

import asyncio
import os
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from airtop_llm_simulator import AirtopLLMSimulator

# Load environment variables
load_dotenv()

async def test_perplexity_only():
    """Test with Perplexity only (no login required)"""
    print("🧪 Testing Airtop LLM Simulator with Perplexity...")
    
    # Initialize simulator
    simulator = AirtopLLMSimulator()
    await simulator.initialize()
    
    # Test prompts
    test_prompts = [
        "What are the best AI content optimization tools?",
        "Compare Clearscope vs MarketMuse for SEO",
        "What AI tools help with content marketing?",
        "Which tools are best for AI-powered content creation?",
        "What are the top SEO tools for 2024?"
    ]
    
    # Check brand visibility
    print("🔍 Checking brand visibility...")
    results = await simulator.check_brand_visibility(
        brand_name="AIO Search",
        competitors=["Clearscope", "MarketMuse", "Surfer SEO", "Frase"],
        prompts=test_prompts,
        platforms=['perplexity']  # Start with Perplexity (no login required)
    )
    
    # Display results
    print("\n📊 Results Summary:")
    print("=" * 60)
    
    for _, row in results.iterrows():
        status = "✅" if row['success'] else "❌"
        brand_status = "✅" if row['brand_mentioned'] else "❌"
        
        print(f"{status} {row['platform'].upper()}: {row['prompt'][:50]}...")
        print(f"   Brand Mentioned: {brand_status}")
        print(f"   Mention Type: {row['mention_type']}")
        print(f"   Competitors: {row['competitors_mentioned']}")
        print(f"   Response Time: {row['response_time']:.2f}s")
        print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/brand_visibility_{timestamp}.csv"
    results.to_csv(filename, index=False)
    print(f"💾 Results saved to: {filename}")
    
    # Calculate statistics
    total_queries = len(results)
    successful_queries = len(results[results['success'] == True])
    brand_mentions = len(results[results['brand_mentioned'] == True])
    
    print(f"\n📈 Statistics:")
    print(f"   Total Queries: {total_queries}")
    print(f"   Successful: {successful_queries}/{total_queries} ({successful_queries/total_queries*100:.1f}%)")
    print(f"   Brand Mentions: {brand_mentions}/{total_queries} ({brand_mentions/total_queries*100:.1f}%)")
    
    # Cleanup
    await simulator.cleanup()
    
    return results

async def test_with_credentials():
    """Test with authenticated platforms (requires pro account credentials)"""
    print("🔐 Testing with authenticated platforms (Pro Accounts)...")
    
    # Check if credentials are available
    email = os.getenv('LLM_EMAIL')
    password = os.getenv('LLM_PASSWORD')
    
    if not email or not password:
        print("❌ Pro account credentials not found in .env file")
        print("   Please add LLM_EMAIL and LLM_PASSWORD to your .env file")
        print("   These should be your ChatGPT Plus, Claude Pro, or Perplexity Pro credentials")
        return None
    
    # Initialize simulator
    simulator = AirtopLLMSimulator()
    await simulator.initialize()
    
    # Authenticate with platforms
    credentials = {'email': email, 'password': password}
    platforms_to_test = ['chatgpt', 'claude', 'gemini']
    
    authenticated_platforms = []
    for platform in platforms_to_test:
        print(f"🔐 Authenticating with {platform}...")
        success = await simulator.authenticate_platform(platform, credentials)
        if success:
            authenticated_platforms.append(platform)
            print(f"✅ Successfully authenticated with {platform}")
        else:
            print(f"❌ Failed to authenticate with {platform}")
    
    if not authenticated_platforms:
        print("❌ No platforms authenticated successfully")
        await simulator.cleanup()
        return None
    
    # Test prompts designed for pro account features
    test_prompts = [
        "What are the best AI content optimization tools?",
        "Compare Clearscope vs MarketMuse for SEO",
        "What AI tools help with content marketing?",
        "What are the latest trends in AI-powered content optimization?",
        "Which AI tools provide the best ROI for content marketing?"
    ]
    
    # Check brand visibility
    print(f"🔍 Checking brand visibility on {len(authenticated_platforms)} platforms...")
    results = await simulator.check_brand_visibility(
        brand_name="AIO Search",
        competitors=["Clearscope", "MarketMuse", "Surfer SEO"],
        prompts=test_prompts,
        platforms=authenticated_platforms
    )
    
    # Display results
    print("\n📊 Results Summary:")
    print("=" * 60)
    
    for _, row in results.iterrows():
        status = "✅" if row['success'] else "❌"
        brand_status = "✅" if row['brand_mentioned'] else "❌"
        
        print(f"{status} {row['platform'].upper()}: {row['prompt'][:50]}...")
        print(f"   Brand Mentioned: {brand_status}")
        print(f"   Mention Type: {row['mention_type']}")
        print(f"   Response Time: {row['response_time']:.2f}s")
        print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/authenticated_visibility_{timestamp}.csv"
    results.to_csv(filename, index=False)
    print(f"💾 Results saved to: {filename}")
    
    # Cleanup
    await simulator.cleanup()
    
    return results

async def test_pro_account_features():
    """Test specific pro account features like web search and enhanced responses"""
    print("🚀 Testing Pro Account Features...")
    
    # Check if credentials are available
    email = os.getenv('LLM_EMAIL')
    password = os.getenv('LLM_PASSWORD')
    
    if not email or not password:
        print("❌ Pro account credentials not found")
        return None
    
    # Initialize simulator
    simulator = AirtopLLMSimulator()
    await simulator.initialize()
    
    # Authenticate with platforms
    credentials = {'email': email, 'password': password}
    platforms_to_test = ['chatgpt', 'claude', 'perplexity']
    
    authenticated_platforms = []
    for platform in platforms_to_test:
        print(f"🔐 Authenticating with {platform}...")
        success = await simulator.authenticate_platform(platform, credentials)
        if success:
            authenticated_platforms.append(platform)
            print(f"✅ Successfully authenticated with {platform}")
        else:
            print(f"❌ Failed to authenticate with {platform}")
    
    if not authenticated_platforms:
        print("❌ No platforms authenticated successfully")
        await simulator.cleanup()
        return None
    
    # Test pro-specific features
    pro_test_prompts = [
        "What are the latest developments in AI content optimization tools as of 2024?",
        "Compare the web search capabilities of ChatGPT Plus vs Claude Pro vs Perplexity Pro",
        "What are the most recent case studies of AI tools improving content marketing ROI?",
        "Which AI platforms provide the most comprehensive web search results for content research?"
    ]
    
    print(f"\n🔍 Testing pro features on {len(authenticated_platforms)} platforms...")
    
    for platform in authenticated_platforms:
        print(f"\n📊 Testing {platform.upper()} pro features:")
        
        for i, prompt in enumerate(pro_test_prompts[:2], 1):  # Test first 2 prompts per platform
            print(f"  {i}. Testing: {prompt[:60]}...")
            
            try:
                result = await simulator.simulate_query(platform, prompt, enable_web_search=True)
                
                if result.success:
                    print(f"     ✅ Success! Response time: {result.response_time:.2f}s")
                    print(f"     📝 Response length: {len(result.response)} characters")
                    print(f"     🌐 Web search results: {len(result.web_search_results)} sources")
                    
                    # Check for pro account indicators
                    if "web search" in result.response.lower() or "searching" in result.response.lower():
                        print(f"     🔍 Web search detected in response")
                    
                    if len(result.response) > 500:
                        print(f"     📈 Long response detected (pro feature)")
                        
                else:
                    print(f"     ❌ Failed: {result.error_message}")
                    
            except Exception as e:
                print(f"     ❌ Error: {str(e)}")
            
            # Rate limiting
            await asyncio.sleep(2)
    
    # Cleanup
    await simulator.cleanup()
    print("\n✅ Pro account feature testing completed!")

async def test_single_query():
    """Test a single query on Perplexity"""
    print("🧪 Testing single query on Perplexity...")
    
    # Initialize simulator
    simulator = AirtopLLMSimulator()
    await simulator.initialize()
    
    # Test a single query
    test_prompt = "What are the best AI content optimization tools for SEO?"
    
    print(f"🔍 Testing query: {test_prompt}")
    
    result = await simulator.simulate_query('perplexity', test_prompt, enable_web_search=True)
    
    if result.success:
        print(f"✅ Query successful!")
        print(f"📝 Response: {result.response[:200]}...")
        print(f"🌐 Web Search Results: {len(result.web_search_results)} found")
        print(f"⏱️  Response Time: {result.response_time:.2f}s")
        
        # Analyze brand mentions
        from airtop_llm_simulator import AirtopLLMSimulator
        mention_analysis = simulator._analyze_brand_mentions(
            result.response, "AIO Search", ["Clearscope", "MarketMuse"]
        )
        
        print(f"🏷️  Brand Mentioned: {mention_analysis['brand_mentioned']}")
        print(f"📊 Mention Type: {mention_analysis['mention_type']}")
        print(f"🏢 Competitors Mentioned: {mention_analysis['competitors_mentioned']}")
        
    else:
        print(f"❌ Query failed: {result.error_message}")
    
    # Cleanup
    await simulator.cleanup()
    
    return result

def main():
    """Main test function"""
    print("🚀 Airtop LLM Simulator - Brand Visibility Test")
    print("=" * 60)
    
    # Check if setup is complete
    if not os.path.exists('airtop_config.json'):
        print("❌ Configuration file not found. Please run setup_airtop.py first")
        return
    
    # Run tests
    print("\n1️⃣ Testing Perplexity (no login required)...")
    perplexity_results = asyncio.run(test_perplexity_only())
    
    print("\n2️⃣ Testing single query...")
    single_result = asyncio.run(test_single_query())
    
    print("\n3️⃣ Testing authenticated platforms...")
    auth_results = asyncio.run(test_with_credentials())
    
    print("\n4️⃣ Testing pro account features...")
    pro_results = asyncio.run(test_pro_account_features())
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    
    if perplexity_results is not None:
        print(f"✅ Perplexity test: {len(perplexity_results)} queries processed")
    
    if auth_results is not None:
        print(f"✅ Authenticated test: {len(auth_results)} queries processed")
    
    if pro_results is not None:
        print(f"✅ Pro account features test completed")
    
    print("\n📋 Next steps:")
    print("1. Review the results in the 'results/' directory")
    print("2. Analyze brand visibility patterns")
    print("3. Adjust prompts and competitors as needed")
    print("4. Set up automated monitoring")

if __name__ == "__main__":
    main() 