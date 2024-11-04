from functools import wraps
from django.http import JsonResponse
import json
from asgiref.sync import iscoroutinefunction
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime
import pytz

def handle_request(view_func):
    """Decorator to handle request processing and response formatting"""
    @wraps(view_func)
    async def wrapper(request, *args, **kwargs):
        try:
            # For POST/PUT/PATCH requests, parse JSON body
            if request.method in ['POST', 'PUT', 'PATCH']:
                body = json.loads(request.body)
                kwargs['body'] = body
            
            response = await view_func(request, *args, **kwargs)
            return JsonResponse({
                'status': 200,
                'message': 'Success',
                'data': response
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 400,
                'message': 'Invalid JSON in request body',
                'data': {}
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 500,
                'message': str(e),
                'data': {}
            }, status=500)
    
    return wrapper

class ExportUtils:
    @staticmethod
    def generate_excel(data, filename):
        """Generate Excel file from attendance data"""
        df = pd.DataFrame(data)
        
        # Convert timestamps to readable format
        if 'check_in' in df.columns:
            df['check_in'] = pd.to_datetime(df['check_in']).dt.strftime('%Y-%m-%d %H:%M:%S')
        if 'check_out' in df.columns:
            df['check_out'] = pd.to_datetime(df['check_out']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Calculate hours if both check_in and check_out exist
        if 'check_in' in df.columns and 'check_out' in df.columns:
            df['hours'] = pd.to_datetime(df['check_out']) - pd.to_datetime(df['check_in'])
            df['hours'] = df['hours'].dt.total_seconds() / 3600
            df['hours'] = df['hours'].round(2)
        
        # Create Excel writer
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Attendance')
            
            # Auto-adjust columns width
            worksheet = writer.sheets['Attendance']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(str(col))
                )
                worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
        
        output.seek(0)
        return output

    @staticmethod
    def generate_pdf(data, title):
        """Generate PDF report from attendance data"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Add title
        styles = getSampleStyleSheet()
        elements.append(Paragraph(title, styles['Heading1']))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        
        # Prepare data for table
        table_data = [[key for key in data[0].keys()]]
        for item in data:
            row = []
            for key in data[0].keys():
                value = item[key]
                if isinstance(value, datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                row.append(str(value))
            table_data.append(row)
        
        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)
        return buffer
