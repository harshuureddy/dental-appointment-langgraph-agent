

````markdown
# 🦷 Dental Appointment Management System

An AI-powered conversational dental appointment management system built with **LangGraph, LangChain, OpenAI, and Python**.

The application allows users to interact with a dental appointment system using natural language. The AI agent understands the user's request, decides which tool to call, validates appointment information, and performs operations such as checking availability, booking, cancelling, and rescheduling appointments.

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

---

## 🧠 How It Works

The project uses a **LangGraph ReAct agent** connected to a set of appointment-management tools.

The OpenAI language model acts as the reasoning component of the system. Based on the user's request, it decides whether it needs to call a tool.

```text
                 User
                   │
                   ▼
           ┌─────────────────┐
           │ LangGraph Agent │
           │   (ReAct Loop)  │
           └────────┬────────┘
                    │
                    ▼
             ┌─────────────┐
             │ OpenAI LLM  │
             └──────┬──────┘
                    │
             Does it need a tool?
                /          \
              Yes           No
               │             │
               ▼             ▼
        ┌──────────────┐   Direct
        │ Dental Tools │   Response
        └──────┬───────┘
               │
               ▼
      doctor_availability.csv
               │
               ▼
         Tool Result
               │
               └────────► LLM
                            │
                            ▼
                      Final Response
````

The agent can repeatedly reason, call tools, inspect tool results, and continue until the user's request is completed.

---

# 🛠️ Available Tools

The agent currently has access to the following tools:

### Read Operations

* `get_available_slots`
* `get_patient_appointments`
* `check_slot_availability`
* `list_doctors_by_specialization`

### Write Operations

* `book_appointment`
* `cancel_appointment`
* `reschedule_appointment`

This separation keeps appointment-management logic outside the LLM itself.

The language model decides **when to use a tool**, while Python functions perform the actual data operations.

---

# ⚙️ Technology Stack

| Technology        | Purpose                                |
| ----------------- | -------------------------------------- |
| **Python**        | Core application                       |
| **LangGraph**     | Agent orchestration and ReAct workflow |
| **LangChain**     | LLM and tool integration               |
| **OpenAI**        | Language model and reasoning           |
| **Pandas**        | CSV data processing                    |
| **Pydantic**      | Data validation                        |
| **python-dotenv** | Environment variable management        |
| **CSV**           | Appointment data storage               |

---

# 📁 Project Structure

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

**`main.py`**

Provides the interactive command-line interface and maintains conversation history.

**`dental_agent/agent.py`**

Creates the LangGraph ReAct agent, defines the system prompt, connects the OpenAI model, and registers the available tools.

**`dental_agent/tools/csv_reader.py`**

Contains tools for reading appointment information.

**`dental_agent/tools/csv_writer.py`**

Contains tools for booking, cancelling, and rescheduling appointments.

**`dental_agent/config/settings.py`**

Loads environment variables and application configuration.

**`doctor_availability.csv`**

Acts as the application's appointment data store.

---

# 📊 Appointment Data

Appointment information is stored in:

```text
doctor_availability.csv
```

Example structure:

| Field               | Description                      |
| ------------------- | -------------------------------- |
| `date_slot`         | Appointment date and time        |
| `specialization`    | Dental specialization            |
| `doctor_name`       | Dentist name                     |
| `is_available`      | Whether the slot is available    |
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

# 🦷 Supported Specializations

The system currently supports:

* General Dentist
* Oral Surgeon
* Orthodontist
* Cosmetic Dentist
* Prosthodontist
* Pediatric Dentist
* Emergency Dentist

---

# 📦 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/harshuureddy/dental-appointment-langgraph-agent.git
```

Navigate into the project:

```bash
cd dental-appointment-langgraph-agent
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution temporarily:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example dependencies:

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

# 🔑 Environment Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4.1-mini
TEMPERATURE=0
```

> Never commit your `.env` file or API key to GitHub.

The `.gitignore` should include:

```gitignore
.env
venv/
.venv/
__pycache__/
*.pyc
.vscode/
```

---

# ▶️ Running the Application

Start the system with:

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

# 💬 Example Interactions

## Check Available Slots

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

## Find Doctors by Specialization

```text
You: Which doctors are orthodontists?

Agent: The orthodontist available is Dr. Kevin Anderson.
Would you like to see his available appointment slots?
```

---

## Book an Appointment

```text
You: Show available slots for an orthodontist

Agent: Here are the available slots...

You: 8/8/2026 10:30

Agent: The slot is available.
Could you please provide your patient ID?

You: 232333

Agent: Your appointment with Dr. Kevin Anderson
on 8/8/2026 at 10:30 has been successfully booked.
```

This demonstrates multi-turn conversational context.

---

## Prevent Duplicate Booking

```text
You: Book patient 1000082 with Emily Johnson
on 7/8/2026 16:00

Agent: Patient 1000082 already has an appointment
with Dr. Emily Johnson on 7/8/2026 at 16:00.
```

---

## Handle an Unavailable Slot

```text
You: Book patient 1000082 with Emily Johnson
on 5/10/2026 9:00

Agent: Dr. Emily Johnson does not have an available
slot at that time.

Would you like me to find alternative available slots?
```

---

## View Patient Appointments

```text
You: What appointments does patient 1000048 have?

Agent: Patient 1000048 has the following appointments:

- 5/8/2026 9:00 with Dr. John Doe
- 6/8/2026 8:30 with Dr. John Doe
...
```

---

## Cancel an Appointment

```text
You: Cancel appointment for patient 1000082
at 7/8/2026 16:00

Agent: Please confirm that you want to cancel
the appointment.

You: yes confirmed

Agent: The appointment has been successfully cancelled.
```

The system requires confirmation before performing the cancellation.

---

## Reschedule an Appointment

```text
You: Reschedule patient 1000082
from 7/8/2026 16:00
to 8/8/2026 10:30

Agent: I will verify the existing appointment
and check whether the requested new slot is available.
```

The system validates the appointment before modifying the data.

---

# 🔄 Agent Workflow

A typical booking request follows this flow:

```text
User Request
     │
     ▼
OpenAI Model
     │
     ▼
Understand Intent
     │
     ▼
Select Tool
     │
     ▼
check_slot_availability
     │
     ├── Available ──► book_appointment
     │
     └── Unavailable ──► get_available_slots
                              │
                              ▼
                      Suggest Alternatives
```

This demonstrates how LLM-based agents can combine reasoning with deterministic application logic.

---

# 🧠 Key AI Engineering Concepts Demonstrated

## 1. Tool Calling

The language model does not directly manipulate appointment data.

Instead, it selects Python tools such as:

```text
check_slot_availability
book_appointment
cancel_appointment
reschedule_appointment
```

The Python tool performs the operation and returns the result to the model.

---

## 2. ReAct Agent Pattern

The agent follows a loop similar to:

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

LangGraph manages this agent execution workflow.

---

## 3. Conversational Context

Conversation history is maintained so users can provide information incrementally.

Example:

```text
User: Show orthodontist appointments

Agent: Here are the available slots...

User: 8/8/2026 10:30

Agent: Please provide your patient ID.

User: 232333

Agent: Appointment successfully booked.
```

The agent understands that the date and patient ID belong to the same booking request.

---

## 4. Validation Before Actions

Before booking, the system checks whether a slot is actually available.

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

---

## 5. Human Confirmation

Potentially destructive operations such as cancellation require user confirmation before execution.

```text
Cancellation Request
        ↓
Find Appointment
        ↓
Ask Confirmation
        ↓
User Confirms
        ↓
Cancel Appointment
```

---

## 6. Separation of AI and Business Logic

The project separates:

```text
LLM / Agent
    ↓
Tool Interface
    ↓
Python Business Logic
    ↓
CSV Data
```

The LLM decides **what action should happen**, while deterministic Python functions decide **how the action is performed**.

This makes the system easier to test, maintain, and extend.

---

# 🔮 Future Improvements

Possible extensions include:

* FastAPI REST API
* Web-based chat interface
* PostgreSQL/MySQL database instead of CSV
* User authentication
* Appointment reminders
* Email/SMS notifications
* Persistent LangGraph checkpoints
* Doctor-specific working hours
* Date/time validation
* Logging and monitoring
* Docker deployment
* Automated tests
* Cloud deployment

A production version could follow:

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

# 🎯 Project Purpose

This project was built as a practical demonstration of:

* Generative AI application development
* Agentic AI
* LangGraph
* LangChain
* OpenAI integration
* Tool calling
* ReAct agents
* Conversational state
* Business-rule validation
* Python application development

It demonstrates how an LLM can move beyond simple text generation and interact with external application logic to complete real-world tasks.

---

# 📄 License

This project is intended for educational and portfolio purposes.

```

**`OpenAI LLM + LangGraph ReAct agent + tool calling + conversational state + CSV CRUD operations + business-rule validation.`**
```
