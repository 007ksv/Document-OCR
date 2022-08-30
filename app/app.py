from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from app.utils import markdown_to_html_string

from .models import OCRDocument
from .ocr import OCR

app = FastAPI()


@app.get("/")
def read_root():
    html_string = markdown_to_html_string(markdown_file_location="README.md")
    return HTMLResponse(html_string)


@app.post("/api/v1/ocr-document/")
def ocr_document(ocr_doc: OCRDocument):
    try:
        ocr_obj = OCR(image_url=ocr_doc.image_url)
        result = ocr_obj.get_data_form_image()
        return JSONResponse(
            {"success": True, "data": {"document_id": result}}, status_code=200
        )
    except Exception as e:
        err_msg = getattr(e, "message", None)
        if not err_msg:
            err_msg = "Internal Error. Please Try Again"
        return JSONResponse({"error": err_msg}, 500)
