# Forex Monitoring Agent: Real-Time Market Intelligence with Africa's Talking

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DeepSeek-R1](https://img.shields.io/badge/Model-DeepSeekR1-green)](https://huggingface.co/deepseek-ai/deepseek-r1)

The Forex Monitoring Agent is an AI-powered system that autonomously tracks currency markets, detects significant events in real-time, and alerts traders through voice calls using Africa's Talking API. Built on DeepSeek-R1, this agent provides actionable intelligence when market conditions change rapidly, with special focus on African markets.

## Key Features

- **Real-time Event Detection**: Identifies price spikes and breaking news instantly
- **AI-Powered Analysis**: DeepSeek-R1 provides market insights and recommendations
- **Priority Alert System**: Critical alerts bypass normal processing queues
- **Voice Call Notifications**: Get alerts directly to your phone via Africa's Talking
- **Market Hours Awareness**: Only alerts during active trading sessions
- **Resource Optimization**: Sleeps during normal conditions, activates on events
- **Africa Focus**: Optimized for African markets and phone networks

## System Architecture

```mermaid
graph TD
    A[Market Data Stream] -->|Price Events| B[Priority Event Queue]
    C[News Monitor] -->|News Events| B
    B --> D{Event Processor}
    D -->|High Priority| E[Price Event Handler]
    D -->|Medium Priority| F[News Event Handler]
    E --> G[AI Analysis]
    F --> G
    G --> H[Alert System]
    H --> I[Africa's Talking Voice API]
```

### Core Components

1. **Data Ingestion Layer**
   - Real-time market data streams
   - News feed monitoring
   - Economic calendar integration

2. **Event Processing Engine**
   - Priority-based queue system
   - Dedicated event handlers
   - AI-powered analysis

3. **Alert System**
   - Africa's Talking voice call notifications
   - Rate limiting
   - Market hours detection

## Getting Started

### Prerequisites

- Python 3.8+
- Africa's Talking account ([sign up for free](https://africastalking.com/))
- NVIDIA GPU recommended (but not required)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/InterfaceLab-Libraries-SDKs/forex-monitoring-agent-real-time-market-intelligence.git
cd forex-monitoring-agent-real-time-market-intelligence
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:
```env
# Forex Alert Agent Configuration
AFRICASTALKING_USERNAME=your_africastalking_username
AFRICASTALKING_API_KEY=your_africastalking_api_key
YOUR_PHONE_NUMBER=+2547XXXXXXXX  # Format: +2547XXXXXXXX
```

### Running the Agent

```bash
python forex_agent.py
```

### Behavior Output:

```bash
🚀 Starting Advanced Forex Agent
🔍 Monitoring: EUR/USD, USD/JPY, GBP/USD, AUD/USD
⏱️ Market hours: 24/5

🖥️ SYSTEM STATUS
Queue depth: 0
Active events: 0
Latest alerts:
  EUR/USD: 1.0823 | Last alert: 325s ago

⚡ EVENT RECEIVED [price] for EUR/USD
📢 The EUR/USD pair has experienced a significant movement of 1.62% in the last minute...

🚨 ALERT: EUR/USD PRICE MOVEMENT: 1.62%
📞 Call initiated: CA1234567890abcdef

🖥️ SYSTEM STATUS
Queue depth: 1
Active events: 0
Latest alerts:
  EUR/USD: 1.0823 | Last alert: 0s ago
```

## Configuration

Customize the agent behavior by modifying these parameters in the code:

```python
# Core configuration parameters
monitored_pairs = ["EUR/USD", "USD/JPY", "GBP/USD", "AUD/USD", "USD/KES"]
alert_thresholds = {
    "emergency_price": 1.5,  # Percentage change
    "price_spike": 0.8       # Percentage change
}
news_keywords = ["interest rate", "inflation", "policy", "crisis", "war"]
```

### Event Priorities

| Event Type         | Priority | Description                           |
|--------------------|----------|---------------------------------------|
| emergency_price    | 1        | Extreme price movements (>1.5%)      |
| breaking_news      | 1        | Critical news events                 |
| price_spike        | 2        | Significant price movements (>0.8%)  |
| news               | 3        | Important but not critical news      |
| status_update      | 4        | System health checks                 |

## Africa's Talking Integration

### Voice Call Configuration

The agent uses Africa's Talking Voice API to make calls. Key implementation details:

```python
import africastalking

# Initialize SDK
africastalking.initialize(
    username=os.getenv('AFRICASTALKING_USERNAME'),
    api_key=os.getenv('AFRICASTALKING_API_KEY')
)

# Create voice service instance
voice = africastalking.Voice

# Make call
response = voice.call(
    callFrom='+254711XXXYYY',  # Your Africa's Talking virtual number
    callTo=[os.getenv('YOUR_PHONE_NUMBER')]
)
```

### Benefits for African Users

1. **Local Phone Number Support**: Works seamlessly with local phone numbers
2. **Cost-Effective**: Lower call rates for African networks
3. **Network Optimization**: Better connectivity with local carriers
4. **SMS Fallback**: Option to add SMS notifications for failed calls

## Customization

### Integrating Real Data Sources

Replace the simulated data streams with real APIs:

1. **Market Data** (Uncomment and implement in `market_data_stream()`):
```python
# Real implementation example
async def real_market_data_stream():
    async with connect("wss://api.forexpros.com/ws") as ws:
        await ws.send(json.dumps({"action": "subscribe", "symbols": ["EUR/USD"]}))
        while True:
            data = await ws.recv()
            # Process real market data
```

2. **News Feed** (Uncomment and implement in `news_monitor()`):
```python
# Real news API implementation
async def real_news_monitor():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://newsapi.org/v2/everything?q=forex") as response:
            data = await response.json()
            # Process real news data
```

### Modifying AI Behavior

Adjust the prompt engineering for African market focus:

```python
# Custom analysis prompt with African context
custom_prompt = (
    f"Act as a forex analyst specializing in African markets. For {pair} movement of {change}%, "
    "consider impact on African currencies and economies. "
    "Provide trading recommendations relevant to African traders:"
)
```

## Troubleshooting

### Common Issues

1. **Africa's Talking connection errors**:
   - Verify username and API key
   - Ensure phone number is in E.164 format (+2547XXXXXXXX)
   - Check account balance in Africa's Talking dashboard

2. **Slow AI responses**:
   - Enable GPU acceleration
   - Reduce `max_new_tokens` parameter
   - Use model quantization

3. **Missed events**:
   - Decrease sleep intervals in monitors
   - Increase queue capacity
   - Adjust alert thresholds

### Africa's Talking Specific Tips

| Issue                  | Solution                                  |
|------------------------|-------------------------------------------|
| Call not connecting    | Verify number format (+2547XXXXXXXX)      |
| Call drops quickly     | Increase message length to >5 seconds     |
| No voice heard         | Check text-to-speech formatting           |
| Authorization errors   | Verify username/api key combination       |

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

### Development Setup

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest tests/
```

3. Verify code style:
```bash
flake8 forex_agent.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Third-party Licenses:**
- [DeepSeek-R1](https://huggingface.co/deepseek-ai/deepseek-r1): Apache 2.0
- [Africa's Talking SDK](https://github.com/AfricasTalkingLtd/africastalking-python): MIT
- [Transformers](https://github.com/huggingface/transformers): Apache 2.0

## Roadmap

- [ ] Add African market data sources (NSE, JSE)
- [ ] Implement SMS fallback notifications
- [ ] Add support for local African languages
- [ ] Create web dashboard for monitoring
- [ ] Add mobile app integration

## Acknowledgements

- [DeepSeek](https://www.deepseek.com) for the powerful language model
- [Hugging Face](https://huggingface.co) for model hosting
- [Africa's Talking](https://africastalking.com) for communication APIs
- [Python](https://python.org) for the programming language foundation

---

**Disclaimer**: This software is for educational purposes only. Forex trading involves significant risk of loss and is not suitable for all investors. The developers assume no responsibility for any trading decisions made using this tool.







