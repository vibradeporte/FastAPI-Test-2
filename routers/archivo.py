from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from docx import Document
from docx2pdf import convert
import os
import shutil

archivo_router = APIRouter()

@archivo_router.post("/convert/")
async def convert_word_to_pdf(
    file: UploadFile = File(...),
    fecha: str = Form(...),
    cliente: str = Form(...),
    cotizacion: str = Form(...)
):
    # Crear un directorio temporal para almacenar archivos
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)

    # Guardar el archivo subido
    input_path = os.path.join(temp_dir, file.filename)
    with open(input_path, "wb") as f:
        f.write(await file.read())
    
    # Verificar si el archivo fue guardado correctamente
    if not os.path.exists(input_path):
        raise RuntimeError(f"Failed to save the uploaded file: {input_path}")

    # Cargar el documento existente
    document = Document(input_path)
    
    # Reemplazar texto en párrafos
    for paragraph in document.paragraphs:
        if "FECHA" in paragraph.text:
            paragraph.text = paragraph.text.replace("FECHA", fecha)
        if "CLIENTE" in paragraph.text:
            paragraph.text = paragraph.text.replace("CLIENTE", cliente)
        if "COTIZACION" in paragraph.text:
            paragraph.text = paragraph.text.replace("COTIZACION", cotizacion)
    
    # Guardar el documento modificado
    modified_docx_path = os.path.join(temp_dir, "modified_document.docx")
    document.save(modified_docx_path)

    # Verificar si el documento modificado fue guardado correctamente
    if not os.path.exists(modified_docx_path):
        raise RuntimeError(f"Failed to save the modified document: {modified_docx_path}")
    
    # Convertir el documento modificado a PDF
    output_pdf_path = os.path.join(temp_dir, "output.pdf")
    convert(modified_docx_path, output_pdf_path)

    # Verificar si el archivo PDF fue generado correctamente
    if not os.path.exists(output_pdf_path):
        raise RuntimeError(f"Failed to convert the document to PDF: {output_pdf_path}")
    
    # Devolver el archivo PDF
    response = FileResponse(output_pdf_path, filename="output.pdf", media_type='application/pdf')
    
    # Limpiar archivos temporales
    #shutil.rmtree(temp_dir)
    
    return response
