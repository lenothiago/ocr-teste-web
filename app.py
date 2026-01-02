import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from docx import Document
import io

# Configuração da Página
st.set_page_config(page_title="Conversor OCR", layout="centered")

def processar_pdf_para_docx(pdf_file):
    doc = Document()
    doc.add_heading('Texto Extraído', 0)

    try:
        # Converter PDF para imagens (300 dpi é bom para OCR)
        st.info("Lendo PDF... Isso pode demorar um pouco.")
        images = convert_from_bytes(pdf_file.read(), dpi=300)
        
        total = len(images)
        barra = st.progress(0)

        for i, image in enumerate(images):
            status_text = st.empty()
            status_text.text(f"Processando página {i+1}/{total}...")
            
            if i > 0: doc.add_page_break()
            doc.add_heading(f'Página {i+1}', level=1)

            # OCR
            texto = pytesseract.image_to_string(image, lang='por+eng')
            
            if texto.strip():
                doc.add_paragraph(texto)
            else:
                doc.add_paragraph("[Sem texto detectado]")
            
            barra.progress((i + 1) / total)
            status_text.empty() # Limpa o texto de status

        docx_io = io.BytesIO()
        doc.save(docx_io)
        docx_io.seek(0)
        return docx_io

    except Exception as e:
        st.error(f"Erro: {e}")
        return None

# Interface
st.title("📄 Extrator de Texto (OCR)")
st.markdown("Faça upload de um PDF para receber um DOCX editável.")

uploaded_file = st.file_uploader("Arraste seu PDF aqui", type=['pdf'])

if uploaded_file and st.button("Processar Arquivo"):
    resultado = processar_pdf_para_docx(uploaded_file)
    if resultado:
        st.success("Pronto!")
        st.download_button("📥 Baixar Word (.docx)", resultado, "texto_convertido.docx")