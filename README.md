# ETH Options Analyzer 📈

A comprehensive Ethereum options analysis dashboard with real-time implied volatility analysis, Monte Carlo simulations, and AI-powered trading recommendations.

## Features 🚀

- **Real-time Market Data**: ETH price, implied volatility from Deribit, options flow
- **Advanced Analytics**: Volatility Risk Premium, IV Rank, Skew Analysis
- **AI-Powered Insights**: GPT-4 powered market analysis and position commentary  
- **Trading Positions**: Automated generation of options strategies
- **Cross-Asset Analysis**: BTC/ETH ratios, VIX correlation, MOVE index
- **Monte Carlo Simulations**: Forward-looking volatility projections

## Architecture 🏗️

### Backend (Python/Flask)
- `main.py` - Flask application entry point
- `data_collector.py` - Real-time market data from APIs
- `analysis_engine.py` - Quantitative analysis engine
- `ai_assistant.py` - OpenAI GPT-4 integration

### Frontend (React)
- `App.jsx` - Main dashboard component
- `index.html` - Entry point

## Quick Start 🎯

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

### Backend Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env
python main.py
```

### Frontend Setup  
```bash
npm install
npm run dev
```

## API Endpoints 📡

- `GET /api/eth/market-data` - Current market data
- `POST /api/eth/analysis` - Run comprehensive analysis
- `POST /api/eth/ai-chat` - AI assistant chat

## Key Metrics 📊

- **VRP (Volatility Risk Premium)**: IV - RV spread
- **IV Rank**: Current IV percentile vs historical range
- **Put-Call Skew**: 25D put vs call volatility differential
- **Regime Analysis**: Low/Medium/High volatility classification

## Trading Strategies 💡

1. **Short Put Spreads** - High VRP + elevated skew
2. **Short Straddles** - Extreme IV levels  
3. **Calendar Spreads** - Term structure opportunities
4. **Protective Puts** - Portfolio hedging

## Environment Variables 🔧

```env
OPENAI_API_KEY=your_openai_api_key
FLASK_SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///database/app.db
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License 📄

MIT License - see LICENSE file for details

## Disclaimer ⚠️

This tool is for educational and research purposes. Options trading involves substantial risk. Past performance does not guarantee future results.