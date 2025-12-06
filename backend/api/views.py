# backend/api/views.py
# Universal Data Analyzer - Works with ANY file type!

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.conf import settings
import pandas as pd
import io
from openai import OpenAI
import PyPDF2
import pdfplumber

# Store uploaded data in memory
uploaded_data = None
file_metadata = {}

def extract_pdf_tables(file):
    """Extract tables from PDF using pdfplumber"""
    try:
        pdf = pdfplumber.open(io.BytesIO(file.read()))
        all_tables = []
        
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    all_tables.append(table)
        
        pdf.close()
        
        if all_tables:
            # Convert first table to DataFrame
            df = pd.DataFrame(all_tables[0][1:], columns=all_tables[0][0])
            return df
        
        return None
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return None

def extract_pdf_text(file):
    """Extract raw text from PDF"""
    try:
        file.seek(0)  # Reset file pointer
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        return text
    except Exception as e:
        print(f"PDF text extraction error: {e}")
        return None

def smart_csv_read(file):
    """Auto-detect CSV delimiter and read"""
    try:
        # Try common delimiters
        delimiters = [',', ';', '\t', '|']
        
        for delimiter in delimiters:
            try:
                file.seek(0)
                df = pd.read_csv(io.BytesIO(file.read()), delimiter=delimiter)
                if len(df.columns) > 1:  # Successfully parsed
                    return df
            except:
                continue
        
        # Default to comma
        file.seek(0)
        return pd.read_csv(io.BytesIO(file.read()))
    except Exception as e:
        print(f"CSV read error: {e}")
        return None

def analyze_data_with_ai(df, query):
    """Use AI to understand data and answer query"""
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Get data summary
        columns = df.columns.tolist()
        dtypes = df.dtypes.to_dict()
        sample_data = df.head(3).to_dict('records')
        total_rows = len(df)
        
        # Identify numeric and text columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Basic statistics for numeric columns
        stats = {}
        for col in numeric_cols[:5]:  # Limit to 5 columns
            stats[col] = {
                'mean': float(df[col].mean()),
                'min': float(df[col].min()),
                'max': float(df[col].max())
            }
        
        prompt = f"""You are a data analyst. Analyze this dataset and answer the user's query.

DATASET INFO:
- Total Rows: {total_rows}
- Columns: {columns}
- Column Types: {dtypes}
- Numeric Columns: {numeric_cols}
- Text Columns: {text_cols}

STATISTICS:
{stats}

SAMPLE DATA (first 3 rows):
{sample_data}

USER QUERY: {query}

Please provide:
1. A clear answer to the user's query based on the data
2. Key insights from the data
3. Any trends or patterns you notice
4. Recommendations or next steps

Format your response in a friendly, conversational way. Use emojis where appropriate. Keep it under 250 words."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert data analyst who can understand any type of dataset and provide insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"AI analysis error: {e}")
        return generate_fallback_analysis(df, query)

def generate_fallback_analysis(df, query):
    """Basic analysis without AI"""
    try:
        columns = df.columns.tolist()
        rows = len(df)
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        summary = f"""📊 Dataset Overview:

• Total Records: {rows}
• Columns: {', '.join(columns[:5])}{'...' if len(columns) > 5 else ''}
• Numeric Fields: {len(numeric_cols)}

Query: "{query}"

This dataset contains {rows} records with {len(columns)} columns. """
        
        if numeric_cols:
            col = numeric_cols[0]
            avg = df[col].mean()
            summary += f"Average {col}: {avg:.2f}"
        
        return summary
    except:
        return "Dataset loaded successfully. Please ask specific questions about the data."

def prepare_chart_data(df, query):
    """Intelligently prepare chart data based on query and data structure"""
    try:
        # Find date/year column
        date_col = None
        for col in df.columns:
            if any(word in str(col).lower() for word in ['year', 'date', 'time', 'period', 'month']):
                date_col = col
                break
        
        # Find numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not date_col or not numeric_cols:
            return []
        
        # Group by date and aggregate first numeric column
        chart_data = []
        value_col = numeric_cols[0]
        
        grouped = df.groupby(date_col)[value_col].mean().reset_index()
        
        for _, row in grouped.head(20).iterrows():  # Limit to 20 points
            chart_data.append({
                'category': str(row[date_col]),
                'value': float(row[value_col]),
                'label': value_col
            })
        
        return chart_data
    
    except Exception as e:
        print(f"Chart data error: {e}")
        return []

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def upload_file(request):
    """
    Universal file upload handler
    Supports: PDF, Excel (.xlsx, .xls), CSV, TSV
    """
    global uploaded_data, file_metadata
    
    try:
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=400)
        
        file = request.FILES['file']
        filename = file.name.lower()
        
        print(f"📁 Received file: {filename}")
        
        # Handle different file types
        if filename.endswith('.pdf'):
            print("📄 Processing PDF...")
            df = extract_pdf_tables(file)
            
            if df is None:
                # Try extracting text if no tables found
                file.seek(0)
                text = extract_pdf_text(file)
                if text:
                    return Response({
                        'message': 'PDF uploaded (text-only)',
                        'rows': 0,
                        'columns': [],
                        'sample_areas': [],
                        'text_preview': text[:500] + '...',
                        'note': 'This PDF contains text but no structured tables. You can ask questions about the content.'
                    })
                return Response({'error': 'Could not extract data from PDF. Please ensure it contains tables or structured data.'}, status=400)
        
        elif filename.endswith('.csv') or filename.endswith('.tsv'):
            print("📊 Processing CSV/TSV...")
            df = smart_csv_read(file)
        
        elif filename.endswith(('.xlsx', '.xls')):
            print("📗 Processing Excel...")
            df = pd.read_excel(io.BytesIO(file.read()))
        
        else:
            return Response({'error': 'Unsupported file type. Please upload PDF, Excel, or CSV files.'}, status=400)
        
        if df is None or df.empty:
            return Response({'error': 'Could not read file or file is empty'}, status=400)
        
        # Store data
        uploaded_data = df
        file_metadata = {
            'filename': file.name,
            'rows': len(df),
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.astype(str).to_dict()
        }
        
        print(f"✅ File processed: {len(df)} rows, {len(df.columns)} columns")
        
        # Get sample values from first few rows
        sample_values = []
        text_cols = df.select_dtypes(include=['object']).columns
        
        for col in text_cols[:3]:  # First 3 text columns
            unique_vals = df[col].dropna().unique()[:5]
            sample_values.extend([str(v) for v in unique_vals])
        
        return Response({
            'message': f'✅ {file.name} uploaded successfully!',
            'rows': len(df),
            'columns': df.columns.tolist(),
            'sample_areas': sample_values,
            'data_types': {
                'numeric': df.select_dtypes(include=['number']).columns.tolist(),
                'text': df.select_dtypes(include=['object']).columns.tolist(),
                'dates': df.select_dtypes(include=['datetime']).columns.tolist()
            }
        })
    
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': f'Error processing file: {str(e)}'}, status=500)

@api_view(['POST'])
def analyze_query(request):
    """
    Universal query analyzer - works with any dataset
    """
    global uploaded_data
    
    try:
        if uploaded_data is None:
            return Response({'error': 'Please upload a file first'}, status=400)
        
        query = request.data.get('query', '').strip()
        
        if not query:
            return Response({'error': 'Query is required'}, status=400)
        
        df = uploaded_data.copy()
        
        print(f"\n🔍 Query: {query}")
        print(f"📊 Data: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Try to filter data based on query keywords
        filtered_df = df
        query_lower = query.lower()
        
        # Search in text columns for keywords
        text_cols = df.select_dtypes(include=['object']).columns
        for col in text_cols:
            if any(word in df[col].astype(str).str.lower().values for word in query_lower.split() if len(word) > 3):
                mask = df[col].astype(str).str.lower().str.contains('|'.join([w for w in query_lower.split() if len(w) > 3]), na=False, regex=True)
                if mask.any():
                    filtered_df = df[mask]
                    print(f"✅ Filtered by {col}: {len(filtered_df)} rows")
                    break
        
        # Generate AI analysis
        print("🤖 Generating AI analysis...")
        summary = analyze_data_with_ai(filtered_df, query)
        
        # Prepare chart data
        chart_data = prepare_chart_data(filtered_df, query)
        
        # Prepare table data
        table_data = filtered_df.head(50).to_dict('records')
        
        print(f"✅ Returning: {len(chart_data)} chart points, {len(table_data)} table rows")
        
        return Response({
            'summary': summary,
            'chart_data': chart_data,
            'table_data': table_data,
            'metadata': {
                'total_rows': len(filtered_df),
                'columns_used': filtered_df.columns.tolist()
            }
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': f'Server error: {str(e)}'}, status=500)

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'Universal Data Analyzer is running! 🤖📊'})