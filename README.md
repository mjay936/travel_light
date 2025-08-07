# travel_light
# Travel Light - AI Travel Planning Assistant

An intelligent travel planning system that uses multiple AI agents to create detailed itineraries, search for flights, and find hotels. Available as both a web interface and command-line application.

## 🚀 Quick Start

### Option 1: Easy Launcher (Recommended)
```bash
python run_webapp.py
```
This gives you a menu to choose between web interface, CLI, demo, or setup check.

### Option 2: Web Interface
```bash
streamlit run travel_light_webpage.py
```
Opens a beautiful web interface in your browser at http://localhost:8501

### Option 3: Command Line
```bash
python travel_light.py
```

### Option 4: Demo Version (No API Keys Required)
```bash
python demo_version.py
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Copy `env_template.txt` to `.env`
   - Fill in your API keys:
     - `OPENAI_API_KEY` (required) - Get from [OpenAI](https://platform.openai.com/api-keys)
     - `AMADEUS_API_KEY` and `AMADEUS_API_SECRET` (optional) - Get from [Amadeus](https://developers.amadeus.com/)
     - `AVIATIONSTACK_API_KEY` (optional) - Get from [AviationStack](https://aviationstack.com/)

## Features

### 🌐 Web Interface
- **Beautiful Chat Interface**: Modern, responsive design
- **Real-time AI Responses**: See the AI planning your trip live
- **PDF Export**: Download your conversation as a PDF
- **Debug Mode**: Toggle to see technical details
- **Sidebar Help**: Built-in instructions and examples

### 💻 Command Line Interface
- **Fast & Lightweight**: Quick responses without browser overhead
- **Full AI Integration**: Complete multi-agent system
- **Error Handling**: Graceful handling of missing API keys

### 🎮 Demo Mode
- **No API Keys Required**: Works immediately
- **Sample Data**: See how the system works
- **Perfect for Testing**: Try before you buy API credits

## Usage Examples

### Web Interface
1. Open http://localhost:8501
2. Type: "Plan a 3-day budget trip to Bali"
3. Review the AI-generated itinerary
4. Confirm and get hotel/flight options
5. Export your conversation as PDF

### Command Line
```bash
# Start the application
python travel_light.py

# The system will prompt you for:
# - Destination
# - Number of days
# - Budget level
# - Travel preferences
```

## File Structure

```
travel_light_cursor/
├── travel_light.py              # Main AI application
├── travel_light_webpage.py      # Streamlit web interface
├── run_webapp.py               # Launcher script
├── demo_version.py             # Demo without API keys
├── travel_graph.py             # Graph integration
├── llm_provider.py             # OpenAI integration
├── langgraph_supervisor.py     # Multi-agent supervisor
├── requirements.txt            # Dependencies
├── README.md                   # This file
└── env_template.txt           # Environment template
```

## API Integration

### Required
- **OpenAI API**: Powers the AI conversation and itinerary generation

### Optional
- **Amadeus API**: Real hotel search and booking
- **AviationStack API**: Real flight search and booking

## Troubleshooting

### "OpenAI API Key not found"
- Create a `.env` file with your API key
- Get a key from https://platform.openai.com/api-keys

### "Import errors"
- Run `pip install -r requirements.txt`
- Make sure all files are in the same directory

### "Web interface won't start"
- Check if port 8501 is available
- Try `streamlit run travel_light_webpage.py --server.port 8502`

## Example Output

```
User: Plan a 3-day budget trip to Bali
AI: 🌴 Here's a 3-day budget trip to Bali:

Day 1: Arrival & Kuta Beach
- Arrive at Ngurah Rai International Airport
- Check into budget hostel in Kuta
- Explore Kuta Beach and watch sunset
- Dinner at local warung

Day 2: Cultural Ubud
- Visit Sacred Monkey Forest
- Explore Ubud Palace and Market
- Traditional dance performance

Day 3: Adventure & Departure
- Sunrise at Mount Batur
- Visit Tanah Lot Temple
- Departure

