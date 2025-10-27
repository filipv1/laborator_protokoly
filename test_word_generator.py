"""
Simple Word generator - replaces placeholders in Word template with JSON data
Usage: python test_word_generator.py <json_file>
"""
import sys
import json
from docxtpl import DocxTemplate, RichText


def add_purple_highlight(data):
    """Recursively wraps all string/number values in RichText with violet highlight"""
    if isinstance(data, dict):
        return {k: add_purple_highlight(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [add_purple_highlight(item) for item in data]
    elif isinstance(data, str):
        return RichText(data, highlight='violet')
    elif isinstance(data, (int, float)):
        return RichText(str(data), highlight='violet')
    else:
        return data


# Get JSON file from command line argument
if len(sys.argv) < 2:
    print("Usage: python test_word_generator.py <json_file>")
    sys.exit(1)

json_file = sys.argv[1]

# Load JSON data
with open(json_file, encoding='utf-8') as f:
    data = json.load(f)

# Add purple highlight to all values
data_with_highlight = add_purple_highlight(data)

# Load Word template
template_path = r"Vzorové protokoly\Autorizované protokoly pro MUŽE\lsz_placeholdery_v2.docx"
doc = DocxTemplate(template_path)

# Render template with data
doc.render(data_with_highlight)

# Save output
output_path = "LSZ_vyplneny.docx"
doc.save(output_path)

print(f"✓ Word vygenerován: {output_path}")
