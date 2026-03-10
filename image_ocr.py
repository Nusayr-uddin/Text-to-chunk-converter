import fitz
import easyocr
import os

PDF_PATH = "data/source_docs/IMF_Qatar_Report.pdf"
OUTPUT_IMG_DIR = "data/processed/images"

os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

reader = easyocr.Reader(['en'])

def extract_images():
    doc = fitz.open(PDF_PATH)
    img_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]

            img_path = f"{OUTPUT_IMG_DIR}/page{page_num+1}_img{img_index+1}.png"
            with open(img_path, "wb") as f:
                f.write(img_bytes)

            img_count += 1

    print(f"🖼 Extracted {img_count} images into {OUTPUT_IMG_DIR}")
    return img_count


def perform_ocr():
    texts = []
    for img_name in os.listdir(OUTPUT_IMG_DIR):
        img_path = f"{OUTPUT_IMG_DIR}/{img_name}"
        result = reader.readtext(img_path, detail=0)
        texts.append(f"[{img_name}]: {' '.join(result)}")
    
    with open("data/processed/ocr_text.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(texts))

    print("✔️ OCR Completed → data/processed/ocr_text.txt")


if __name__ == "__main__":
    extract_images()
    perform_ocr()