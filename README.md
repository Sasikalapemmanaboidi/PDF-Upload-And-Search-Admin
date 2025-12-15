Technical Document
Django PDF Upload, Page-wise Text Extraction & Search System
1. Introduction
This document describes the design and implementation of a Django-based PDF processing system that allows users to upload PDF files, extract text page by page, store the extracted content in a database, view pages similar to the original PDF structure, and perform text search across pages with page-level results.
The system is built using Django 4.x, follows a clean MVT architecture, and uses PyMuPDF for efficient PDF text extraction.
2. System Overview
High-Level Workflow
PDF Upload
   ↓
Text Extraction (Page-wise)
   ↓
Database Storage
   ↓
Page Viewer with Pagination
   ↓
Search Across Pages
The system ensures that each PDF page is treated as an independent searchable unit while still belonging to a single PDF document.
3. Technology Stack
Technology	Purpose
Django 4.x / 5.x	Backend framework
Python 3.10+	Programming language
PyMuPDF (fitz)	PDF text extraction
MySQL	Database
Bootstrap 5	UI styling
HTML + JavaScript	Client-side rendering & highlighting

4. Libraries Used
4.1 PyMuPDF (fitz)
Why PyMuPDF?
•	Faster than pdfplumber
•	Accurate page-wise text extraction
•	Handles large PDFs efficiently
•	Minimal dependencies
Usage:
import fitz
doc = fitz.open(pdf_path)
page_text = doc.load_page(page_index).get_text()

5. Database Design
5.1 PDFDocument Model
Stores metadata about uploaded PDFs.
class PDFDocument(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
5.2 PDFPage Model
Stores extracted text per page.
class PDFPage(models.Model):
    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE)
    page_number = models.PositiveIntegerField()
    text = models.TextField()
Design Benefits
•	Enables page-level search
•	Supports pagination
•	Scales well for large documents
•	Maintains document–page relationship
6. Upload → Extract → Save Flow
Step-by-Step Process
1.	User uploads a PDF file via Django Admin or UI.
2.	The PDF file is saved to the media/ directory.
3.	PyMuPDF opens the file and iterates through pages.
4.	Text is extracted from each page.
5.	Each page’s text is stored in the database with its page number.
Extraction Logic
doc = fitz.open(pdf_path)
for page_index in range(len(doc)):
    text = doc.load_page(page_index).get_text()
    PDFPage.objects.create(
        document=document,
        page_number=page_index + 1,
        text=text
    )
This ensures one database row per PDF page.
7. Page Viewing & Pagination
Pagination Strategy
•	Each page is displayed individually
•	Django’s Paginator is used
•	Navigation via Previous / Next buttons
Paginator(pages, 1)
Benefits
•	Mimics real PDF page navigation
•	Efficient for large PDFs
•	Clean UI experience
8. Search Logic
Search Requirements
•	Search text across all pages
•	Show page numbers where matches are found
•	Allow jumping directly to matching pages
Backend Search
PDFPage.objects.filter(
    document=document,
    text__icontains=query
)
Search Behavior
•	Case-insensitive
•	Page-level results
•	Fast for medium-sized documents

9. Search Highlighting (HTML-Only)
To enhance usability, the searched word is highlighted in red using JavaScript, without backend changes.
How It Works
1.	Read q parameter from URL
2.	Find matching words in page text
3.	Wrap matches with a red <span>
Highlight Example
<span class="highlight">searched_word</span>
Benefits
•	No backend processing
•	Instant visual feedback
•	Lightweight and fast
10. Security & Performance Considerations
•	File upload restricted to PDFs
•	Extraction runs only once per upload
•	No user input is directly executed
•	Search uses Django ORM to prevent SQL injection
•	Pagination prevents loading large text blobs at once
11. Setup Instructions
Installation
pip install -r requirements.txt
Run Migrations
python manage.py makemigrations
python manage.py migrate
Start Server
python manage.py runserver
12. Conclusion
This system provides a robust, scalable, and user-friendly solution for PDF text extraction and searching. By combining Django’s ORM, PyMuPDF’s extraction capabilities, and a clean UI, the application meets all functional requirements while remaining easy to extend with features such as full-text search, PDF previews, or role-based access.
<img width="664" height="337" alt="image" src="https://github-production-user-asset-6210df.s3.amazonaws.com/97533699/526366687-572293bb-5f5a-46ee-bfc1-db7a89c7f20a.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20251215%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251215T021906Z&X-Amz-Expires=300&X-Amz-Signature=f4e6a988e3d929afb92f981b6120a98e8d9a59dd681fed6f888d57db11decee7&X-Amz-SignedHeaders=host"/>
<img width="664" height="337" alt="image" src="<img width="1136" height="591" alt="image" src="https://github.com/user-attachments/assets/3602f89b-90e7-4b7c-aba6-ac645ec10d6d" />
" />
<img width="1148" height="623" alt="image" src="https://github.com/user-attachments/assets/ad383600-c425-4b30-9bf6-47c82e3e47a5" />
<img width="911" height="603" alt="image" src="https://github.com/user-attachments/assets/a6f20867-93f2-4356-aef5-585021595655" />
![Uploading image.png…]()




