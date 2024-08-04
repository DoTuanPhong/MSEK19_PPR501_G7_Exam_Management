import docx
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime
from docx.oxml.shared import qn

def parse_docx(file_path):
    doc = docx.Document(file_path)
    info = {}
    questions = []
    warnings = []

    # Process metadata
    for para in doc.paragraphs:
        text = para.text.strip()
        if text.startswith("Subject:"):
            try:
                info['subject'] = text.split(":", 1)[1].strip()
            except IndexError:
                warnings.append("Subject format is incorrect.")
        elif text.startswith("Number of Quiz:"):
            try:
                info['num_quiz'] = int(text.split(":", 1)[1].strip())
            except (ValueError, IndexError):
                warnings.append("Number of Quiz format is incorrect.")
        elif text.startswith("Lecturer:"):
            info['lecturer'] = text.split(":", 1)[1].strip()
        elif text.startswith("Date:"):
            try:
                date_str = text.split(":", 1)[1].strip()
                info['date'] = datetime.strptime(date_str, "%d-%m-%Y").date()
            except (ValueError, IndexError):
                warnings.append("Date format is incorrect.")
    if len(info) != 4:
        warnings.append("Missing header information.")

    expected_order = ['qn', 'a.', 'b.', 'c.', 'd.', 'answer', 'mark', 'unit', 'mix choices']
    table_index = 0

    for table in doc.tables:
        question = {}
        order = []

        for row in table.rows:
            if len(row.cells) != 2:
                warnings.append(f"Invalid table format in table {table_index + 1}")
                continue

            key = row.cells[0].text.strip().lower()
            value = row.cells[1].text.strip()
            order.append(key)

            if key.strip().lower().startswith('qn'):
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
            elif key.strip().lower() == 'a.':
                question['choices'] = [value]
            elif key.strip().lower() in ['b.', 'c.', 'd.']:
                if 'choices' in question:
                    question['choices'].append(value)
                else:
                    warnings.append(f"Choice {key} found before 'a.' in table {table_index + 1}")
            elif key.strip().lower() == 'answer':
                question['correct_answer'] = value
            elif key.strip().lower() == 'mark':
                try:
                    question['mark'] = float(value)
                except ValueError:
                    warnings.append(f"Invalid mark value in table {table_index + 1}")
            elif key.strip().lower() == 'unit':
                question['unit'] = value
            elif key.strip().lower() == 'mix choices':
                question['mix_choices'] = value.lower() == 'yes'

        # Ensure keys are in the expected order
        order = list(map(lambda x: x.strip().lower(), order))
        order[0] = order[0][:2]
        if order != expected_order:
            warnings.append(f"Keys are not in the expected order in table {table_index + 1}")

        if 'text' not in question:
            warnings.append(f"Question text is missing in table {table_index + 1}")
        if 'choices' not in question or len(question.get('choices', [])) < 2:
            warnings.append(f"Insufficient choices in table {table_index + 1}")
        if 'correct_answer' not in question:
            warnings.append(f"Correct answer is missing in table {table_index + 1}")

        if 'text' in question and 'choices' in question and 'correct_answer' in question:
            questions.append(question)
        
        table_index += 1

    return info, questions, warnings

