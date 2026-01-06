# Asana Workspace Seed Data Generator

## Overview

This project implements a synthetic data generation pipeline that produces a realistic SQLite database simulating an enterprise Asana workspace. The dataset is intended as high-quality seed data for reinforcement learning (RL) environments where agents interact with structured project management data.

The emphasis is on realism, consistency, and controlled noise rather than exhaustive feature completeness. The generated dataset mirrors real B2B SaaS patterns such as incomplete tasks, repeated naming conventions, uneven team sizes, and sparse metadata.

## Key Objectives

- Generate a relationally consistent Asana-like schema
- Produce realistic enterprise task data suitable for RL simulation
- Combine real-world datasets, heuristics, and LLM-generated text
- Avoid synthetic regularities that could enable shortcut learning
- Keep the system simple, explainable, and reproducible

## Database Output

Running the pipeline produces a single SQLite database:

- `asana_simulation.sqlite`

Core entities included:

- `organizations`
- `users`
- `teams`
- `team_memberships`
- `projects`
- `sections`
- `tasks`
- `subtasks`
- `comments`
- `custom_field_definitions`
- `custom_field_values`
- `tags`
- `task_tags`

An Entity–Relationship (ER) diagram is included in the documentation to illustrate table relationships.

## Data Sources

### Public Datasets

The following publicly available datasets help ground the synthetic data in realistic distributions:

- Abhijeet107 / Shark-Tank-India — used for realistic company and organization names
- Aptivi-Analytics / NamesList — used for first and last names

Static datasets ensure reproducibility and avoid placeholder naming artifacts.

### Large Language Model

The Gemini API is used for natural language generation (task titles, descriptions, comments). LLM usage is constrained and supplemented with deterministic fallbacks to ensure robustness.

## Data Generation Strategy

The pipeline combines three complementary approaches:

1. Dataset-Driven Generation — anchors names and organization data in real-world patterns
2. Heuristic-Based Generation — controls relationships, temporal attributes, completion rates, custom field values, and tag application
3. LLM-Based Text Generation — produces task names, descriptions, and comments with post-processing and fallbacks

## Project Structure

```
src/
├── main.py
├── generators/
│   ├── organizations.py
│   ├── users.py
│   ├── teams.py
│   ├── projects.py
│   ├── tasks.py
│   ├── subtasks.py
│   ├── comments.py
│   ├── custom_fields.py
│   └── tags.py
├── utils/
│   ├── data_loader.py
│   └── llm.py
├── prompts/
│   ├── task_names.txt
│   ├── task_descriptions.txt
│   └── comments.txt
└── data/
    ├── saas_companies.txt
    ├── first_names.txt
    └── last_names.txt
```

## How to Run

1. Install dependencies:

```bash
pip install google-generativeai
```

2. Set the Gemini API key (or use a `.env` solution):

```bash
# Unix/macOS
export GEMINI_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:GEMINI_API_KEY = "your_api_key_here"
```

3. Generate the database from the project root:

```bash
python src/main.py
```

This will create `asana_simulation.sqlite` in the `output/` folder.

Use `test.py` to print a small sample of rows from the generated database:

```bash
python test.py
```
