#!/usr/bin/env python3
"""
API test script for ETH Options Analyzer
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001/api/eth"

def test_market_data():
    """Test market data endpoint"""
    print("📊 Testing market data endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/market-data", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            market_data = data.get('data', {})
            print(f"✅ Market data retrieved:")
            print(f"   ETH Price: ${market_data.get('eth_price', 'N/A')}")
            print(f"   ETH IV: {market_data.get('eth_iv_deribit', 'N/A')}%")
            print(f"   VIX: {market_data.get('vix', 'N/A')}")
            return True
        else:
            print(f"❌ API returned error: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Market data test failed: {e}")
        return False

def test_analysis():
    """Test analysis endpoint"""
    print("\n🧮 Testing analysis endpoint...")
    try:
        payload = {
            "use_cached_data": True,
            "include_ai_insights": False  # Skip AI for speed
        }
        
        response = requests.post(f"{BASE_URL}/analysis", 
                               json=payload, 
                               timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            analysis = data.get('analysis', {})
            metrics = analysis.get('current_metrics', {})
            print(f"✅ Analysis completed:")
            print(f"   VRP: {metrics.get('vrp', 'N/A')}%")
            print(f"   IV Rank: {metrics.get('estimated_ivr', 'N/A')}")
            print(f"   Positions: {len(analysis.get('trading_positions', []))} generated")
            return True
        else:
            print(f"❌ API returned error: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def test_ai_chat():
    """Test AI chat endpoint"""
    print("\n🤖 Testing AI chat endpoint...")
    try:
        payload = {
            "question": "What is the current market regime for ETH options?"
        }
        
        response = requests.post(f"{BASE_URL}/ai-chat", 
                               json=payload, 
                               timeout=20)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            ai_response = data.get('response', '')
            print(f"✅ AI response received:")
            print(f"   Response: {ai_response[:100]}..." if len(ai_response) > 100 else f"   Response: {ai_response}")
            return True
        else:
            print(f"❌ API returned error: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ AI chat test failed: {e}")
        return False

def main():
    """Run API tests"""
    print("🧪 ETH Options Analyzer - API Test Suite")
    print("=" * 50)
    print("📝 Make sure the Flask server is running: python main.py")
    print()
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    tests_passed = 0
    total_tests = 3
    
    # Run tests
    if test_market_data():
        tests_passed += 1
    
    if test_analysis():
        tests_passed += 1
        
    if test_ai_chat():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All API tests passed! Your ETH Options Analyzer is working perfectly.")
        print("\n🌐 You can now:")
        print("1. Open http://localhost:5001 in your browser")
        print("2. Test the React frontend")
        print("3. Use the API endpoints programmatically")
    else:
        print("❌ Some tests failed. Check server logs for details.")

if __name__ == '__main__':
    main()