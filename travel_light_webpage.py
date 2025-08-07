import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

####################
# Page Configuration
st.set_page_config(page_title="Travel Light - AI Travel Planner", page_icon="✈️")
st.title("✈️ Travel Light - AI Travel Planning Assistant")

# Check for OpenAI API Key
if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ OpenAI API Key not found!")
    st.markdown("""
    **To use the full AI-powered version:**
    1. Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
    2. Create a `.env` file in this directory
    3. Add: `OPENAI_API_KEY=your_api_key_here`
    4. Restart the app
    
    **For now, you can try the demo version below:**
    """)
    
    # Demo mode
    st.markdown("### 🎮 Demo Mode")
    demo_input = st.text_input("Try: 'Plan a 3-day budget trip to Bali'")
    if demo_input:
        st.success("🎉 Demo mode would process your request with AI agents!")
        st.info("💡 Get an API key to experience the full AI-powered travel planning!")
    
    st.stop()

# Try to import the travel graph
try:
    from travel_graph import build_conversation_graph
    graph = build_conversation_graph()
    ai_mode = True
except ImportError as e:
    st.error(f"❌ Could not import travel planning system: {e}")
    st.info("💡 Make sure all files are in the same directory")
    st.stop()
except Exception as e:
    st.error(f"❌ Error initializing AI system: {e}")
    st.info("💡 Check your API key and internet connection")
    st.stop()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "graph_state" not in st.session_state:
    st.session_state["graph_state"] = {"messages": []}
if "summary" not in st.session_state:
    st.session_state["summary"] = ""

# Sidebar with information
with st.sidebar:
    st.markdown("### 🎯 How to Use")
    st.markdown("""
    1. **Ask for a trip plan** (e.g., "Plan a 3-day budget trip to Tokyo")
    2. **Review the itinerary** the AI creates
    3. **Confirm** if you like it
    4. **Get hotel & flight options**
    5. **Export** your conversation as PDF
    """)
    
    st.markdown("### 💡 Example Requests")
    st.markdown("""
    - "Plan a 5-day luxury trip to Paris"
    - "I want a 2-day budget trip to New York"
    - "Create a 7-day mid-range itinerary for Japan"
    """)
    
    st.markdown("### 🔧 Features")
    st.markdown("""
    ✅ AI-powered itinerary planning
    ✅ Hotel search (with Amadeus API)
    ✅ Flight search (with AviationStack API)
    ✅ Multi-agent conversation system
    ✅ PDF export functionality
    """)

# Display Chat History
st.markdown("### 💬 Conversation")
for msg in st.session_state["messages"]:
    role_display = "🧑‍💼 You" if msg["role"] == "user" else "🤖 Travel AI"
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
user_input = st.chat_input("Type your travel request here...")

# Buttons
col1, col2, col3 = st.columns(3)
with col1:
    reset_button = st.button("🔄 Reset")
with col2:
    debug_mode = st.checkbox("🐛 Debug Mode")
with col3:
    if st.session_state["messages"]:
        export_pdf = st.button("📄 Export PDF")

# Handle Reset
if reset_button:
    st.session_state["messages"] = []
    st.session_state["graph_state"] = {"messages": []}
    st.session_state["summary"] = ""
    st.rerun()

# Handle User Input
if user_input and user_input.strip():
    # Append user message
    user_msg = {"role": "user", "content": user_input.strip()}
    st.session_state["messages"].append(user_msg)
    st.session_state["graph_state"]["messages"].append(user_msg)

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Show AI is thinking
    with st.chat_message("assistant"):
        with st.spinner("🤖 AI is planning your trip..."):
            try:
                # Invoke the graph
                result = graph.invoke(st.session_state["graph_state"])
                bot_messages = result.get("messages", [])

                # Process and display bot response
                if bot_messages:
                    # Get the latest message content
                    latest_bot_msg = bot_messages[-1]
                    if hasattr(latest_bot_msg, 'content'):
                        bot_content = latest_bot_msg.content
                    else:
                        bot_content = str(latest_bot_msg)
                    
                    bot_msg = {"role": "assistant", "content": bot_content}
                    st.session_state["messages"].append(bot_msg)
                    st.session_state["graph_state"]["messages"].append(bot_msg)
                    
                    # Display the response
                    st.markdown(bot_content)
                    
                    # Create summary
                    st.session_state["summary"] = "\n".join(
                        getattr(m, 'content', str(m)) for m in bot_messages 
                        if getattr(m, 'role', 'assistant') == 'assistant'
                    )
                else:
                    error_msg = "The AI didn't return a response. Please try again."
                    st.error(error_msg)
                    st.session_state["messages"].append({"role": "assistant", "content": error_msg})
                    
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state["messages"].append({"role": "assistant", "content": error_msg})

    # Debug Output
    if debug_mode:
        st.markdown("---")
        st.markdown("### 🐛 Debug Information")
        st.json(st.session_state["graph_state"])
        st.markdown("---")

# Summary Section
if st.session_state["summary"]:
    with st.expander("📝 View Conversation Summary"):
        st.text(st.session_state["summary"])

# PDF Export
class CustomPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Travel Light - AI Travel Planning', ln=True, align='C')
        self.ln(10)

    def add_conversation(self, messages):
        self.set_font('Arial', '', 10)
        for msg in messages:
            role = "You:" if msg['role'] == 'user' else "Travel AI:"
            self.set_font('Arial', 'B', 10)
            self.multi_cell(0, 5, role)
            self.set_font('Arial', '', 10)
            self.multi_cell(0, 5, msg['content'])
            self.ln(2)

def export_conversation_pdf(messages: list) -> str:
    pdf = CustomPDF()
    pdf.add_page()
    pdf.add_conversation(messages)
    filename = f"travel_light_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# Handle PDF Export
if export_pdf and st.session_state["messages"]:
    try:
        filename = export_conversation_pdf(st.session_state["messages"])
        with open(filename, "rb") as file:
            st.download_button(
                label="📄 Download Conversation PDF",
                data=file,
                file_name=filename,
                mime="application/pdf"
            )
        st.success(f"✅ PDF exported as {filename}")
    except Exception as e:
        st.error(f"❌ Error exporting PDF: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🚀 Powered by OpenAI GPT & LangGraph | Made with ❤️ for travelers</p>
</div>
""", unsafe_allow_html=True)
            