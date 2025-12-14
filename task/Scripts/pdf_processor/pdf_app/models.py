from django.db import models

class PDFDocument(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'pdf_document'


class PDFPage(models.Model):
    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='pages')
    page_number = models.PositiveIntegerField()
    text = models.TextField()

    def __str__(self):
        return f"{self.document.title} - Page {self.page_number}"

    class Meta:
        db_table = 'pdf_page'