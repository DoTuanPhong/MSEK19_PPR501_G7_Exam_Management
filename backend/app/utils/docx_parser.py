import docx
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime
from docx.oxml.shared import qn

def parse_docx(file_path):
    doc = docx.Document(file_path)
    metadata = {}
    questions = []
    warnings = []

    # Process metadata
    for i, paragraph in enumerate(doc.paragraphs[:4]):
        try:
            key, value = paragraph.text.split(': ', 1)
            if i == 0:
                metadata['subject'] = value.strip()
            elif i == 1:
                metadata['number_of_quiz'] = int(value.strip())
            elif i == 2:
                metadata['lecturer'] = value.strip()
            elif i == 3:
                metadata['date'] = datetime.strptime(value.strip(), '%d-%m-%Y').date()
        except ValueError:
            warnings.append(f"Invalid metadata format in paragraph {i+1}")

    if 'subject' not in metadata:
        warnings.append("Subject is missing in the metadata")

    for table_index, table in enumerate(doc.tables):
        question = {}
        for row in table.rows:
            if len(row.cells) != 2:
                warnings.append(f"Invalid table format in table {table_index + 1}")
                continue

            key = row.cells[0].text.strip().lower()
            value = row.cells[1].text.strip()

            if key == 'qn':
                question['text'] = value
                # Handle image (MS Word 2016+)
                for paragraph in row.cells[1].paragraphs:
                    for run in paragraph.runs:
                        for element in run._element.findall('.//w:drawing', namespaces=run._element.nsmap):
                            blip = element.find('.//a:blip', namespaces=run._element.nsmap)
                            if blip is not None:
                                rId = blip.get(qn('r:embed'))
                                image_part = doc.part.related_parts[rId]
                                image_bytes = image_part.blob
                                image = Image.open(BytesIO(image_bytes))
                                buffered = BytesIO()
                                image.save(buffered, format="PNG")
                                question['image'] = base64.b64encode(buffered.getvalue()).decode()
            elif key.startswith('a.'):
                question['choices'] = [value]
            elif key in ['b.', 'c.', 'd.']:
                if 'choices' in question:
                    question['choices'].append(value)
                else:
                    warnings.append(f"Choice {key} found before 'a.' in table {table_index + 1}")
            elif key == 'answer':
                question['correct_answer'] = value
            elif key == 'mark':
                try:
                    question['mark'] = float(value)
                except ValueError:
                    warnings.append(f"Invalid mark value in table {table_index + 1}")
            elif key == 'unit':
                question['unit'] = value
            elif key == 'mix choices':
                question['mix_choices'] = value.lower() == 'yes'

        if 'text' not in question:
            warnings.append(f"Question text is missing in table {table_index + 1}")
        if 'choices' not in question or len(question.get('choices', [])) < 2:
            warnings.append(f"Insufficient choices in table {table_index + 1}")
        if 'correct_answer' not in question:
            warnings.append(f"Correct answer is missing in table {table_index + 1}")

        if 'text' in question and 'choices' in question and 'correct_answer' in question:
            questions.append(question)

    return metadata, questions, warnings