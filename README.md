# 🦷 Dental Appointment Management System

An AI-powered conversational dental appointment management system built with **LangGraph, LangChain, OpenAI, and Python**.

The application allows users to manage dental appointments using natural language. The AI agent understands the user's request, decides which tool to call, validates appointment information, and performs operations such as checking availability, booking, cancelling, and rescheduling appointments.

---

## 🚀 Features

The system supports:

- 🔍 Check available appointment slots
- 👨‍⚕️ Find doctors by specialization
- 📅 View patient appointments
- ✅ Book new appointments
- ❌ Cancel existing appointments
- 🔄 Reschedule appointments
- 🧠 Maintain conversational context across multiple turns
- 🛠️ Automatically select and execute the appropriate tool
- 🔎 Validate slot availability before booking
- ⚠️ Prevent duplicate or invalid bookings
- 👍 Ask for confirmation before cancelling appointments
- 💬 Collect missing information conversationally

---

## 🏗️ Architecture

### LangGraph ReAct Agent Design

The current implementation uses a **LangGraph ReAct agent** connected to multiple appointment-management tools.

The OpenAI language model acts as the reasoning component. It understands the user's request, decides whether a tool is required, selects the appropriate tool, observes the result, and continues until the task is completed.

```text
                         ┌──────────────────┐
                         │       User       │
                         └────────┬─────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │   LangGraph ReAct      │
                     │        Agent           │
                     └───────────┬────────────┘
                                 │
                                 ▼
                         ┌──────────────┐
                         │  OpenAI LLM  │
                         └──────┬───────┘
                                │
                         Understand Intent
                                │
                         Select Tool
                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
        ▼                       ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│ Information     │    │ Booking         │    │ Modification     │
│ Tools           │    │ Tools           │    │ Tools            │
├─────────────────┤    ├─────────────────┤    ├──────────────────┤
│ Available Slots │    │ Check Slot      │    │ Cancel           │
│ Patient Appts   │    │ Book Appointment│    │ Reschedule       │
│ Find Doctors    │    │                 │    │                  │
└────────┬────────┘    └────────┬────────┘    └─────────┬────────┘
         │                      │                       │
         └──────────────────────┼───────────────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │ doctor_availability.csv│
                    └───────────┬────────────┘
                                │
                                ▼
                           Tool Result
                                │
                                ▼
                         ┌──────────────┐
                         │  OpenAI LLM  │
                         └──────┬───────┘
                                │
                                ▼
                         Final Response
```

### Component Responsibilities

- **LangGraph ReAct Agent**  
  Controls the reasoning and tool-execution loop. It evaluates the conversation and determines what action should happen next.

- **OpenAI LLM**  
  Understands natural-language requests, extracts required information, decides when tools are needed, and generates responses.

- **Information Tools**  
  Retrieve doctor schedules, available appointment slots, specializations, and patient appointments.

- **Booking Tools**  
  Validate slot availability and create new appointments.

- **Cancellation Tool**  
  Cancels an existing appointment after appropriate validation and user confirmation.

- **Rescheduling Tool**  
  Moves an existing appointment to another available time slot.

- **CSV Data Layer**  
  Stores doctor schedules, availability information, and patient appointment data.

---

## 🛠️ Available Tools

The agent currently has access to seven appointment-management tools.

### Read Operations

- `get_available_slots`
- `get_patient_appointments`
- `check_slot_availability`
- `list_doctors_by_specialization`

### Write Operations

- `book_appointment`
- `cancel_appointment`
- `reschedule_appointment`

The language model does **not directly manipulate appointment data**.

Instead:

```text
LLM
 ↓
Select Tool
 ↓
Python Function
 ↓
CSV Data
 ↓
Tool Result
 ↓
LLM Response
```

This keeps the AI reasoning layer separate from deterministic business logic.

---

## 🔄 ReAct Execution Flow

The agent follows a reasoning and tool-execution loop:

```text
User Request
     ↓
Understand Intent
     ↓
Choose Tool
     ↓
Execute Tool
     ↓
Observe Result
     ↓
Need Another Action?
   /             \
 Yes              No
  ↓                ↓
Choose Tool     Final Response
  ↓
Continue
```

For example, a booking request may follow:

```text
Booking Request
      ↓
check_slot_availability
      ↓
   Available?
    /      \
  Yes       No
   ↓         ↓
book_      get_available_
appointment slots
   ↓         ↓
Success   Suggest Alternatives
```

---

## ⚙️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application development |
| **LangGraph** | Agent orchestration and ReAct workflow |
| **LangChain** | LLM integration and tool framework |
| **OpenAI** | Language model and reasoning |
| **Pandas** | CSV data processing |
| **Pydantic** | Data validation |
| **python-dotenv** | Environment variable management |
| **CSV** | Appointment data storage |

---

## 📁 Project Structure

```text
dental-appointment-langgraph-agent/
│
├── main.py
├── doctor_availability.csv
├── requirements.txt
├── README.md
├── .gitignore
│
└── dental_agent/
    │
    ├── agent.py
    ├── utils.py
    │
    ├── config/
    │   └── settings.py
    │
    ├── tools/
    │   ├── csv_reader.py
    │   └── csv_writer.py
    │
    ├── agents/
    ├── models/
    └── workflows/
```

### Important Files

#### `main.py`

Provides the interactive command-line interface and maintains conversation history across user turns.

#### `dental_agent/agent.py`

Creates the LangGraph ReAct agent, defines the system prompt, connects the OpenAI model, and registers available tools.

#### `dental_agent/utils.py`

Contains message-processing and sanitization utilities used before model calls.

#### `dental_agent/tools/csv_reader.py`

Contains tools for reading appointment and doctor information.

#### `dental_agent/tools/csv_writer.py`

Contains tools for booking, cancelling, and rescheduling appointments.

#### `dental_agent/config/settings.py`

Loads application configuration, environment variables, model settings, and file paths.

#### `doctor_availability.csv`

Acts as the application's appointment data store.

---

## 📊 Appointment Data

Appointment information is stored in:

```text
doctor_availability.csv
```

The data includes fields such as:

| Field | Description |
|---|---|
| `date_slot` | Appointment date and time |
| `specialization` | Dental specialization |
| `doctor_name` | Dentist name |
| `is_available` | Whether the slot is available |
| `patient_to_attend` | Patient ID if the slot is booked |

The expected date format is:

```text
M/D/YYYY H:MM
```

Example:

```text
8/8/2026 10:30
```

---

## 🦷 Supported Specializations

The system currently supports:

- General Dentist
- Oral Surgeon
- Orthodontist
- Cosmetic Dentist
- Prosthodontist
- Pediatric Dentist
- Emergency Dentist

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/harshuureddy/dental-appointment-langgraph-agent.git
```

Navigate into the project:

```bash
cd dental-appointment-langgraph-agent
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution temporarily:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

#### macOS/Linux

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The project uses dependencies such as:

```text
langgraph>=0.2.0
langchain>=0.3.0
langchain-core>=0.3.0
langchain-openai>=1.6.0
openai>=3.7.0
pandas>=2.0.0
python-dotenv>=1.0.0
pydantic>=2.0.0
```

---

## 🔑 Environment Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4.1-mini
TEMPERATURE=0
```

> Never commit your `.env` file or API key to GitHub.

Your `.gitignore` should include:

```gitignore
.env
venv/
.venv/
__pycache__/
*.pyc
.vscode/
.idea/
.DS_Store
Thumbs.db
```

---

## ▶️ Running the Application

Start the application with:

```bash
python main.py
```

You should see:

```text
╔══════════════════════════════════════════════════════════╗
║         Dental Appointment Management System             ║
║         Powered by LangGraph + OpenAI                    ║
╚══════════════════════════════════════════════════════════╝
```

Type:

```text
quit
```

to exit the application.

---

## 💬 Example Interactions

### Check Available Slots

```text
You: Show available slots for an orthodontist

Agent: Available slots for an orthodontist
(Dr. Kevin Anderson) are:

- 7/8/2026 8:00
- 7/8/2026 9:00
- 7/8/2026 11:00
...
```

---

### Find Doctors by Specialization

```text
You: Which doctors are orthodontists?

Agent: The orthodontist available is Dr. Kevin Anderson.
Would you like to know his available appointment slots
or book an appointment?
```

---

### Multi-Turn Appointment Booking

```text
You: Show available slots for an orthodontist

Agent: Here are the available slots...

You: 8/8/2026 10:30

Agent: The slot on 8/8/2026 at 10:30 with
Dr. Kevin Anderson is available.

Could you please provide your patient ID?

You: 232333

Agent: Your appointment with Dr. Kevin Anderson
on 8/8/2026 at 10:30 has been successfully booked.
```

This demonstrates conversational context because the user does not need to repeat the doctor and appointment information in every message.

---

### Check Patient Appointments

```text
You: What appointments does patient 1000048 have?

Agent: Patient 1000048 has the following appointments:

- 5/8/2026 9:00 with Dr. John Doe
- 6/8/2026 8:30 with Dr. John Doe
...
```

---

### Prevent Duplicate Booking

```text
You: Book patient 1000082 with Emily Johnson
on 7/8/2026 16:00

Agent: Patient 1000082 already has an appointment
with Dr. Emily Johnson on 7/8/2026 at 16:00.
```

The system checks existing appointment data instead of blindly creating duplicate bookings.

---

### Handle an Unavailable Slot

```text
You: Book patient 1000082 with Emily Johnson
on 5/10/2026 9:00

Agent: Dr. Emily Johnson does not have an available
slot on 5/10/2026 at 9:00.

Would you like me to find alternative available slots?
```

If requested, the agent can call `get_available_slots` and suggest alternatives.

---

### Cancel an Appointment

```text
You: Cancel appointment for patient 1000082
at 7/8/2026 16:00

Agent: Please confirm that you want to cancel
the appointment for patient 1000082.

You: yes confirmed

Agent: The appointment has been successfully cancelled.
```

The system requires user confirmation before executing the cancellation.

---

### Reschedule an Appointment

```text
You: Reschedule patient 1000082
from 7/8/2026 16:00
to 8/8/2026 10:30

Agent: I will verify the existing appointment
and check whether the requested new slot is available.
```

The system validates the existing appointment and target slot before modifying appointment data.

---

## 🧠 Key AI Engineering Concepts Demonstrated

### 1. Tool Calling

The language model determines which Python function is appropriate for a user's request.

For example:

```text
User:
"Show orthodontist appointments"

        ↓

OpenAI determines:
get_available_slots should be called

        ↓

Python tool reads CSV

        ↓

Tool result returned to model

        ↓

Natural-language response
```

This allows the LLM to interact with deterministic application logic.

---

### 2. ReAct Agent Pattern

The application demonstrates the ReAct-style pattern:

```text
Reason
  ↓
Choose Action
  ↓
Call Tool
  ↓
Observe Result
  ↓
Reason Again
  ↓
Final Answer
```

LangGraph orchestrates this execution loop.

---

### 3. Conversational Context

Conversation history is maintained across multiple user turns.

Example:

```text
User: Show orthodontist appointments

Agent: Here are the available slots...

User: 8/8/2026 10:30

Agent: Please provide your patient ID.

User: 232333

Agent: Appointment successfully booked.
```

The agent understands that the doctor, selected slot, and patient ID belong to the same booking conversation.

---

### 4. Validation Before Actions

Before booking an appointment, the system checks whether the requested slot is actually available.

```text
Booking Request
      ↓
check_slot_availability
      ↓
Available?
   /        \
 Yes         No
  ↓           ↓
Book       Suggest
           Alternatives
```

This prevents invalid appointment updates.

---

### 5. Human Confirmation

Potentially destructive operations such as cancellation require explicit user confirmation.

```text
Cancellation Request
        ↓
Identify Appointment
        ↓
Ask Confirmation
        ↓
User Confirms
        ↓
Cancel Appointment
```

---

### 6. Separation of AI and Business Logic

The system separates AI reasoning from application logic:

```text
LLM / Agent
    ↓
Tool Interface
    ↓
Python Business Logic
    ↓
CSV Data
```

The LLM determines **what action should happen**, while deterministic Python functions determine **how the operation is performed**.

This makes the application easier to maintain, test, and extend.

---

### 7. State and Multi-Turn Interaction

The application maintains conversation history so the agent can reason about earlier user messages.

Instead of requiring:

```text
Book patient 232333 with Kevin Anderson
on 8/8/2026 at 10:30
```

the system can support:

```text
User: Show orthodontist slots
Agent: ...

User: 8/8/2026 10:30
Agent: Please provide patient ID.

User: 232333
Agent: Appointment booked.
```

This creates a more natural conversational workflow.

---

## 🧪 Example Test Scenarios

The system can be tested with requests such as:

```text
Show available slots for an orthodontist
```

```text
Show available slots for Emily Johnson
```

```text
Which doctors are orthodontists?
```

```text
What appointments does patient 1000048 have?
```

```text
Book patient 1000082 with Emily Johnson on 7/8/2026 16:00
```

```text
Cancel appointment for patient 1000082 at 7/8/2026 16:00
```

```text
Reschedule patient 1000082 from 7/8/2026 16:00 to 8/8/2026 10:30
```

The agent can also handle incomplete requests by asking for missing information one detail at a time.

---

## 🔒 Security

API keys are loaded through environment variables rather than being stored directly in the Python source code.

```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

The `.env` file is excluded from Git using `.gitignore`.

Never commit real API keys or credentials to a public repository.

---

## 🔮 Future Improvements

Possible extensions include:

- FastAPI REST API
- Web-based chat interface
- PostgreSQL or MySQL instead of CSV
- User authentication
- Patient and staff roles
- Appointment reminders
- Email/SMS notifications
- Persistent LangGraph checkpoints
- Doctor-specific working hours
- Improved date/time validation
- Logging and monitoring
- Docker deployment
- Automated unit and integration tests
- Cloud deployment

A production-oriented architecture could look like:

```text
Frontend
    ↓
FastAPI
    ↓
LangGraph Agent
    ↓
OpenAI
    ↓
Tool Layer
    ↓
PostgreSQL
```

---

## 🎯 Project Purpose

This project demonstrates practical concepts used in modern AI engineering:

- Generative AI application development
- Agentic AI
- LangGraph
- LangChain
- OpenAI integration
- Tool calling
- ReAct agents
- Conversational state
- Business-rule validation
- CRUD-style operations
- Environment-based configuration
- Separation of AI reasoning and deterministic application logic

The project demonstrates how an LLM can move beyond simple text generation and interact with external application logic to complete real-world tasks.

---

## 📄 License

This project is intended for educational and portfolio purposes.
