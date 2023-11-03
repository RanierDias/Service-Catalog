from dotenv import load_dotenv
import os


load_dotenv()

link = os.getenv("LINK_CONFIRM")


def template_confirm_acount(token: str):
    template = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1);
                }}
                .header {{
                    background-color: #4CAF50;
                    color: #ffffff;
                    padding: 10px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    padding: 20px;
                }}
                .button {{
                    display: block;
                    width: 200px;
                    background-color: #4CAF50;
                    color: #ffffff;
                    text-align: center;
                    padding: 10px;
                    margin: 20px auto;
                    border-radius: 5px;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Confirme seu endereço de e-mail</h2>
                </div>
                <div class="content">
                    <p>Clique no botão abaixo para confirmar seu endereço de e-mail:</p>
                    <a class="button" href="{link + token}">Confirmar E-mail</a>
                </div>
            </div>
        </body>
    </html>"""
    
    return template
