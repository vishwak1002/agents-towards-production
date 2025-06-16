"""
Meeting Recorder Agent Event Handler

This module handles event-driven execution of the Meeting Recorder Agent.
It processes incoming execution requests from the xpander.ai platform and
manages the agent's lifecycle for meeting recording tasks.
"""

import json
from xpander_utils.events import XpanderEventListener, AgentExecutionResult, AgentExecution, ExecutionStatus
from xpander_sdk import XpanderClient

from meeting_recorder_agent import MeetingAgent

# === Load Configuration ===
# Reads API credentials and organization context from a local JSON file
# This file should contain your xpander.ai API key and agent ID
with open('xpander_config.json', 'r') as config_file:
    xpander_config: dict = json.load(config_file)

# === Initialize Event Listener ===
# Create a listener to subscribe to execution requests from specified agent(s)
# This enables the agent to respond to events from the xpander.ai platform
listener = XpanderEventListener(**xpander_config)

# Initialize xpander client for API interactions
xpander = XpanderClient(api_key=xpander_config.get("api_key"))

# === Define Execution Handler ===
async def on_execution_request(execution_task: AgentExecution) -> AgentExecutionResult:
    """
    Callback triggered when an execution request is received from a registered agent.
    This is the main entry point for processing meeting recording tasks.
    
    Args:
        execution_task (AgentExecution): Object containing execution metadata and input.
            This includes the meeting details and requested actions.

    Returns:
        AgentExecutionResult: Object describing the output of the execution.
            Contains the result of the meeting recording task and success status.
    """
    
    # Initialize agent instance from xpander.ai platform
    agent = xpander.agents.get(agent_id=xpander_config.get("agent_id"))
    
    # Initialize the agent with the current task
    # This sets up the context for the meeting recording operation
    agent.init_task(execution=execution_task.model_dump()) 
    
    # Create and initialize the MeetingAgent instance
    # This handles the actual meeting recording logic
    my_agent = MeetingAgent(agent=agent)
    
    # Run the agent's main execution loop
    # This processes the meeting recording task and returns the result
    exec_status = await my_agent._agent_loop() 
    
    # Return the execution result to the xpander.ai platform
    return AgentExecutionResult(
        result=exec_status.result,
        is_success=exec_status.status == ExecutionStatus.COMPLETED,
    )

# === Register Callback ===
# Attach the execution handler to the event listener
# This connects the handler to the xpander.ai platform's event system
listener.register(on_execution_request=on_execution_request)