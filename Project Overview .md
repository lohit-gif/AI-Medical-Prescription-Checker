1. PROJECT TITLE

AI Medical Prescription Checker


---

2. PROJECT OVERVIEW

The AI Medical Prescription Checker is an AI-based healthcare system that analyzes handwritten or printed medical prescriptions. It uses OCR and Machine Learning techniques to extract medicine details, verify dosages, detect duplicate medicines, identify drug interactions, and generate reports for safer medication usage.


---

3. PROBLEM STATEMENT

Medical prescriptions are often difficult to read and may contain dosage errors, duplicate medications, or harmful drug interactions. Patients can misunderstand instructions, leading to medication mistakes. An automated AI-based system is needed to verify prescriptions and improve patient safety.


---

4. PROJECT OBJECTIVES

Digitize handwritten prescriptions.

Extract medicine information using OCR.

Verify dosage and frequency.

Detect duplicate medicines.

Identify drug interactions.

Generate prescription analysis reports.

Improve patient safety.



---

5. PROJECT MODULES

Module 1: User Management

Registration

Login

Profile Management

---

Module 2: Prescription Upload

Upload Image/PDF

Image Processing

OCR Text Extraction

---

Module 3: AI Analysis

Medicine Recognition

Dosage Verification

Drug Interaction Detection

Duplicate Medicine Detection

---

Module 4: Medicine Information

Medicine Details

Side Effects

Usage Instructions

---

Module 5: Report Generation

Analysis Summary

Warning Reports

Download Reports

---

Module 6: Admin Module

Manage Users

Manage Medicines

View Reports



---

6. DATABASE TABLES

USERS TABLE

| Field Name | Data Type    | Description   |
| ---------- | ------------ | ------------- |
| user_id    | INT (PK)     | User ID       |
| name       | VARCHAR(100) | User Name     |
| email      | VARCHAR(100) | Email Address |
| password   | VARCHAR(255) | Password      |
| role       | VARCHAR(20)  | User Role     |

PRESCRIPTIONS TABLE

| Field Name      | Data Type    | Description        |
| --------------- | ------------ | ------------------ |
| prescription_id | INT (PK)     | Prescription ID    |
| user_id         | INT (FK)     | User Reference     |
| file_name       | VARCHAR(255) | Uploaded File Name |
| upload_date     | DATETIME     | Upload Date        |
| status          | VARCHAR(20)  | Analysis Status    |

MEDICINES TABLE

| Field Name        | Data Type    | Description        |
| ----------------- | ------------ | ------------------ |
| medicine_id       | INT (PK)     | Medicine ID        |
| medicine_name     | VARCHAR(100) | Medicine Name      |
| dosage            | VARCHAR(50)  | Dosage Information |
| side_effects      | TEXT         | Side Effects       |
| usage_instruction | TEXT         | Usage Instructions |

ANALYSIS_REPORT TABLE

| Field Name         | Data Type | Description            |
| ------------------ | --------- | ---------------------- |
| report_id          | INT (PK)  | Report ID              |
| prescription_id    | INT (FK)  | Prescription Reference |
| medicines_detected | TEXT      | Detected Medicines     |
| warnings           | TEXT      | Alerts & Warnings      |
| analysis_date      | DATETIME  | Analysis Date          |

DRUG_INTERACTIONS TABLE

| Field Name              | Data Type    | Description         |
| ----------------------- | ------------ | ------------------- |
| interaction_id          | INT (PK)     | Interaction ID      |
| medicine_1              | VARCHAR(100) | First Medicine      |
| medicine_2              | VARCHAR(100) | Second Medicine     |
| interaction_description | TEXT         | Interaction Details |
| severity                | VARCHAR(20)  | Risk Level          |

---

7. TECHNOLOGIES USED

Front End: HTML, CSS, JavaScript, Bootstrap

Back End: Python, Flask

Database: MySQL

AI/OCR: Tesseract OCR, Machine Learning, NLP

Tools: VS Code, GitHub, XAMPP


---

8. EXPECTED OUTCOME

The system automatically analyzes medical prescriptions, identifies medicines, verifies dosages, detects duplicate medicines and drug interactions, and generates a detailed report. This reduces medication errors and improves patient safety through AI-powered prescription validation.
