# Law-N SQL Core (`law-n-sql-core`)

Core prototype for **N-SQL**, the network-native query language of **Law-N**.

N-SQL treats **network state** (signals, channels, devices, towers, G-layers) as first-class queryable objects — just like rows in a database, but aligned with the Law-N philosophy:

> Instead of computers talking _over_ a network,  
> the network itself becomes the computer.

This repo is a **minimal but working** implementation:

- A tiny **lexer** for N-SQL
- A simple **parser** building an AST
- An in-memory **execution engine** over mock `network.routes` data
- A **CLI** so you can run N-SQL queries from the terminal
- Docs for the **initial grammar** and mental model

It is **not** production code.  
It’s a **reference core** for Law-N Part 3 and future repos in the Law-N stack.

---

## 🚀 Quickstart

### Requirements

- Python **3.10+**
- No external dependencies (standard library only)

### Install (local dev)

```bash
git clone https://github.com/YOUR_USER/law-n-sql-core.git
cd law-n-sql-core
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
