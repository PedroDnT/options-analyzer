import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  DollarSign, 
  BarChart3, 
  AlertTriangle,
  RefreshCw,
  Bot,
  Target,
  Shield,
  Zap
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'
import './App.css'

const API_BASE = '/api/eth'

function App() {
  const [marketData, setMarketData] = useState(null)
  const [analysisResults, setAnalysisResults] = useState(null)
  const [tradingPositions, setTradingPositions] = useState([])
  const [loading, setLoading] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [aiQuestion, setAiQuestion] = useState('')
  const [aiResponse, setAiResponse] = useState('')
  const [aiLoading, setAiLoading] = useState(false)
  const [lastUpdated, setLastUpdated] = useState(null)

  // Fetch market data
  const fetchMarketData = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/market-data`)
      const data = await response.json()
      if (data.success) {
        setMarketData(data.data)
        setLastUpdated(new Date(data.timestamp))
      }
    } catch (error) {
      console.error('Error fetching market data:', error)
    }
    setLoading(false)
  }

  // Run comprehensive analysis
  const runAnalysis = async () => {
    setAnalyzing(true)
    try {
      const response = await fetch(`${API_BASE}/analysis`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      const data = await response.json()
      if (data.success) {
        setAnalysisResults(data.analysis)
        setTradingPositions(data.analysis.trading_positions || [])
      }
    } catch (error) {
      console.error('Error running analysis:', error)
    }
    setAnalyzing(false)
  }

  // Ask AI assistant
  const askAI = async () => {
    if (!aiQuestion.trim()) return
    
    setAiLoading(true)
    try {
      const response = await fetch(`${API_BASE}/ai-chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: aiQuestion })
      })
      const data = await response.json()
      if (data.success) {
        setAiResponse(data.response)
      }
    } catch (error) {
      console.error('Error asking AI:', error)
    }
    setAiLoading(false)
  }

  // Load initial data
  useEffect(() => {
    fetchMarketData()
  }, [])

  const formatCurrency = (value) => {
    if (value === null || value === undefined) return 'N/A'
    return `$${value.toLocaleString()}`
  }

  const formatPercent = (value) => {
    if (value === null || value === undefined) return 'N/A'
    return `${value.toFixed(2)}%`
  }

  const getAssessmentColor = (assessment) => {
    switch (assessment) {
      case 'EXPENSIVE': return 'destructive'
      case 'MODERATELY EXPENSIVE': return 'secondary'
      case 'FAIR VALUE': return 'default'
      case 'CHEAP': return 'default'
      default: return 'secondary'
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'HIGH': return 'destructive'
      case 'MEDIUM': return 'secondary'
      case 'LOW': return 'default'
      case 'HEDGE': return 'outline'
      default: return 'default'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <div className="container mx-auto p-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">
                ETH Options Dashboard
              </h1>
              <p className="text-slate-300">
                Live implied volatility analysis and trading recommendations
              </p>
            </div>
            <div className="flex gap-3">
              <Button 
                onClick={fetchMarketData} 
                disabled={loading}
                variant="outline"
                className="bg-white/10 border-white/20 text-white hover:bg-white/20"
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                Refresh Data
              </Button>
              <Button 
                onClick={runAnalysis} 
                disabled={analyzing || !marketData}
                className="bg-blue-600 hover:bg-blue-700"
              >
                <Activity className={`w-4 h-4 mr-2 ${analyzing ? 'animate-pulse' : ''}`} />
                {analyzing ? 'Analyzing...' : 'Run Analysis'}
              </Button>
            </div>
          </div>
          {lastUpdated && (
            <p className="text-sm text-slate-400 mt-2">
              Last updated: {lastUpdated.toLocaleString()}
            </p>
          )}
        </div>

        {/* Market Overview Cards */}
        {marketData && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Card className="bg-white/10 border-white/20 text-white">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">ETH Price</CardTitle>
                <DollarSign className="h-4 w-4 text-green-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{formatCurrency(marketData.eth_price)}</div>
                <p className="text-xs text-slate-300">Current spot price</p>
              </CardContent>
            </Card>

            <Card className="bg-white/10 border-white/20 text-white">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Implied Volatility</CardTitle>
                <TrendingUp className="h-4 w-4 text-blue-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{formatPercent(marketData.eth_iv_deribit)}</div>
                <p className="text-xs text-slate-300">ATM options IV</p>
              </CardContent>
            </Card>

            <Card className="bg-white/10 border-white/20 text-white">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Realized Vol (30D)</CardTitle>
                <BarChart3 className="h-4 w-4 text-orange-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{formatPercent(marketData.eth_rv_30d)}</div>
                <p className="text-xs text-slate-300">Historical volatility</p>
              </CardContent>
            </Card>

            <Card className="bg-white/10 border-white/20 text-white">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">VIX</CardTitle>
                <Activity className="h-4 w-4 text-red-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{formatPercent(marketData.vix)}</div>
                <p className="text-xs text-slate-300">Traditional market vol</p>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Main Dashboard Tabs */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 bg-white/10 border-white/20">
            <TabsTrigger value="overview" className="text-white data-[state=active]:bg-blue-600">
              Overview
            </TabsTrigger>
            <TabsTrigger value="analysis" className="text-white data-[state=active]:bg-blue-600">
              Analysis
            </TabsTrigger>
            <TabsTrigger value="positions" className="text-white data-[state=active]:bg-blue-600">
              Positions
            </TabsTrigger>
            <TabsTrigger value="ai-assistant" className="text-white data-[state=active]:bg-blue-600">
              AI Assistant
            </TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            {marketData && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Volatility Metrics */}
                <Card className="bg-white/10 border-white/20 text-white">
                  <CardHeader>
                    <CardTitle>Volatility Metrics</CardTitle>
                    <CardDescription className="text-slate-300">
                      Current volatility landscape
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex justify-between">
                      <span>ETH IV (Deribit):</span>
                      <span className="font-bold">{formatPercent(marketData.eth_iv_deribit)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>ETH RV (7D):</span>
                      <span className="font-bold">{formatPercent(marketData.eth_rv_7d)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>ETH RV (30D):</span>
                      <span className="font-bold">{formatPercent(marketData.eth_rv_30d)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>BTC RV (7D):</span>
                      <span className="font-bold">{formatPercent(marketData.btc_rv_7d)}</span>
                    </div>
                    <div className="flex justify-between border-t border-white/20 pt-2">
                      <span>VRP (IV - RV):</span>
                      <span className={`font-bold ${(marketData.eth_iv_deribit - marketData.eth_rv_30d) > 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {formatPercent(marketData.eth_iv_deribit - marketData.eth_rv_30d)}
                      </span>
                    </div>
                  </CardContent>
                </Card>

                {/* Options Flow */}
                <Card className="bg-white/10 border-white/20 text-white">
                  <CardHeader>
                    <CardTitle>Options Flow</CardTitle>
                    <CardDescription className="text-slate-300">
                      Market sentiment indicators
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex justify-between">
                      <span>Puts Bought:</span>
                      <span className="font-bold text-red-400">{formatPercent(marketData.puts_bought)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Calls Bought:</span>
                      <span className="font-bold text-green-400">{formatPercent(marketData.calls_bought)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Puts Sold:</span>
                      <span className="font-bold">{formatPercent(marketData.puts_sold)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Calls Sold:</span>
                      <span className="font-bold">{formatPercent(marketData.calls_sold)}</span>
                    </div>
                    <div className="flex justify-between border-t border-white/20 pt-2">
                      <span>Net Put Bias:</span>
                      <span className={`font-bold ${marketData.net_put_bias > 0 ? 'text-red-400' : 'text-green-400'}`}>
                        {formatPercent(marketData.net_put_bias)}
                      </span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </TabsContent>

          {/* Analysis Tab */}
          <TabsContent value="analysis" className="space-y-6">
            {!analysisResults ? (
              <Card className="bg-white/10 border-white/20 text-white">
                <CardContent className="flex flex-col items-center justify-center py-12">
                  <Activity className="w-12 h-12 text-blue-400 mb-4" />
                  <h3 className="text-xl font-semibold mb-2">Run Analysis</h3>
                  <p className="text-slate-300 text-center mb-6">
                    Click "Run Analysis" to generate comprehensive ETH options analysis with AI insights
                  </p>
                  <Button 
                    onClick={runAnalysis} 
                    disabled={analyzing || !marketData}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    <Activity className={`w-4 h-4 mr-2 ${analyzing ? 'animate-pulse' : ''}`} />
                    {analyzing ? 'Analyzing...' : 'Start Analysis'}
                  </Button>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-6">
                {/* Assessment Summary */}
                <Card className="bg-white/10 border-white/20 text-white">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Target className="w-5 h-5" />
                      Market Assessment
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="text-center">
                        <Badge variant={getAssessmentColor(analysisResults.assessment?.overall_assessment)} className="mb-2">
                          {analysisResults.assessment?.overall_assessment || 'N/A'}
                        </Badge>
                        <p className="text-sm text-slate-300">Overall IV Assessment</p>
                      </div>
                      <div className="text-center">
                        <Badge variant="secondary" className="mb-2">
                          {analysisResults.assessment?.regime || 'N/A'}
                        </Badge>
                        <p className="text-sm text-slate-300">Volatility Regime</p>
                      </div>
                      <div className="text-center">
                        <Badge variant="default" className="mb-2">
                          {analysisResults.assessment?.confidence || 'N/A'}
                        </Badge>
                        <p className="text-sm text-slate-300">Analysis Confidence</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <Card className="bg-white/10 border-white/20 text-white">
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold">{formatPercent(analysisResults.current_metrics?.vrp)}</div>
                      <p className="text-sm text-slate-300">Volatility Risk Premium</p>
                    </CardContent>
                  </Card>
                  <Card className="bg-white/10 border-white/20 text-white">
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold">{(analysisResults.current_metrics?.estimated_ivr * 100)?.toFixed(0)}%</div>
                      <p className="text-sm text-slate-300">IV Rank</p>
                    </CardContent>
                  </Card>
                  <Card className="bg-white/10 border-white/20 text-white">
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold">{formatPercent(analysisResults.skew_analysis?.put_call_skew)}</div>
                      <p className="text-sm text-slate-300">Put-Call Skew</p>
                    </CardContent>
                  </Card>
                  <Card className="bg-white/10 border-white/20 text-white">
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold">{formatPercent(analysisResults.forward_projections?.mc_mean)}</div>
                      <p className="text-sm text-slate-300">Expected IV (30D)</p>
                    </CardContent>
                  </Card>
                </div>

                {/* AI Insights */}
                {analysisResults.ai_insights && (
                  <Card className="bg-white/10 border-white/20 text-white">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Bot className="w-5 h-5" />
                        AI Market Analysis
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div>
                          <h4 className="font-semibold mb-2">Executive Summary</h4>
                          <p className="text-slate-300">{analysisResults.ai_insights.executive_summary}</p>
                        </div>
                        <div>
                          <h4 className="font-semibold mb-2">Market Analysis</h4>
                          <p className="text-slate-300">{analysisResults.ai_insights.market_analysis}</p>
                        </div>
                        <div>
                          <h4 className="font-semibold mb-2">Risk Assessment</h4>
                          <p className="text-slate-300">{analysisResults.ai_insights.risk_assessment}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            )}
          </TabsContent>

          {/* Trading Positions Tab */}
          <TabsContent value="positions" className="space-y-6">
            {tradingPositions.length === 0 ? (
              <Card className="bg-white/10 border-white/20 text-white">
                <CardContent className="flex flex-col items-center justify-center py-12">
                  <Target className="w-12 h-12 text-blue-400 mb-4" />
                  <h3 className="text-xl font-semibold mb-2">No Positions Available</h3>
                  <p className="text-slate-300 text-center">
                    Run the analysis to generate trading position recommendations
                  </p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4">
                {tradingPositions.map((position, index) => (
                  <Card key={index} className="bg-white/10 border-white/20 text-white">
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <CardTitle className="flex items-center gap-2">
                          <Zap className="w-5 h-5" />
                          {position.position_type}
                        </CardTitle>
                        <div className="flex gap-2">
                          <Badge variant={getPriorityColor(position.priority)}>
                            {position.priority}
                          </Badge>
                          {position.entry_criteria_met && (
                            <Badge variant="default" className="bg-green-600">
                              ✓ Ready
                            </Badge>
                          )}
                        </div>
                      </div>
                      <CardDescription className="text-slate-300">
                        {position.strategy}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <div>
                          <p className="text-sm text-slate-400">Strikes</p>
                          <p className="font-semibold">{position.strikes}</p>
                        </div>
                        <div>
                          <p className="text-sm text-slate-400">Expiry</p>
                          <p className="font-semibold">{position.expiry}</p>
                        </div>
                        <div>
                          <p className="text-sm text-slate-400">Net Credit/Debit</p>
                          <p className={`font-semibold ${position.net_credit_debit > 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {position.net_credit_debit > 0 ? '+' : ''}{formatCurrency(position.net_credit_debit)}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm text-slate-400">Win Probability</p>
                          <p className="font-semibold">
                            {position.win_probability ? `${(position.win_probability * 100).toFixed(0)}%` : 'N/A'}
                          </p>
                        </div>
                      </div>
                      
                      {position.max_risk && (
                        <div className="mt-4 p-3 bg-red-500/20 border border-red-500/30 rounded">
                          <p className="text-sm">
                            <Shield className="w-4 h-4 inline mr-1" />
                            Max Risk: {formatCurrency(position.max_risk)}
                          </p>
                        </div>
                      )}

                      {analysisResults?.ai_insights?.position_commentary?.[position.position_type] && (
                        <div className="mt-4 p-3 bg-blue-500/20 border border-blue-500/30 rounded">
                          <p className="text-sm">
                            <Bot className="w-4 h-4 inline mr-1" />
                            {analysisResults.ai_insights.position_commentary[position.position_type]}
                          </p>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </TabsContent>

          {/* AI Assistant Tab */}
          <TabsContent value="ai-assistant" className="space-y-6">
            <Card className="bg-white/10 border-white/20 text-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Bot className="w-5 h-5" />
                  AI Assistant
                </CardTitle>
                <CardDescription className="text-slate-300">
                  Ask questions about the ETH options analysis
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-2">
                  <Input
                    placeholder="Ask about volatility, positions, or market conditions..."
                    value={aiQuestion}
                    onChange={(e) => setAiQuestion(e.target.value)}
                    className="bg-white/10 border-white/20 text-white placeholder:text-slate-400"
                    onKeyPress={(e) => e.key === 'Enter' && askAI()}
                  />
                  <Button 
                    onClick={askAI} 
                    disabled={aiLoading || !aiQuestion.trim()}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    {aiLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : 'Ask'}
                  </Button>
                </div>
                
                {aiResponse && (
                  <div className="p-4 bg-blue-500/20 border border-blue-500/30 rounded">
                    <h4 className="font-semibold mb-2">AI Response:</h4>
                    <p className="text-slate-200 whitespace-pre-wrap">{aiResponse}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App

