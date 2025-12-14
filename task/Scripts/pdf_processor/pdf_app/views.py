import fitz  # PyMuPDF
from .models import PDFDocument, PDFPage
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect



def upload_pdf(request):
    if request.method == 'POST':
        title = request.POST['title']
        pdf_file = request.FILES['pdf']

        document = PDFDocument.objects.create(
            title=title,
            pdf_file=pdf_file
        )

        doc = fitz.open(document.pdf_file.path)

        for page_index in range(len(doc)):
            page = doc.load_page(page_index)
            text = page.get_text()

            PDFPage.objects.create(
                document=document,
                page_number=page_index + 1,
                text=text
            )

        return redirect('view_pages', document.id)

    return render(request, 'upload.html')




def view_pages(request, doc_id):
    document = get_object_or_404(PDFDocument, id=doc_id)
    pages = PDFPage.objects.filter(document=document).order_by("page_number")

    # Pagination
    paginator = Paginator(pages, 1)
    current_page = request.GET.get("page", 1)
    page_obj = paginator.get_page(current_page)

    # Search logic
    query = request.GET.get("q")
    search_results = []

    if query:
        search_results = PDFPage.objects.filter(
            document=document,
            text__icontains=query
        ).values("page_number").distinct()

    return render(request, "pages.html", {
        "document": document,
        "page_obj": page_obj,
        "query": query,
        "search_results": search_results
    })

