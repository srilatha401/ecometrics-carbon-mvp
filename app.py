import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from google import genai

app = Flask(__name__)
app.secret_key = "eco_metrics_secure_key"

# Database Configuration Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          
        password="mention your mysql passward",  # <-- Your updated MySQL password
        database="ecometrics_db"
    )

# Initialize Gemini Client using your provided credential key
ai_client = genai.Client()


@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Fetch total emissions broken down by energy type
    query = """
        SELECT c.energy_type, SUM(c.amount * f.factor_per_unit) as total_co2
        FROM consumption_logs c
        JOIN emission_factors f ON c.energy_type = f.energy_type
        GROUP BY c.energy_type
    """
    cursor.execute(query)
    breakdown = cursor.fetchall()
    
    # Calculate aggregate metrics
    total_emissions = sum(item['total_co2'] for item in breakdown)
    
    # 2. Get AI Insights via Gemini API
    ai_insights = "No data available to generate insights."
    if total_emissions > 0:
        data_summary = ", ".join([f"{item['energy_type']}: {item['total_co2']:.2f} MTCO2e" for item in breakdown])
        
        # FIXED INDENTATION LOGIC BLOCK HERE
        try:
            # Attempt to call the latest live model
            response = ai_client.models.generate_content(
                model='gemini-3.8-flash',
                contents=f"As a corporate sustainability expert, provide 3 bulleted, practical recommendations based on this monthly carbon footprint profile: Total emissions {total_emissions:.2f} MTCO2e broken down by: {data_summary}. Keep it concise and professional.",
            )
            ai_insights = response.text
        except Exception as e:
            # Smart Fallback: Displays clean, standard advisory tips if the API is busy
            ai_insights = (
                "🌱 *Notice: Live advisory server is busy. Displaying baseline recommendations:*\n\n"
                "• **Optimize HVAC Systems:** Program smart thermostats to adjust temperatures during non-business hours to lower facility fuel emissions.\n"
                "• **Transition to LED Lighting:** Retrofit warehouse and office light fixtures to cut commercial electricity consumption by up to 30%.\n"
                "• **Implement Energy Audits:** Track monthly billing peaks to identify machinery or equipment causing unnatural consumption spikes."
            )
            
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', total_emissions=total_emissions, breakdown=breakdown, ai_insights=ai_insights)

@app.route('/input', methods=['GET', 'POST'])
def data_input():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        facility_id = request.form['facility_id']
        log_month = request.form['log_month']
        energy_type = request.form['energy_type']
        amount = request.form['amount']
        
        # Get standard unit mapping
        cursor.execute("SELECT unit FROM emission_factors WHERE energy_type = %s", (energy_type,))
        unit_res = cursor.fetchone()
        unit = unit_res['unit'] if unit_res else 'units'
        
        # Insert raw log entry into MySQL
        insert_query = """
            INSERT INTO consumption_logs (facility_id, log_month, energy_type, amount, unit)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (facility_id, log_month, energy_type, amount, unit))
        conn.commit()
        return redirect(url_for('dashboard'))
        
    cursor.execute("SELECT * FROM facilities")
    facilities = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('input.html', facilities=facilities)

if __name__ == '__main__':
    app.run(debug=True)
