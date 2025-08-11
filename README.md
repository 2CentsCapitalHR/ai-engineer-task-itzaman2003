[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/vgbm4cZ0)


# AI Engineer Task – Document Review & ADGM Reference Ingestion

## Overview
This repository contains the implementation for an AI-assisted document review system designed to identify compliance issues in corporate and legal documents against the Abu Dhabi Global Market (ADGM) regulatory framework.  
The solution integrates rule-based checks with a reference dataset built from official ADGM document sources. The reference dataset can be queried to provide relevant legal evidence for each flagged issue.

---

## Features
- **Document Parsing:** Extracts content from `.docx` and `.pdf` files.
- **Document Type Detection:** Identifies common corporate document types (e.g., Articles of Association, Memorandum of Association, Registers).
- **Rule-Based Compliance Checks:** Detects jurisdiction mismatches, missing signatory blocks, and other common issues.
- **ADGM Reference Ingestion:** Downloads, processes, and stores official ADGM regulatory documents for keyword-based search.
- **Evidence Attachment:** Associates flagged issues with relevant ADGM reference snippets.
- **Output Formats:**
  - Annotated `.docx` document with inline comments.
  - JSON report summarizing all detected issues, severity levels, and suggestions.

---

## Repository Structure
