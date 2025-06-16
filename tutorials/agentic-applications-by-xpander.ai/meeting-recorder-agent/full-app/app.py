"""
Meeting Recorder Agent CLI Application

This module provides a command-line interface for interacting with the Meeting Recorder Agent.
It allows users to chat with the agent and perform meeting recording tasks through a simple
text-based interface.
"""

import os
import asyncio
from dotenv import load_dotenv
from xpander_sdk import XpanderClient, Agent

from meeting_recorder_agent import MeetingAgent

# === Load Configuration ===
load_dotenv()
# Initialize xpander client for API interactions
xpander_client = XpanderClient(api_key=os.getenv("XPANDER_API_KEY"))

# Load the Meeting Recorder Agent from xpander.ai platform
xpander_agent: Agent = xpander_client.agents.get(agent_id=os.getenv("XPANDER_AGENT_ID"))

async def main():
    """
    Main entry point for the CLI application.
    Initializes the agent and starts an interactive chat session.
    """
    # Initialize the Meeting Recorder Agent
    agent = MeetingAgent(xpander_agent)
    
    # Start the agent with a greeting message
    # This initializes the conversation and returns a thread ID
    thread = await agent.chat(
        "Hi!, what can you do?"
    )
    
    # Main interaction loop
    # Continuously reads user input and processes it through the agent
    while True:
        user_input = input("You: ")
        # Process the user's input and maintain conversation context using the thread ID
        thread = await agent.chat(user_input, thread)          

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())