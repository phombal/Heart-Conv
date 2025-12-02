# Agent Evaluation Guide

## Overview

This project now supports evaluating multiple agent implementations using the same evaluation framework. You can easily switch between different agent architectures to compare their performance.

## Available Agents

### 1. `assistant.py` (Multi-Agent with Handoffs)
- **Architecture**: Multi-agent system with orchestrator pattern
- **Agents**: Assistant Agent, Recommendation Agent, Verification Agent, and medication-specific checker agents
- **Features**: 
  - Agent-to-agent handoffs for specialized tasks
  - Separate recommendation and verification logic
  - Medication-specific safety checks
- **Use Case**: Complex clinical decision-making with multiple specialized agents

### 2. `base-assistant.py` (Single Agent, No Handoffs)
- **Architecture**: Single agent handling all tasks
- **Agents**: One Base Assistant Agent
- **Features**:
  - No tool calls or agent handoffs
  - All logic handled by a single LLM call
  - Simpler architecture
- **Use Case**: Baseline comparison, testing if simpler approaches work as well

## Running Evaluations

### Basic Usage

```bash
# Run with default agent (assistant.py)
./venv/bin/python simulation.py

# Run with base agent (no handoffs)
./venv/bin/python simulation.py -a base-assistant.py

# Run with custom agent file
./venv/bin/python simulation.py -a path/to/your/agent.py
```

### Command-Line Arguments

- `-a, --agent`: Agent file to use (default: `assistant.py`)
- `-n, --num`: Number of scenarios to run (default: all 20)
- `-b, --batch-size`: Concurrent simulations per batch (default: 5)
- `-o, --output`: Output directory for results (default: `eval_results`)

### Examples

```bash
# Quick test: Run 3 scenarios with base agent
./venv/bin/python simulation.py -a base-assistant.py -n 3

# Full evaluation: All scenarios with multi-agent system
./venv/bin/python simulation.py -a assistant.py

# Custom output directory
./venv/bin/python simulation.py -a base-assistant.py -o base_agent_results
```

## Creating Your Own Agent

To create a custom agent for evaluation:

1. **Create a new Python file** (e.g., `my-agent.py`)

2. **Implement the `AssistantOrchestrator` class** with this structure:

```python
from agents import Agent, Runner, TResponseInputItem
from typing import List
from prompts.assistantInstructions import assistantInstructions

class AssistantOrchestrator:
    def __init__(self, scenario_str: str):
        # Combine scenario context with instructions
        combined_instructions = f"{scenario_str}\n\n{assistantInstructions}"
        
        # Create your agent(s)
        self.assistant_agent = Agent(
            name="My Custom Agent",
            instructions=combined_instructions,
            tools=[]  # Add tools if needed
        )
    
    async def run(self):
        # Optional: implement interactive mode for testing
        pass
```

3. **Run evaluation** with your custom agent:

```bash
./venv/bin/python simulation.py -a my-agent.py
```

## Evaluation Output

Each agent run produces:

- **Individual conversation files**: `{output_dir}/{conversation_id}_conversation.json`
  - Full conversation transcript
  - Per-turn evaluations (SAFE/CORRECT/OPTIMAL/EMPATHETIC)
  - Protocol outcome classification
  - Assignment compliance scores

- **Batch summary**: `{output_dir}/batch_eval_summary_{timestamp}.json`
  - Aggregate statistics across all conversations
  - Average scores per dimension
  - Success rates
  - Protocol outcome distribution

## Comparing Agents

To compare different agents:

1. Run evaluations with different output directories:
```bash
./venv/bin/python simulation.py -a assistant.py -o multi_agent_results
./venv/bin/python simulation.py -a base-assistant.py -o base_agent_results
```

2. Compare the summary files:
   - `multi_agent_results/batch_eval_summary_*.json`
   - `base_agent_results/batch_eval_summary_*.json`

3. Key metrics to compare:
   - **Per-turn scores**: SAFE, CORRECT, OPTIMAL, EMPATHETIC
   - **Weighted score**: Overall quality (0-5 scale)
   - **Protocol outcomes**: Distribution of success/failure types
   - **Assignment compliance**: Adherence to high-level requirements

## Troubleshooting

### "Module not found" errors
Make sure you're using the virtual environment:
```bash
./venv/bin/python simulation.py
```

### "AssistantOrchestrator not found"
Your custom agent file must have an `AssistantOrchestrator` class with:
- `__init__(self, scenario_str: str)` method
- `self.assistant_agent` attribute

### Agent loading errors
Check that:
- The agent file exists and path is correct
- The file has valid Python syntax
- All required imports are available


