# Meeting Recorder Agent

This directory contains a production-ready Meeting Recorder Agent implementation using the xpander.ai SDK, demonstrating how to build an autonomous agent that can manage meeting recordings and summaries.

## Overview

The Meeting Recorder Agent is designed to automate meeting workflows by:
- Connecting to Google Calendar to find upcoming meetings
- Scheduling and initiating meeting recordings
- Checking recorder status and retrieving post-meeting assets (video & transcript)
- Generating meeting summaries and PDF agendas
- Emailing meeting assets and summaries to participants
- Maintaining memory and context across multiple sessions

## Directory Structure

```
meeting-recorder-agent/
├── app.py                      # CLI entry point for the agent
├── meeting_recorder_agent.py   # Main agent implementation
├── xpander_handler.py          # Event handler for platform events
├── agent_instructions.json     # Agent persona configuration
├── xpander_config.json         # API credentials configuration
├── Dockerfile                  # Container definition for deployment
├── providers/
│   ├── ai_frameworks/          # Framework integrations
│   └── llms/                   # LLM provider implementations
│       └── openai/             # OpenAI specific implementation
└── tools/
    ├── local_tools.py          # Custom tool implementations
    └── async_function_caller.py # Async function caller utility
```

## Getting Started

### Prerequisites

- Python 3.10+ (3.10.0 or higher)
- Node.js for the xpander CLI
- xpander-sdk and xpander-utils (installed via requirements.txt)
- [xpander.ai](https://xpander.ai/) account
- Google Calendar API credentials (for calendar integration)
- OpenAI API key (for LLM capabilities)

### Installation

1. Create and activate a Python virtual environment:

```bash
# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Setting Up Your Agent

You have two options to set up the agent on xpander.ai:

#### Option 1: Use the Template (Recommended)

1. Log in to your [app.xpander.ai](https://app.xpander.ai) account
2. Inside "Agents" Click on Templates and select "Meeting Recorder Template"
3. Click "Import Template" to add it to your workspace
4. Once imported, from the AI Agent Workbench, click on the SDK Trigger
5. Copy your **Agent ID** and **API Key**

Learn more about getting started with xpander workbench in the [official documentation](https://docs.xpander.ai/docs/01-get-started/02-getting-started-01-workbench).

#### Option 2: Manual Setup

If you prefer to build the agent manually:

1. Log in to your [app.xpander.ai](https://xpander.ai) account
2. Click "Create New Agent" from your dashboard and skip the Planner step
3. Add the following tools to your agent from the Built-in actions menu:
   - **Check Recorder Status** tool
   - **Create Meeting Recording Bot** tool
   - **Send Email with Content** tool
4. Add the following tool to your agent from the Google Calendar app:
   - **Get Calendar Events by ID** tool
5. Save your agent and copy your **Agent ID** and **API Key** from the SDK Trigger

For detailed instructions on adding tools to your agent, refer to the [Adding Tools to Agents](https://docs.xpander.ai/docs/02-agent-builder/02-add-tools-to-agents) documentation.

3.  Configure your environment: 
Create a `.env` file in the project root with the required keys and settings:

```
OPENAI_API_KEY=your_openai_key
XPANDER_API_KEY=your_xpander_key 
XPANDER_AGENT_ID=your_agent_id
```

## 📚 How It Works

The agent uses two main components:

1. **Main App (`app.py`)**: Coordinates everything 
2. **Meeting Agent (`meeting_agent.py`)**: Connects to xpander.ai to run the agent

The agent leverages xpander.ai's built-in thread-based memory system to maintain conversation context and remember meeting details across sessions.

### Agent Tools

<table>
<tr>
  <td width="25%" align="center">
    <h4>🔎<br>Check Recorder Status</h4>
  </td>
  <td>
    Queries the status of recording bots and retrieves information about recordings:
    <ul>
      <li>Shows if recordings are in progress or completed</li>
      <li>Provides links to video, audio, and transcript downloads</li>
      <li>Displays metadata like duration and participants</li>
    </ul>
  </td>
</tr>
<tr>
  <td width="25%" align="center">
    <h4>🤖<br>Create Recording Bot</h4>
  </td>
  <td>
    Creates and deploys a new bot to record a Google Meet session:
    <ul>
      <li>Accepts Google Meet URLs in any format</li>
      <li>Automatically joins meetings using specified credentials</li>
      <li>Creates a dedicated recorder ID for tracking</li>
    </ul>
  </td>
</tr>
<tr>
  <td width="25%" align="center">
    <h4>📧<br>Send Email Content</h4>
  </td>
  <td>
    Sends meeting summaries and recordings via email:
    <ul>
      <li>Sends transcript summaries to meeting participants</li>
      <li>Attaches or links to recording files</li>
      <li>Supports customized email templates</li>
    </ul>
  </td>
</tr>
<tr>
  <td width="25%" align="center">
    <h4>📅<br>Get Calendar Events</h4>
  </td>
  <td>
    Connects with your Google Calendar:
    <ul>
      <li>Fetches upcoming and past calendar events</li>
      <li>Links calendar events to meeting recordings</li>
      <li>Provides scheduling information for the agent</li>
    </ul>
  </td>
</tr>
</table>

### Running the Agent

#### CLI Mode

first login to xpander.ai
```bash
xpander login
```

Run the agent in interactive command-line mode:

```bash
python app.py
```

This starts a conversation with the agent where you can interact with it directly.

Example output:
```
2025-05-27 21:15:18.436 | INFO     | meeting_recorder_agent:chat:80 - 🧠 Adding task to a new thread
2025-05-27 21:15:21.590 | INFO     | meeting_recorder_agent:_agent_loop:115 - 🪄 Starting Agent Loop
2025-05-27 21:15:25.275 | INFO     | meeting_recorder_agent:_agent_loop:121 - --------------------------------------------------------------------------------
2025-05-27 21:15:25.276 | INFO     | meeting_recorder_agent:_agent_loop:122 - 🔍 Step 1
2025-05-27 21:15:29.686 | INFO     | providers.llms.openai.async_client:invoke_model:87 - 🔄 Model response received in 3.78 s
2025-05-27 21:15:29.687 | INFO     | providers.llms.openai.async_client:invoke_model:93 - 🔄 Tool call function name: xpfinish-agent-execution-finished
2025-05-27 21:15:34.801 | INFO     | meeting_recorder_agent:_agent_loop:179 - ✅ xpfinish-agent-execution-finished
2025-05-27 21:15:34.802 | INFO     | meeting_recorder_agent:_agent_loop:181 - 🔢 Step 1 tokens used: 2436 (output: 144, input: 2292)
2025-05-27 21:15:36.571 | INFO     | meeting_recorder_agent:_agent_loop:187 - ✨ Execution duration: 14.98 s
2025-05-27 21:15:36.573 | INFO     | meeting_recorder_agent:_agent_loop:190 - 🔢 Total tokens used: 2436 (output: 144, input: 2292)
2025-05-27 21:15:37.113 | INFO     | meeting_recorder_agent:chat:84 - --------------------------------------------------------------------------------
2025-05-27 21:15:37.114 | INFO     | meeting_recorder_agent:chat:85 - 🤖 Agent response: Hello! Here are some of the things I can do for you:

- Record your video meetings by creating a meeting recorder bot and provide you with the recording status and assets.
- Retrieve and manage events from your calendar, including sending notifications or summaries via email.
- Generate and export a weekly meeting agenda as a PDF from your list of meetings.
- Send crafted email notifications or alerts with custom content.

If you have a specific task in mind, just let me know and I'll help you with it!
You: 
```

#### Event-Driven Mode

Run the agent in event-driven mode to handle events from the xpander.ai platform:

```bash
python xpander_handler.py
```

When running correctly, the agent will start and wait for incoming events from the xpander.ai platform. There won't be immediate output unless an event is received.

Note: Make sure to use python3 if your system doesn't recognize the python command:

```bash
python3 xpander_handler.py
```

## Usage Examples

### Add Calendar Integration

This agent is configured to retrieve upcoming meetings from your connected Google Calendar. You can ask it to look up your schedule and include key details about each meeting.

During a conversation with the agent, try sending a message like:
```
List my upcoming meetings on <DATE> and the three consecutive days, for each meeting, include: title, description (if available), location, time, participants
```
The agent will process your request, call the calendar tool, and return a nicely formatted list of meetings with all the details you requested.

Example output:
```
2025-05-27 21:28:04.970 | INFO     | meeting_recorder_agent:chat:77 - 🧠 Adding task to existing thread: fb6b4ed0-d39e-4129-ad59-d2f508f29db1
2025-05-27 21:28:09.065 | INFO     | meeting_recorder_agent:_agent_loop:115 - 🪄 Starting Agent Loop
2025-05-27 21:28:10.209 | INFO     | meeting_recorder_agent:_agent_loop:121 - --------------------------------------------------------------------------------
2025-05-27 21:28:10.209 | INFO     | meeting_recorder_agent:_agent_loop:122 - 🔍 Step 1
2025-05-27 21:28:12.225 | INFO     | providers.llms.openai.async_client:invoke_model:87 - 🔄 Model response received in 1.40 s
2025-05-27 21:28:12.225 | INFO     | providers.llms.openai.async_client:invoke_model:93 - 🔄 Tool call function name: CalendarEventManagementGetCalendarEventsById
2025-05-27 21:28:20.334 | INFO     | meeting_recorder_agent:_agent_loop:179 - ✅ CalendarEventManagementGetCalendarEventsById
2025-05-27 21:28:20.334 | INFO     | meeting_recorder_agent:_agent_loop:181 - 🔢 Step 1 tokens used: 2400 (output: 67, input: 2333)
2025-05-27 21:28:21.421 | INFO     | meeting_recorder_agent:_agent_loop:121 - --------------------------------------------------------------------------------
2025-05-27 21:28:21.422 | INFO     | meeting_recorder_agent:_agent_loop:122 - 🔍 Step 2
2025-05-27 21:28:25.683 | INFO     | providers.llms.openai.async_client:invoke_model:87 - 🔄 Model response received in 3.68 s
2025-05-27 21:28:25.684 | INFO     | providers.llms.openai.async_client:invoke_model:93 - 🔄 Tool call function name: xpfinish-agent-execution-finished
2025-05-27 21:28:32.740 | INFO     | meeting_recorder_agent:_agent_loop:179 - ✅ xpfinish-agent-execution-finished
2025-05-27 21:28:32.741 | INFO     | meeting_recorder_agent:_agent_loop:181 - 🔢 Step 2 tokens used: 6013 (output: 337, input: 5676)
2025-05-27 21:28:34.478 | INFO     | meeting_recorder_agent:_agent_loop:187 - ✨ Execution duration: 25.41 s
2025-05-27 21:28:34.480 | INFO     | meeting_recorder_agent:_agent_loop:190 - 🔢 Total tokens used: 8413 (output: 404, input: 8009)
2025-05-27 21:28:35.020 | INFO     | meeting_recorder_agent:chat:84 - --------------------------------------------------------------------------------
2025-05-27 21:28:35.021 | INFO     | meeting_recorder_agent:chat:85 - 🤖 Agent response: Here are your meetings from your Google Calendar for the next 3 days (27–29 May 2025):

---

**1. Onboarding to xpander**
- **Date:** 27 May 2025
- **Time:** 15:30–16:00 (Asia/Jerusalem)
- **Location:** Google Meet Link (https://meet.google.com/ ....)
- **Attendees:** Daniel, Or, David

**2. AWS Summit Tel Aviv**
- **Date:** 28 May 2025
- **Time:** 08:00–17:30 (Asia/Jerusalem)
- **Location:** EXPO Tel Aviv, Pavilion 1, 101 Rokach Blvd
---

Let me know if you need more details or want this as a PDF!
```

### Create a Meeting Recorder Bot 

This agent is configured to create a meeting recorder bot for a given Google Meet URL. You can ask it to create a recorder for a specific meeting and it will do so.

During a conversation with the agent, try sending a message like:
```
Create a meeting recorder bot for the following Google Meet URL: https://meet.google.com/okf-ntry-xtg
```
or :
```
Create a recorder for the <MEETING_TITLE>.
```

Check the recorder status:

```
Check the recorder status and give me the asset links if done.
```

### Generate a Meeting Summary and send it via email

```
Email the video & transcript to <YOUR_EMAIL> with a summary
```

## Agent Capabilities

The Meeting Recorder Agent demonstrates several key capabilities:

- **Framework-Agnostic Design**: Built without tight coupling to any specific AI framework
- **Asynchronous Processing**: Utilizes Python's asyncio for non-blocking operations
- **Tool Integration**: Uses both local and cloud-based tools
- **Memory Management**: Maintains conversation context across interactions
- **Observability**: Logs detailed execution metrics and token usage
- **Multi-Step Reasoning**: Coordinates complex reasoning chains

## Local Tools

The agent includes local tools:

1. `export_meeting_schedule_pdf`: Generates formatted PDF agendas

## Customization

### Changing Instructions

Modify the `agent_instructions.json` file to customize the agent's behavior:
```json
{
    "role": "Meeting Recorder Assistant",
    "goal": "Automate meeting recording and summary workflows",
    "general": "Detailed instructions for handling meetings..."
}
```

### Switching LLM Providers

By default, the agent uses OpenAI. To switch to a different provider:

```python
# In my_agent.py
llm_provider = LLMProvider.ANTHROPIC  # Or another supported provider

# During initialization
self.agent.select_llm_provider(llm_provider)
```

### Adding Custom Tools

Add new tools by extending `local_tools.py` with additional functions and tool declarations.

## Deployment

Deploy the agent to xpander.ai's managed infrastructure:

```bash
xpander deploy
```

Monitor the deployed agent's logs:

```bash
xpander logs
```

## Troubleshooting

- **Calendar Integration Issues**: Verify Google Calendar API authentication 
 **Missing Dependencies**: Ensure all requirements are installed
- **Tool Execution Errors**: Check the logs for detailed error messages
## Additional Resources

- [xpander.ai Documentation](https://docs.xpander.ai)
- [SDK API Reference](https://docs.xpander.ai/api-reference/07-sdk)
- [Example Library](https://github.com/xpander-ai/xpander.ai/tree/main/examples) 

## Exploring the Code

To better understand how the agent works, here are the key files to examine:

1. **meeting_recorder_agent.py**: The core agent implementation that handles:
   - Initialization with xpander.ai SDK
   - The agent reasoning loop with `_agent_loop()`
   - Tool execution flow
   - Token usage tracking and metrics

2. **xpander_handler.py**: Event-driven architecture implementation showing:
   - How to register event handlers with the xpander platform
   - Processing incoming execution requests
   - Returning structured results

3. **tools/local_tools.py**: Example tool implementations with:
   - Function definitions
   - Tool schema declarations
   - Helper utilities for tool registration

The code is structured to demonstrate best practices for building AI agents with xpander.ai, including:

- Clean separation of concerns
- Asynchronous processing
- Structured error handling
- Detailed logging
- Modular tool implementation

When modifying the agent, start by examining these files to understand the execution flow before making changes. 