# 🔍 SmartSearch Pro: Comprehensive Technical Project Guide

Welcome team! This document is designed to help your group (6 students) understand every detail of the **SmartSearch Pro** project. This will ensure every member can confidently explain their part during the final presentation.

---

## 1. Project Vision & Objective
SmartSearch Pro is a complete **Information Retrieval (IR) System** that operates on **live web data**.
*   **Domain:** Technology, Science, and Space News.
*   **Objective:** To provide high-precision search results using the state-of-the-art **BM25 Ranking Algorithm**.

---

## 2. Technical Architecture
The system is divided into 4 main layers:
1.  **Data Layer (scraper.py):** Handles automated web crawling and data extraction.
2.  **Logic Layer (engine.py):** Handles Natural Language Processing (NLP) and indexing.
3.  **Storage Layer (index.json):** Persists the processed data in an "Inverted Index" format.
4.  **Presentation Layer (app.py & HTML):** The user interface for interacting with the engine.

---

## 3. Detailed Component Breakdown

### 📂 `scraper.py` (The Crawler)
*   **Technology:** Uses `requests` and `BeautifulSoup4`.
*   **Function:** It visits 4 global news portals (BBC, Wired, Hacker News, The Verge).
*   **Extraction:** It captures the (Title, Content, and URL) while cleaning out HTML noise.

### 📂 `engine.py` (The Brain)
This is the most critical file, containing the `IREngine` class:
*   **`preprocess` Method**: Performs 4 NLP steps:
    1.  **Lowercasing**: Standardizing text.
    2.  **Cleaning**: Removing punctuation and numbers.
    3.  **Tokenization**: Splitting sentences into individual words.
    4.  **Stemming**: Reducing words to their root form (e.g., `computers` -> `comput`) using the Porter Stemmer.
*   **BM25 Algorithm**: A modern ranking function (superior to TF-IDF) that scores documents based on:
    *   Term Frequency (How many times a word appears).
    *   Inverse Document Frequency (How unique a word is across the system).
    *   Length Normalization (Accounting for short vs. long articles).

### 📂 `app.py` (The Bridge)
*   **Framework:** Built with **Flask**.
*   **Routes:**
    *   `/`: Serves the main search dashboard.
    *   `/search`: Receives the query and returns JSON results from the engine.
    *   `/stats`: Provides system metrics (Doc count, Term count) for the UI.

### 📂 `evaluator.py` (Quality Assurance)
*   Tests system effectiveness using 3 industry-standard metrics:
    1.  **Precision**: Accuracy of the retrieved results.
    2.  **Recall**: The ability to find all relevant documents.
    3.  **F1-Score**: The harmonic mean of Precision and Recall.

---

## 4. Why BM25? (The Math)
If asked, "Why not use simple keyword matching?", your answer should be:
**BM25 solves two major IR problems:**
1.  **Term Saturation**: It prevents "Spam" articles (that repeat words excessively) from dominating the results.
2.  **Length Normalization**: It ensures fair ranking for shorter, focused articles compared to longer ones.

---

## 5. UI/UX Design
*   **Design Style:** Modern **Glassmorphism**.
*   **Framework:** **Tailwind CSS**.
*   **Responsiveness:** Fully mobile-friendly and interactive.

---

## 6. Recommended Task Distribution (For 6 Students)
To deliver a professional presentation, consider this split:
1.  **Student 1 (Project Lead):** Explains project vision, objectives, and scope.
2.  **Student 2 (Scraping Specialist):** Explains `scraper.py` and live data acquisition.
3.  **Student 3 (NLP Expert):** Explains Preprocessing (Stemming, Tokenization) in `engine.py`.
4.  **Student 4 (Algorithm Master):** Explains the BM25 formula and scoring math.
5.  **Student 5 (Full-Stack Developer):** Explains the Flask API and the Glassmorphic UI.
6.  **Student 6 (QA & Analytics):** Explains `evaluator.py` and the precision/recall results.

---

## 7. How to Run
1.  **Install dependencies:** `pip install -r requirements.txt`
2.  **Collect Data:** `python data_collector.py` (This builds the `index.json`)
3.  **Start Server:** `python app.py`
4.  **Open Browser:** Go to `http://127.0.0.1:5001`

---
