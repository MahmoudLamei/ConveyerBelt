# Conveyor Belt Control System (Reinforcement Learning)

## Overview

This project implements a decision-making system for controlling an industrial conveyor belt scenario using reinforcement learning and structured state modeling.

The system simulates the routing of multiple objects (e.g., boxes with different properties) and learns how to coordinate their movement based on environmental states and defined constraints.

---

## Key Concepts

### 1. State Modeling

The environment is represented using a **discrete state space**, where each state encodes:

* Positions of multiple objects
* Object properties (e.g., color/type)
* System conditions

This structured representation enables consistent decision-making and reflects how real industrial systems model system states.

---

### 2. Action & Decision Logic

* Actions are defined as **combinations of individual object decisions**
* A **joint action space** is used to coordinate multiple entities
* The system maps states → actions using a learned policy

This mirrors **rule-based and configuration-like logic** used in industrial systems.

---

### 3. Reinforcement Learning Approach

* Tabular Q-learning is used
* The system learns optimal behavior through:

  * state transitions
  * reward signals
  * iterative updates

---

### 4. System Design

* Discrete state encoding for deterministic behavior
* Explicit modeling of system constraints
* Separation of environment logic and decision logic

---

## Repository Structure

* `environment/` → simulation logic
* `agent/` → learning and decision logic
* `training/` → training loop and evaluation
