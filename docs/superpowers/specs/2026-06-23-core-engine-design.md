# Core Engine Architecture Design

## 1. Overview
The goal of this design is to upgrade `novel-v2` from a purely interactive, Claude-skills-dependent tool into an automated, highly robust AI core writing engine. This design explicitly excludes any frontend or UI development and focuses entirely on backend automation within the `src/novel/core/` directory.

## 2. Architectural Decisions & Tech Stack

Based on the goal of creating a robust, debuggable, and native generation pipeline:

- **LLM Client & Structured Output**: Native `openai` Python SDK paired with `Pydantic`. We will avoid heavy frameworks like LangChain to keep the abstraction layer thin and debuggable. Pydantic will enforce JSON schema outputs.
- **Workflow Orchestration**: Native Python state machines. Instead of using LangGraph, we will implement explicit while-loops and state transitions for the QA loop to ensure we have precise control over the retry logic.
- **Memory & Context**: A dynamic text-based `ContextBuilder`. In Phase 1, it will read static YAML files (worldbuilding, characters, previous chapter summaries) and assemble them into the system prompt. Vector-based RAG (like ChromaDB) will be deferred to a later phase to minimize initial complexity.

## 3. Component Design

The architecture is divided into four distinct components that pipeline the generation process.

### 3.1 Infrastructure & Configuration
- **Settings Unification**: The `.env` file uses `LLM_API_KEY`, but the `pydantic-settings` model expects `OPENAI_API_KEY`. This mismatch will be resolved by standardizing on `OPENAI_API_KEY`.
- **Dead Code Removal**: Remove the broken import of `llm_client.py` from `scripts/utils/__init__.py`.

### 3.2 Core LLM Layer (`src/novel/core/llm/`)
- **`client.py`**: A thin wrapper around `AsyncOpenAI` that handles authentication, model routing, and asynchronous text generation.
- **`structured.py` (StructuredGenerator)**: A higher-order function that takes a Pydantic schema and a prompt, injects the JSON schema into the system prompt, and attempts to parse the LLM's response.
  - **Self-Healing Retry**: If `ValidationError` or `JSONDecodeError` occurs, the exact error string is fed back to the LLM to request a fix, up to `MAX_RETRIES`.

### 3.3 Context Builder (`src/novel/core/memory/`)
- **`context_builder.py`**: A utility class responsible for avoiding hallucination. Before generating Chapter N, it:
  1. Reads global `worldbuilding` YAML files.
  2. Extracts characters relevant to the current chapter.
  3. Loads the overarching outline and summaries of chapters `N-3` to `N-1`.
  4. Formats these into a dense, token-efficient markdown context string to be prepended to the system prompt.

### 3.4 QA Workflow Engine (`src/novel/core/workflow/`)
- **`qa_loop.py`**: Implements the critique-and-revise cycle. It takes a generated draft, evaluates it against predefined criteria (word count, strict format, setting consistency), and asks the LLM to either pass it or revise it.
- **`chapter_writer.py`**: The main orchestrator that wires the components together:
  `ContextBuilder` -> `StructuredGenerator (Draft)` -> `QA Loop` -> `Save Markdown`.

### 3.5 Automation CLI
- **`scripts/generate.py`**: A new CLI entrypoint allowing headless execution, e.g., `python scripts/generate.py chapter <project_id> --chapter 1`.

## 4. Error Handling & Fallbacks
- **Token Limits**: If the assembled context exceeds context window limits, the ContextBuilder will fall back to using only the broad outline and the immediate previous chapter.
- **Retry Exhaustion**: If `StructuredGenerator` exhausts its retry limit without yielding valid JSON, it will raise a distinct `GenerationError`, allowing the workflow engine to abort gracefully without corrupting local files.

## 5. Testing Strategy
- **Unit Tests**: Test the `StructuredGenerator` using mocked OpenAI responses (both success and simulated JSON decode failures) to prove the retry mechanism works.
- **Integration Tests**: Mock the LLM to return a sub-par draft, and assert that the `qa_loop` correctly flags it and triggers a revision cycle.
