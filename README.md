Student-Report-Assessment-AI
============================

This repository contains a Python script designed to **automate the assessment of academic reports** using large language models (LLMs). Specifically, it processes student reports in PDF format, extracts their content, and then sends the text to an LLM (either **Google Gemini** or **OpenAI's GPT models**) for a comprehensive evaluation based on predefined criteria. The assessment includes a **score (0-100)** and detailed constructive feedback for each criterion. All assessment results are then compiled and saved into an **Excel file** for easy review.

Key Features
------------

*   **PDF Text Extraction**: Utilizes [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) to efficiently extract text from student reports in PDF format.
    
*   **Automated Assessment**: Leverages the Google Gemini or OpenAI APIs to assess reports against specific academic criteria.
    
*   **Detailed Feedback**: Generates an overall score and narrative feedback for each report section (problem explanation, data pre-processing, optimal clustering methods, visualization, conclusion, and originality).
    
*   **Results Storage**: Compiles and saves all assessment results (including scores, comments, and file names) into an Excel file.
    
*   **LLM Model Flexibility**: Easily switch between Google Gemini and OpenAI GPT models.
    
*   **Automated Organization**: Processes reports from an organized student folder structure, making it suitable for bulk assessment.
    

How It Works
------------

This automated assessment process follows a straightforward and efficient workflow:

1.  **Read PDFs**: The script scans a specified main folder, identifies each student's sub-folder, and reads their PDF report files.
    
2.  **Extract Text**: The textual content from each PDF is automatically extracted.
    
3.  **Send to LLM**: The extracted report text is then sent to your configured LLM (either Google Gemini or OpenAI GPT) along with a structured assessment prompt.
    
4.  **Parse Response**: The response received from the LLM is parsed to extract the numerical score and detailed comments for each assessment criterion.
    
5.  **Save to Excel**: All collected assessment data (student/folder name, PDF file name, score, and all comments) are compiled and saved into a tabular format in an Excel file.
    

Purpose
-------

This repository aims to significantly **expedite the academic report grading process** for lecturers and educators. By automating parts of the evaluation, it ensures **consistency and objectivity** in feedback delivery. This tool is designed to be a **powerful supportive aid**, not a replacement for human judgment. Instead, it provides a structured and comprehensive foundation for further discussions with students, allowing educators to focus on more in-depth guidance.
