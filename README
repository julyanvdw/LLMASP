# AspPy2

**AspPy2** is a lightweight and extensible Python library for programmatically constructing Answer Set Programming (ASP) code with integrated support for Controlled Natural Language (CNL) and Natural Language (NL) mappings. It is designed for applications involving explainable logic programming, dataset generation, and language-to-logic translation tasks.

> **Note:** AspPy2 is an active research and development project. Features, interfaces, and documentation are subject to change.

---

## Key Features

- **Composable ASP Construction**  
  Model ASP programs as modular, line-based objects with optional metadata such as labels, CNL strings, and NL explanations.

- **Semantic Grouping & Explanation**  
  Define logical groupings of ASP rules with support for arity-based natural language templates—enabling dynamic generation of fluent group-level explanations.

- **Systematic Data Generation**  
  Automatically generate comprehensive datasets through splicing, variation, and combination of rules and groups. Outputs include:
  - Full `(ASP, CNL, NL)` triplets
  - Unique `NL → CNL` mappings
  - Unique `CNL → ASP` mappings

- **Controlled Text Variation**  
  Incorporate placeholder-based variation mechanisms to produce diverse CNL and NL outputs for robust data augmentation.

---

## How It Works

1. **Program Construction**  
   Use the `ASPProgram` class to incrementally build ASP logic programs. Lines can include CNL/NL mappings and labels, and can be organized into groups.

2. **Text Variation Definition**  
   Specify placeholder substitution patterns to allow fine-grained linguistic variation in both CNL and NL outputs.

3. **Data Generation Pipeline**  
   The `DataGenerator` component handles:
   - Combinatorial generation of valid rule sets
   - Application of variation templates
   - Splicing and transformation strategies

4. **Output & Export**  
   Generated data can be exported or consumed directly as:
   - Complete `(ASP, CNL, NL)` datasets  
   - Deduplicated pairwise mappings (`NL:CNL`, `CNL:ASP`) for training and evaluation

---

## Requirements

- **Python**: 3.8 or higher  
- **Recommended**: Use a virtual environment for isolation

```bash
python3 -m venv venv
source venv/bin/activate
