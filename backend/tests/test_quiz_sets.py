import pytest
import docx
from io import BytesIO
from datetime import datetime
from app.utils.docx_parser import parse_docx

def test_parse_docx_with_sample_file():
    file_path = r"F:\FSB\Python for Engineer\Week 2 - 1\Template.docx"
    
    # Call the parse_docx function with the sample file
    metadata, questions, warnings = parse_docx(file_path)
    
    # Print results for debugging purposes
    print("Metadata:", metadata)
    print("Questions:", questions)
    print("Warnings:", warnings)
    
    # Check metadata (adjust the expected values based on the actual content of your template)
    assert metadata['subject'] == 'ISC'
    assert metadata['number_of_quiz'] == 30
    assert metadata['lecturer'] == 'hungpd2'
    assert metadata['date'] == datetime.strptime('01-01-2022', '%d-%m-%Y').date()  # Adjust date as per your template
    
    # Check questions
    assert len(questions) > 0  # Ensure there's at least one question
    
    # Validate the first question (adjust the expected values based on the actual content of your template)
    question = questions[0]
    assert 'text' in question
    assert 'choices' in question
    assert 'correct_answer' in question
    assert 'mark' in question
    assert 'unit' in question
    assert 'mix_choices' in question
    
    # Check warnings
    assert len(warnings) == 0  # Ensure there are no warnings for a correctly formatted document

# Run tests
if __name__ == "__main__":
    pytest.main()
