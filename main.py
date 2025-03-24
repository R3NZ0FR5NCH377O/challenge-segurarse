import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

user_name = os.getenv("USER_NAME", "Renzo Franchetto")

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>¡Saludo a Segurarse!</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                overflow: hidden;
            }}
            .container {{
                text-align: center;
                background: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                animation: fadeIn 1s ease-in-out;
            }}
            h1 {{
                color: #2a5298;
                font-size: 2.5em;
                margin: 0;
                animation: bounce 1.5s infinite;
            }}
            p {{
                color: #333;
                font-size: 1.5em;
                margin: 20px 0;
            }}
            .name {{
                color: #e63946;
                font-weight: bold;
                animation: slideIn 1s ease-in-out;
            }}
            .emoji {{
                font-size: 2em;
                animation: spin 2s linear infinite;
                display: inline-block;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            @keyframes bounce {{
                0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
                40% {{ transform: translateY(-20px); }}
                60% {{ transform: translateY(-10px); }}
            }}
            @keyframes slideIn {{
                from {{ transform: translateX(-100%); opacity: 0; }}
                to {{ transform: translateX(0); opacity: 1; }}
            }}
            @keyframes spin {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>¡Hola Segurarse!</h1>
            <p>Soy <span class="name">{user_name}</span></p>
            <span class="emoji">✨</span>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)