#!/usr/bin/env python3
"""
Autonomous Forex Monitoring Agent with Africa's Talking Integration
Built on DeepSeek-R1 with Real-time Focus Architecture
"""

import asyncio
import json
import random
import time
from datetime import datetime
from dotenv import load_dotenv
import os
import heapq
import africastalking
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load environment variables
load_dotenv()

class PriorityEventQueue:
    """Priority queue for event handling (1 = highest priority)"""
    def __init__(self):
        self._queue = []
        self._event_available = asyncio.Event()
    
    def put(self, priority, event):
        heapq.heappush(self._queue, (priority, time.time(), event))
        self._event_available.set()
    
    async def get(self):
        while not self._queue:
            await self._event_available.wait()
            self._event_available.clear()
        
        return heapq.heappop(self._queue)[2]  # Return just the event

class ForexAgent:
    EVENT_PRIORITIES = {
        "emergency_price": 1,
        "breaking_news": 1,
        "price_spike": 2,
        "news": 3,
        "status_update": 4
    }
    
    def __init__(self):
        # Initialize Africa's Talking SDK
        africastalking.initialize(
            username=os.getenv('AFRICASTALKING_USERNAME'),
            api_key=os.getenv('AFRICASTALKING_API_KEY')
        )
        self.voice = africastalking.Voice
        
        # Initialize AI model
        self.tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-r1")
        self.model = AutoModelForCausalLM.from_pretrained(
            "deepseek-ai/deepseek-r1",
            device_map="auto",
            torch_dtype="auto"
        )
        
        # State tracking
        self.market_state = {}
        self.last_alert_time = 0
        self.event_queue = PriorityEventQueue()
        self.active_events = {}
        self.resource_lock = asyncio.Lock()
        
        # Configuration
        self.monitored_pairs = ["EUR/USD", "USD/JPY", "GBP/USD", "AUD/USD", "USD/KES"]
        self.alert_thresholds = {
            "emergency_price": 1.5,  # Percentage change
            "price_spike": 0.8       # Percentage change
        }
        self.news_keywords = ["interest rate", "inflation", "policy", "crisis", "war"]
        
        # Initialize market state
        for pair in self.monitored_pairs:
            self.market_state[pair] = {
                "price": random.uniform(0.8, 1.2),
                "last_alert": 0,
                "volatility": 0.1,
                "history": []
            }

    async def market_data_stream(self):
        """Simulated real-time market data stream"""
        while True:
            # Update prices with random walk
            for pair in self.monitored_pairs:
                state = self.market_state[pair]
                last_price = state["price"]
                
                # Generate normal price movement
                change = random.uniform(-0.003, 0.003)
                new_price = last_price * (1 + change)
                
                # Occasionally create significant events
                if random.random() < 0.05:  # 5% chance of event
                    movement = random.choice([-1, 1]) * random.uniform(0.01, 0.05)
                    new_price = last_price * (1 + movement)
                    change = movement
                
                # Update state
                state["price"] = new_price
                state["history"].append({
                    "price": new_price,
                    "timestamp": time.time()
                })
                
                # Trim history
                if len(state["history"]) > 100:
                    state["history"] = state["history"][-50:]
                
                # Calculate and store volatility
                prices = [h["price"] for h in state["history"][-20:]]
                mean_price = sum(prices) / len(prices)
                state["volatility"] = (sum((p - mean_price)**2 for p in prices) / len(prices)) ** 0.5
                
                # Detect significant movements
                abs_change = abs(change * 100)
                event_type = None
                
                if abs_change > self.alert_thresholds["emergency_price"]:
                    event_type = "emergency_price"
                elif abs_change > self.alert_thresholds["price_spike"]:
                    event_type = "price_spike"
                
                if event_type:
                    self.event_queue.put(
                        self.EVENT_PRIORITIES[event_type],
                        {"type": "price", "pair": pair, "change": change*100, "price": new_price}
                    )
            
            await asyncio.sleep(0.5)  # Fast market updates

    async def news_monitor(self):
        """Simulated news monitoring system"""
        sample_news = [
            ("ECB announces emergency rate hike", "EUR/USD"),
            ("US inflation exceeds forecasts", "USD/JPY"),
            ("Political crisis deepens in the UK", "GBP/USD"),
            ("Bank of Japan intervenes in FX market", "USD/JPY"),
            ("Fed signals pause in rate hikes", "EUR/USD"),
            ("Geopolitical tensions escalate", "USD/CHF"),
            ("Natural disaster impacts major economy", "AUD/USD"),
            ("Central Bank of Kenya adjusts rates", "USD/KES"),
            ("South African economic outlook worsens", "USD/ZAR")
        ]
        
        while True:
            # Simulate news events
            if random.random() < 0.02:  # 2% chance of news
                headline, pair = random.choice(sample_news)
                
                # Determine priority
                priority = self.EVENT_PRIORITIES["breaking_news"] if any(
                    kw in headline.lower() for kw in ["emergency", "crisis", "war", "disaster"]
                ) else self.EVENT_PRIORITIES["news"]
                
                self.event_queue.put(
                    priority,
                    {"type": "news", "headline": headline, "pair": pair}
                )
            
            await asyncio.sleep(5)

    async def event_processor(self):
        """Core event processing with dedicated resource allocation"""
        print("🔄 Event processor started - waiting for events")
        while True:
            event = await self.event_queue.get()
            print(f"\n⚡ EVENT RECEIVED [{event['type']}] for {event.get('pair', '')}")
            
            # Dedicate full resources to event
            async with self.resource_lock:
                if event["type"] == "price":
                    await self.handle_price_event(event)
                elif event["type"] == "news":
                    await self.handle_news_event(event)
            
            # Add slight delay to prevent resource starvation
            await asyncio.sleep(0.1)

    async def handle_price_event(self, event):
        """Focused price event analysis"""
        pair = event["pair"]
        state = self.market_state[pair]
        
        # Generate AI analysis
        prompt = (
            f"Generate urgent Forex trading alert. Currency pair: {pair}. "
            f"Price movement: {event['change']:.2f}% in last minute. "
            f"Current price: {event['price']:.4f}. Volatility: {state['volatility']:.4f}. "
            "Provide concise analysis and recommendation:"
        )
        
        analysis = await self.generate_ai_response(prompt)
        await self.maybe_trigger_alert(
            f"{pair} PRICE MOVEMENT: {abs(event['change']):.2f}%",
            analysis,
            pair
        )

    async def handle_news_event(self, event):
        """Focused news event analysis"""
        # Generate AI analysis
        prompt = (
            f"Generate breaking Forex news alert. Currency pair: {event['pair']}. "
            f"Headline: '{event['headline']}'. "
            "Analyze potential market impact and provide trading recommendation:"
        )
        
        analysis = await self.generate_ai_response(prompt)
        await self.maybe_trigger_alert(
            f"{event['pair']} NEWS: {event['headline'][:30]}...",
            analysis,
            event["pair"]
        )

    async def generate_ai_response(self, prompt):
        """Generate response using DeepSeek-R1 with async optimization"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        # Run generation in thread to avoid blocking event loop
        loop = asyncio.get_running_loop()
        outputs = await loop.run_in_executor(
            None, 
            lambda: self.model.generate(**inputs, max_new_tokens=150, temperature=0.7)
        )
        
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return full_response.replace(prompt, "").strip()

    async def maybe_trigger_alert(self, title, message, pair):
        """Smart alert triggering with rate limiting"""
        now = time.time()
        state = self.market_state[pair]
        
        # Apply rate limiting per pair
        if now - state["last_alert"] < 300:  # 5 minutes cooldown per pair
            print(f"⏳ Cooldown active for {pair} - suppressing alert")
            return
        
        # Only alert during market hours
        if not self.is_market_hours():
            print("🌙 Outside market hours - suppressing alert")
            return
        
        print(f"\n🚨 ALERT: {title}")
        print(f"📢 {message}")
        
        # Only call if Africa's Talking is configured
        if not all([os.getenv("AFRICASTALKING_USERNAME"), os.getenv("AFRICASTALKING_API_KEY"), os.getenv("YOUR_PHONE_NUMBER")]):
            print("⚠️ Africa's Talking not configured - skipping call")
            return
        
        try:
            # Create phone call
            response = self.voice.call(
                callFrom=os.getenv("AFRICASTALKING_VIRTUAL_NUMBER", "+254711XXXYYY"),
                callTo=[os.getenv('YOUR_PHONE_NUMBER')]
            )
            
            # Extract call ID from response
            call_id = response['entries'][0]['callId'] if 'entries' in response else 'N/A'
            print(f"📞 Call initiated: ID={call_id}")
            
            state["last_alert"] = now
            self.last_alert_time = now
        except Exception as e:
            print(f"❌ Africa's Talking error: {str(e)}")

    def is_market_hours(self):
        """Check if it's Forex market hours (24/5 but prioritize active sessions)"""
        hour = datetime.utcnow().hour
        # Asian: 23-8 UTC, European: 7-16 UTC, US: 12-21 UTC
        return (0 <= hour < 8) or (7 <= hour < 17) or (12 <= hour < 22)

    async def system_monitor(self):
        """Periodic system health checks"""
        while True:
            await asyncio.sleep(60)
            print("\n🖥️ SYSTEM STATUS")
            print(f"Monitored pairs: {', '.join(self.monitored_pairs)}")
            print(f"Queue depth: {len(self.event_queue._queue)}")
            print(f"Latest alerts:")
            for pair in self.monitored_pairs:
                state = self.market_state[pair]
                last_alert = state["last_alert"]
                alert_status = f"{int(time.time() - last_alert)}s ago" if last_alert > 0 else "Never"
                print(f"  {pair}: {state['price']:.4f} | Last alert: {alert_status}")

    async def run(self):
        """Start the agent system"""
        print("🚀 Starting Advanced Forex Agent with Africa's Talking")
        print(f"🔍 Monitoring: {', '.join(self.monitored_pairs)}")
        print(f"⏱️ Market hours: {'Active' if self.is_market_hours() else 'Check UTC schedule'}")
        
        # Start all components
        await asyncio.gather(
            self.market_data_stream(),
            self.news_monitor(),
            self.event_processor(),
            self.system_monitor()
        )

if __name__ == "__main__":
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("# Forex Alert Agent Configuration\n")
            f.write("AFRICASTALKING_USERNAME=your_africastalking_username\n")
            f.write("AFRICASTALKING_API_KEY=your_africastalking_api_key\n")
            f.write("AFRICASTALKING_VIRTUAL_NUMBER=+254711XXXYYY\n")
            f.write("YOUR_PHONE_NUMBER=+2547XXXXXXXX\n")
        print("ℹ️ Created .env template - please fill in your credentials")
    
    agent = ForexAgent()
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped by user")
