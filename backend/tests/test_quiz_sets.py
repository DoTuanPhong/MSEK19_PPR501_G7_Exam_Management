import pytest
import docx
from io import BytesIO
from datetime import datetime
from app.utils.docx_parser import parse_docx

def test_parse_docx_with_sample_file():
    file_path = r"F:\FSB\Python for Engineer\Week 2 - 1\Template 2.docx"
    
    # Call the parse_docx function with the sample file
    info, questions, warnings = parse_docx(file_path)
    
    # Print results for debugging purposes
    print("info:", info)
    print("Questions:", questions)
    print("Warnings:", warnings)
    
    # Check info (adjust the expected values based on the actual content of your template)
    assert info['subject'] == 'ISC'
    assert info['num_quiz'] == 30
    assert info['lecturer'] == 'hungpd2'
    assert info['date'] == datetime.strptime('22-08-1999', '%d-%m-%Y').date()  # Adjust date as per your template
    
    # Check questions
    assert len(questions) == 26  # Ensure there's at least one question
  
  
    # Validate the first question (adjust the expected values based on the actual content of your template)
    question = questions[2]
    print("Image: ", question['image'][:50])
    assert info['num_quiz'] == 3
    assert 'text' in question
    assert 'choices' in question
    assert 'correct_answer' in question
    assert 'mark' in question
    assert 'unit' in question
    assert 'mix_choices' in question
    assert 'image' in question

    
    # Check warnings
    assert len(warnings) == 0  # Ensure there are no warnings for a correctly formatted document
