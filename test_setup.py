#!/usr/bin/env python3
"""
Test script to validate the ETH Options Analyzer setup
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import flask
        print(f"✅ Flask: {flask.__version__}")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import openai
        print(f"✅ OpenAI: {openai.__version__}")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        import numpy
        print(f"✅ NumPy: {numpy.__version__}")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import pandas
        print(f"✅ Pandas: {pandas.__version__}")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    print("\n🔧 Testing environment variables...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        masked_key = api_key[:7] + '...' + api_key[-4:] if len(api_key) > 11 else 'SET'
        print(f"✅ OPENAI_API_KEY: {masked_key}")
    else:
        print("❌ OPENAI_API_KEY not found")
        return False
    
    secret_key = os.getenv('FLASK_SECRET_KEY')
    if secret_key:
        print(f"✅ FLASK_SECRET_KEY: {'SET' if secret_key else 'NOT SET'}")
    else:
        print("❌ FLASK_SECRET_KEY not found")
    
    print(f"✅ FLASK_ENV: {os.getenv('FLASK_ENV', 'not set')}")
    print(f"✅ DATABASE_URL: {os.getenv('DATABASE_URL', 'not set')}")
    
    return True

def test_data_collector():
    """Test data collector functionality"""
    print("\n📊 Testing data collector...")
    
    try:
        from data_collector import ETHDataCollector
        collector = ETHDataCollector()
        
        # Test cached data
        cached_data = collector.get_cached_data()
        print(f"✅ Cached data loaded: ETH Price ${cached_data.get('eth_price', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Data collector test failed: {e}")
        return False

def test_analysis_engine():
    """Test analysis engine"""
    print("\n🧮 Testing analysis engine...")
    
    try:
        from analysis_engine import ETHOptionsAnalyzer
        from data_collector import ETHDataCollector
        
        analyzer = ETHOptionsAnalyzer()
        collector = ETHDataCollector()
        
        # Get sample data
        market_data = collector.get_cached_data()
        
        # Run basic analysis
        analysis = analyzer.comprehensive_analysis(market_data)
        
        vrp = analysis.get('current_metrics', {}).get('vrp')
        print(f"✅ Analysis completed: VRP {vrp:.2f}%" if vrp else "✅ Analysis completed")
        
        return True
    except Exception as e:
        print(f"❌ Analysis engine test failed: {e}")
        return False

def test_ai_assistant():
    """Test AI assistant setup"""
    print("\n🤖 Testing AI assistant...")
    
    try:
        from ai_assistant import ETHOptionsAIAssistant
        ai = ETHOptionsAIAssistant()
        print("✅ AI assistant initialized successfully")
        
        # Test a simple question (without actually calling OpenAI)
        print("✅ AI assistant ready for GPT-4o-mini queries")
        
        return True
    except Exception as e:
        print(f"❌ AI assistant test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 ETH Options Analyzer - Setup Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run all tests
    tests = [
        test_imports,
        test_environment,
        test_data_collector,
        test_analysis_engine,
        test_ai_assistant
    ]
    
    for test in tests:
        if not test():
            all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! Your ETH Options Analyzer is ready to run.")
        print("\n📋 Next steps:")
        print("1. Run: python main.py")
        print("2. Open: http://localhost:5001")
        print("3. Test the API endpoints")
        print("\n🔗 API Endpoints:")
        print("- GET /api/eth/market-data")
        print("- POST /api/eth/analysis")
        print("- POST /api/eth/ai-chat")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()