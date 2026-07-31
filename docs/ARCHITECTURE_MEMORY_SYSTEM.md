# Jebediah Memory Architecture

## Purpose

The Jebediah Memory System provides persistent semantic memory capabilities for the Jebediah AI infrastructure.

The goal is to allow Jebediah to store, retrieve, classify, and reason over previous information using vector-based semantic search.

---

# System Overview

Current architecture:

User / Agent Input

        |
        v

Collector Layer

        |
        v

Memory Service API

        |
        +----------------+
        |                |
        v                v

Ollama Embeddings     Memory Logic

(nomic-embed-text)        |

        |
        v

Qdrant Vector Database


---

# Components

## Collector

Location:

services/jebediah-memory/app/collector/

Responsibilities:

- Receive incoming memory candidates
- Evaluate memory importance
- Prepare memory objects
- Handle future memory intelligence workflows

---

## Memory API

Location:

services/jebediah-memory/app/main.py

Responsibilities:

- Store memories
- Generate embeddings
- Query semantic memory
- Provide context retrieval

---

## Embedding System

Current model:

nomic-embed-text:latest

Provider:

Ollama

Purpose:

Convert text meaning into vector representations.

Current vector size:

768 dimensions

---

## Vector Database

System:

Qdrant

Collection:

jebediah_memory

Purpose:

Store semantic representations of memories.

---

# Memory Lifecycle

Current:

Input
 |
Generate embedding
 |
Store vector + metadata
 |
Retrieve using semantic similarity


Future:

Input
 |
Classification
 |
Importance scoring
 |
Deduplication
 |
Memory consolidation
 |
Long-term storage

---

# Current Capabilities

Completed:

- Dockerized memory service
- Ollama integration
- Semantic embeddings
- Qdrant vector storage
- Semantic retrieval API
- GitHub source control

---

# Future Development

## Memory Intelligence

Planned:

- Memory classification
- Confidence scoring
- Deduplication
- Importance weighting
- Automatic consolidation


## Collector Intelligence

Planned:

- Determine whether information should become memory
- Identify permanent decisions
- Identify temporary state
- Manage memory lifecycle


## Self Improvement

Future goal:

Allow Jebediah to improve workflows, documentation, and operational knowledge while maintaining human approval boundaries.

---

# Design Principle

Jebediah should not simply remember more.

Jebediah should remember better.
