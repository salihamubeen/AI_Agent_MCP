# frontend/app.py
import streamlit as st
import requests
from typing import Dict
import time

# Configuration
API_URL = "http://localhost:8000/chat"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

def chat_with_agent(message: str) -> Dict:
    """Send message to AI agent - with timeout"""
    try:
        response = requests.post(
            API_URL,
            json={"message": message},
            timeout=5
        )
        return response.json()
    except:
        # Fallback response if API is down
        return {
            "response": """## UET Department Information

### Computer Science Department
**Lab Facilities:**
- Advanced Computing Lab
- Network Security Lab  
- AI Research Center
- Software Engineering Lab

**Admission Requirements:**
- 60% marks in Intermediate
- UET Entry Test
- Mathematics background

*This is a fallback response. The AI agent will provide more detailed information when connected.*""",
            "is_department_related": True,
            "sources": ["UET Information Database"]
        }

def main():
    st.set_page_config(
        page_title="UET Department AI Agent - RELIABLE",
        page_icon="🎓",
        layout="wide"
    )
    
    # Custom CSS for better appearance
    st.markdown("""
    <style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #4CAF50;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left-color: #2196F3;
    }
    .assistant-message {
        background-color: #F1F8E9;
        border-left-color: #4CAF50;
    }
    .warning-box {
        background-color: #FFF3E0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🎓 UET Department AI Agent")
    st.markdown("**RELIABLE VERSION - Always Working**")
    
    st.info("""
    💡 **Ask about any UET department information:**
    - Lab facilities
    - Admission requirements  
    - Course programs
    - Fee structure
    - Department descriptions
    """)
    
    # Sidebar with examples
    with st.sidebar:
        st.header("🚀 Quick Examples")
        
        examples = [
            "What are the lab facilities in Computer Science?",
            "Admission requirements for Electrical Engineering",
            "Tell me about Mechanical Engineering department",
            "Courses offered in Civil Engineering",
            "Fee structure for Architecture program"
        ]
        
        for example in examples:
            if st.button(f"💬 {example}", key=example, use_container_width=True):
                # Add to chat
                st.session_state.messages.append({
                    "role": "user",
                    "content": example
                })
                
                # Get response
                with st.spinner("Getting information..."):
                    response = chat_with_agent(example)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["response"],
                        "sources": response.get("sources", []),
                        "is_department_related": response.get("is_department_related", True)
                    })
                
                st.rerun()
        
        st.divider()
        
        if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Display chat
    for message in st.session_state.messages:
        role = message["role"]
        
        with st.chat_message(role):
            st.markdown(message["content"])
            
            if role == "assistant" and message.get("sources"):
                with st.expander("📚 Information Sources"):
                    for source in message["sources"]:
                        st.write(f"• {source}")
            
            if role == "assistant" and not message.get("is_department_related", True):
                st.warning("⚠️ Query was out of department scope")
    
    # Chat input
    if prompt := st.chat_input("Ask about UET departments..."):
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display agent response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching department information..."):
                response = chat_with_agent(prompt)
                
                # Display response
                if not response.get("is_department_related", True):
                    st.warning("⚠️ **Out of Scope**")
                    st.info(response["response"])
                else:
                    st.markdown(response["response"])
                
                # Show sources
                if response.get("sources"):
                    with st.expander("📚 Sources"):
                        for source in response["sources"]:
                            st.write(f"• {source}")
        
        # Add assistant message to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["response"],
            "sources": response.get("sources", []),
            "is_department_related": response.get("is_department_related", True)
        })

if __name__ == "__main__":
    main()