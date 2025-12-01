# backend/api/views.py
# Updated with REAL OpenAI integration

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.conf import settings
import pandas as pd
import io
from openai import OpenAI

# Store uploaded data in memory (for this session)
uploaded_data = None

def generate_ai_summary(area_name, filtered_data, avg_price, total_properties, latest_year):
    """Generate REAL AI summary using OpenAI GPT"""
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Prepare data for AI
        price_range = f"₹{filtered_data['price_col'].min():,.0f} - ₹{filtered_data['price_col'].max():,.0f}"
        
        # Get sample data points
        sample_data = filtered_data.head(5).to_dict('records')
        
        # Create prompt for AI
        prompt = f"""You are a real estate market analyst. Analyze this data and provide insights:

Area: {area_name}
Total Properties: {total_properties}
Average Price: ₹{avg_price:,.2f}
Price Range: {price_range}
Latest Year: {int(latest_year)}

Sample Data:
{sample_data}

Please provide:
1. A brief market overview (2-3 sentences)
2. Investment recommendation (Strong Buy/Buy/Hold/Avoid with reasoning)
3. Key trend insights
4. Price competitiveness analysis

Keep the response conversational, insightful, and under 200 words. Use emojis appropriately."""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cheapest and fast model
            messages=[
                {"role": "system", "content": "You are an expert real estate analyst providing data-driven insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        ai_summary = response.choices[0].message.content
        
        return f"""🏘️ Real Estate Analysis for {area_name}

📊 Quick Stats:
• Properties Analyzed: {total_properties}
• Average Price: ₹{avg_price:,.2f}
• Latest Data: {int(latest_year)}

🤖 AI Analysis:
{ai_summary}

---
Powered by GPT-4o-mini
"""
    
    except Exception as e:
        print(f"OpenAI Error: {e}")
        # Fallback to rule-based if API fails
        return generate_fallback_summary(area_name, avg_price, total_properties, latest_year)

def generate_fallback_summary(area_name, avg_price, total_properties, latest_year):
    """Fallback summary if OpenAI fails"""
    
    if avg_price > 8000:
        market_strength = "exceptionally strong"
        investment_advice = "This is a premium locality with high property values. Excellent for luxury investments."
    elif avg_price > 5000:
        market_strength = "strong"
        investment_advice = "This area shows robust market performance. Good potential for appreciation."
    elif avg_price > 3000:
        market_strength = "moderate"
        investment_advice = "This is a developing area with reasonable prices. Suitable for first-time buyers."
    else:
        market_strength = "emerging"
        investment_advice = "This is an affordable locality with growth potential. Consider for long-term investment."
    
    summary = f"""🏘️ Real Estate Analysis for {area_name}

📊 Key Insights:
• Properties Analyzed: {total_properties}
• Average Price: ₹{avg_price:,.2f}
• Latest Data Year: {int(latest_year)}
• Market Strength: {market_strength.title()}

💡 Recommendation:
{investment_advice}

📈 Trend Analysis:
Based on the available data, this locality shows {market_strength} market characteristics. The average property price of ₹{avg_price:,.2f} positions it well within its segment.
"""
    return summary.strip()

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def upload_file(request):
    """
    Handle file upload
    Accepts Excel (.xlsx, .xls) or CSV files
    """
    global uploaded_data
    
    try:
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=400)
        
        file = request.FILES['file']
        
        # Check file type
        if file.name.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file.read()))
        elif file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(file.read()))
        else:
            return Response({'error': 'Please upload Excel (.xlsx, .xls) or CSV file'}, status=400)
        
        # Store in memory
        uploaded_data = df
        
        print(f"✅ File uploaded: {len(df)} rows, {len(df.columns)} columns")
        
        # Get basic info
        columns = df.columns.tolist()
        rows = len(df)
        
        # Get unique areas (try to find area column)
        area_col = None
        for col in columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['area', 'location', 'locality', 'city', 'place', 'region']):
                area_col = col
                break
        
        unique_areas = []
        if area_col:
            # Get unique values and convert to string
            unique_vals = df[area_col].dropna().unique()
            unique_areas = [str(val) for val in unique_vals if str(val).strip() and str(val) != 'nan'][:10]
        
        print(f"📍 Detected area column: {area_col}")
        print(f"📍 Sample areas: {unique_areas[:5]}")
        
        return Response({
            'message': 'File uploaded successfully!',
            'rows': rows,
            'columns': columns,
            'sample_areas': unique_areas
        })
    
    except Exception as e:
        print(f"Upload error: {e}")
        return Response({'error': f'Error processing file: {str(e)}'}, status=500)

@api_view(['POST'])
def analyze_query(request):
    """
    Analyze query based on uploaded data using REAL AI
    """
    global uploaded_data
    
    try:
        if uploaded_data is None:
            return Response({'error': 'Please upload a file first'}, status=400)
        
        query = request.data.get('query', '').strip()
        
        if not query:
            return Response({'error': 'Query is required'}, status=400)
        
        df = uploaded_data.copy()
        
        print(f"\n🔍 Processing query: {query}")
        print(f"📊 DataFrame: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Get column names
        columns = df.columns.tolist()
        
        # Find important columns
        area_col = None
        price_col = None
        year_col = None
        
        for col in columns:
            col_lower = str(col).lower()
            # Find area/location column
            if any(keyword in col_lower for keyword in ['area', 'location', 'locality', 'city', 'place', 'region']):
                if area_col is None:  # Take first match
                    area_col = col
            # Find price column
            if any(keyword in col_lower for keyword in ['price', 'cost', 'rate', 'sold', 'sale', 'value']):
                if price_col is None:
                    price_col = col
            # Find year column
            if any(keyword in col_lower for keyword in ['year', 'date', 'time', 'period']):
                if year_col is None:
                    year_col = col
        
        # Fallback to column positions if not found
        if year_col is None:
            year_col = columns[0]
        if area_col is None and len(columns) > 1:
            area_col = columns[1]
        if price_col is None and len(columns) > 2:
            price_col = columns[2]
        
        print(f"📍 Detected columns:")
        print(f"   Year: {year_col}")
        print(f"   Area: {area_col}")
        print(f"   Price: {price_col}")
        print(f"   All columns: {columns}")
        
        # Filter data based on query
        query_lower = query.lower()
        df['area_search'] = df[area_col].astype(str).str.lower()
        
        # Search for matching areas
        filtered_df = pd.DataFrame()
        words = [w for w in query_lower.split() if len(w) > 2]
        
        for word in words:
            temp_df = df[df['area_search'].str.contains(word, na=False)]
            if not temp_df.empty:
                filtered_df = pd.concat([filtered_df, temp_df])
                break
        
        # Remove duplicates
        filtered_df = filtered_df.drop_duplicates()
        
        if filtered_df.empty:
            available_areas = df[area_col].unique()[:5]
            return Response({
                'summary': f"❌ No data found for '{query}'.\n\n📍 Try these areas:\n" + "\n".join([f"• {area}" for area in available_areas]),
                'chart_data': [],
                'table_data': []
            })
        
        # Calculate statistics
        areas = filtered_df[area_col].unique()
        area_name = ', '.join([str(a) for a in areas[:3]])
        
        avg_price = filtered_df[price_col].mean()
        total_properties = len(filtered_df)
        latest_year = filtered_df[year_col].max()
        
        # Add price_col to filtered_df for AI
        filtered_df['price_col'] = filtered_df[price_col]
        
        print(f"🤖 Generating AI summary...")
        
        # Generate REAL AI summary
        summary = generate_ai_summary(area_name, filtered_df, avg_price, total_properties, latest_year)
        
        print(f"✅ Summary generated!")
        
        # Prepare chart data
        chart_data = []
        try:
            for area in areas[:3]:
                area_data = filtered_df[filtered_df[area_col] == area]
                yearly_avg = area_data.groupby(year_col)[price_col].mean().reset_index()
                
                for _, row in yearly_avg.iterrows():
                    chart_data.append({
                        'area': str(area),
                        'year': int(float(row[year_col])),
                        'price': float(row[price_col])
                    })
        except Exception as e:
            print(f"Chart error: {e}")
        
        # Prepare table data
        try:
            display_cols = [col for col in [year_col, area_col, price_col] if col in filtered_df.columns]
            other_cols = [col for col in columns if col not in display_cols][:3]
            display_cols.extend(other_cols)
            
            table_data = filtered_df[display_cols].head(50).to_dict('records')
        except Exception as e:
            print(f"Table error: {e}")
            table_data = []
        
        print(f"📤 Returning: {len(chart_data)} chart points, {len(table_data)} table rows")
        
        return Response({
            'summary': summary,
            'chart_data': chart_data,
            'table_data': table_data
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': f'Server error: {str(e)}'}, status=500)

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'Backend is running with AI! 🤖'})