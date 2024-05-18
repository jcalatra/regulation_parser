import re
import json

def read_text(filename):
    texto = ""
    with open(filename, 'r') as file:
        texto = file.read()
    return texto
        
def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def parse_legal_text(text):
    # Define patterns for different sections
    pattern_article = r'Article\s+(\d+)[^\S\n]*\n(.*?)(?=(Article\s+\d+|\Z))'
    pattern_section = r'Section\s+(\d+)[^\S\n]*\n(.*?)(?=(Section\s+\d+|Article\s+\d+|\Z))'
    pattern_disposition = r'Disposition\s+(\d+)[^\S\n]*\n(.*?)(?=(Disposition\s+\d+|Section\s+\d+|Article\s+\d+|\Z))'

    # Initialize dictionary to store parsed data
    parsed_data = {'articles': []}

    # Parse articles
    articles = re.findall(pattern_article, text, re.DOTALL)
    for article_match in articles:
        article_number = article_match[0]
        article_content = article_match[1].strip()
        article_data = {'number': article_number, 'content': article_content, 'sections': []}

        # Parse sections within the article
        sections = re.findall(pattern_section, article_content)
        for section_match in sections:
            section_number = section_match[0]
            section_content = section_match[1].strip()
            section_data = {'number': section_number, 'content': section_content, 'dispositions': []}

            # Parse dispositions within the section
            dispositions = re.findall(pattern_disposition, section_content)
            for disposition_match in dispositions:
                disposition_number = disposition_match[0]
                disposition_content = disposition_match[1].strip()
                disposition_data = {'number': disposition_number, 'content': disposition_content}
                section_data['dispositions'].append(disposition_data)

            article_data['sections'].append(section_data)

        parsed_data['articles'].append(article_data)

    return parsed_data

text = read_text('texto.txt')
parsed_data = parse_legal_text(text)
save_to_json(parsed_data, 'legal_text.json')
