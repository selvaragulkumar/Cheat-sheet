from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def wrap_text(text, max_width, font_size):
    style = ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=font_size, alignment=0)  # Left alignment
    p = Paragraph(text, style=style)
    width, height = p.wrap(max_width, None)
    return p, height

def adjust_cell_height(text, col_width, font_size):
    style = ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=font_size, alignment=0)
    p = Paragraph(text, style=style)
    # Wrap text to fit within the column width
    width, height = p.wrap(col_width, None)
    return height, p

def draw_table(pdf_canvas, data, col_widths, y_position):
    max_width = letter[0] - 80  # 40 points margin on each side
    col_widths = [min(width, max_width / len(col_widths)) for width in col_widths]
    
    # Wrap text and calculate cell heights
    wrapped_data = []
    cell_heights = []
    for row in data:
        wrapped_row = []
        row_heights = []
        for i, cell in enumerate(row):
            cell_width = col_widths[i]
            cell_height, wrapped_paragraph = adjust_cell_height(cell, cell_width, 12)
            wrapped_row.append(wrapped_paragraph)
            row_heights.append(cell_height)
        wrapped_data.append(wrapped_row)
        cell_heights.append(max(row_heights))
    
    # Create a Table and calculate its height
    table = Table([[p for p in row] for row in wrapped_data], colWidths=col_widths, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    
    # Measure the height of the table
    table_width, table_height = table.wrapOn(pdf_canvas, 40, y_position)
    
    if y_position - table_height < 40:
        pdf_canvas.showPage()
        pdf_canvas.setFont("Helvetica", 12)
        y_position = 750
    
    table.drawOn(pdf_canvas, 40, y_position - table_height)
    
    return y_position - table_height - 20

def add_json_to_pdf(pdf_canvas, json_data, title, y_position):
    styles = getSampleStyleSheet()
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(40, y_position, title)
    
    y_position -= 20
    
    for key, value in json_data.items():
        if isinstance(value, list):
            if all(isinstance(item, dict) for item in value):
                # Create a table for a list of dictionaries
                column_names = list(value[0].keys())
                data = [column_names]
                for item in value:
                    data.append([str(item.get(col, '')) for col in column_names])
                
                # Calculate column widths based on content
                col_widths = [letter[0] / len(column_names) - 80 / len(column_names) for _ in column_names]
                y_position = draw_table(pdf_canvas, data, col_widths, y_position)
            elif all(isinstance(item, str) for item in value):
                # Create a table for a list of strings
                data = [[item] for item in value]
                col_widths = [letter[0] - 80]  # Width for single column
                y_position = draw_table(pdf_canvas, data, col_widths, y_position)
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, list):
                    if all(isinstance(item, dict) for item in sub_value):
                        # Create a table for a list of dictionaries
                        column_names = list(sub_value[0].keys())
                        data = [column_names]
                        for item in sub_value:
                            data.append([str(item.get(col, '')) for col in column_names])
                        
                        col_widths = [letter[0] / len(column_names) - 80 / len(column_names) for _ in column_names]
                        y_position = draw_table(pdf_canvas, data, col_widths, y_position)
                    elif all(isinstance(item, str) for item in sub_value):
                        # Create a table for a list of strings
                        data = [[item] for item in sub_value]
                        col_widths = [letter[0] - 80]  # Width for single column
                        y_position = draw_table(pdf_canvas, data, col_widths, y_position)
                elif isinstance(sub_value, dict):
                    # Recursively handle nested dictionaries
                    y_position = add_json_to_pdf(pdf_canvas, sub_value, sub_key, y_position)
        elif isinstance(value, str):
            # Break text into lines of up to 9 words
            words = value.split()
            lines = [' '.join(words[i:i+9]) for i in range(0, len(words), 9)]
            text = '<br/>'.join(lines)
            p, height = wrap_text(text, letter[0] - 80, 12)
            p.wrapOn(pdf_canvas, letter[0] - 80, y_position)
            p.drawOn(pdf_canvas, 40, y_position - height)
            y_position -= height + 20
    
    return y_position

def generate_pdf_from_json(json_file, output_pdf):
    pdf = SimpleDocTemplate(output_pdf, pagesize=letter)
    pdf_canvas = canvas.Canvas(output_pdf, pagesize=letter)
    
    import json
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    y_position = 750
    
    for key, value in data.items():
        y_position = add_json_to_pdf(pdf_canvas, {key: value}, key, y_position)
    
    pdf_canvas.save()

# Example usage
generate_pdf_from_json('cheat_sheet_json.json', 'cheat_sheet.pdf')
