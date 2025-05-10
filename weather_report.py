import sqlite3
from datetime import datetime
def generate_html_report(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM weather_data")
    rows = cursor.fetchall()

    print("Data from weather_data table:")
    for row in rows:
        print(row)

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather Data Report</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>

        <h1>Weather Data Report</h1>
        <table>
            <tr>
                <th>City Name</th>
                <th>Temperature (°C) - Web</th>
                <th>Feels Like (°C) - Web</th>
                <th>Temperature (°C) - API</th>
                <th>Feels Like (°C) - API</th>
            </tr>
    """


    for row in rows:
        if len(row) == 6:
            city_name, temperature_web, feels_like_web, temperature_api, feels_like_api, _ = row
            html_content += f"""
            <tr>
                <td>{city_name}</td>
                <td>{temperature_web} °C</td>
                <td>{feels_like_web} °C</td>
                <td>{temperature_api} °C</td>
                <td>{feels_like_api} °C</td>
            </tr>
            """
        else:
            print(f"Invalid row: {row}")

    html_content += """
        </table>
    </body>
    </html>
    """

    # Create a dynamic filename with date
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f'weather_report_{timestamp}.html'

    # Saving the report as an HTML file
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(html_content)

    conn.close()
