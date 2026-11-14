# Smart Wordlist Generator (My_Hydra)

> 🌐 **Language:** **English** | [Русский (README_Ru.md)](README_Ru.md)

A context-aware **Python** CLI utility for generating targeted password permutations from known cues (base words, years, special characters) during authorized security testing.

## ✨ Features
- 🧠 **Smart Combinator (`itertools.product`)** — generates case mutations (`lower`, `capitalize`, `original`), year suffixes, and special character combinations while filtering by minimum length (e.g., `>= 8` characters for WPA2).
- ⚡ **Modular CLI Workflow** — interactive command-line interface for rapidly building custom wordlists.

## 🚀 Usage

```bash
python3 mini_hydra.py
```
