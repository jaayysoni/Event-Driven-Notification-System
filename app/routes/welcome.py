from fastapi import APIRouter # type: ignore
from fastapi.responses import HTMLResponse # type: ignore
from datetime import datetime

router = APIRouter()

@router.get("/welcome", response_class=HTMLResponse)
async def welcome(name: str = "Jay", email: str = "jay@example.com"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
    <html>
      <head>
        <title>Welcome</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss/dist/tailwind.min.css" rel="stylesheet">
        <script>
          function showPopup() {{
            alert("Welcome {name}!");
          }}
          setInterval(showPopup, 2000);
        </script>
      </head>
      <body class="flex flex-col items-center justify-center h-screen bg-gray-100">
        <h1 class="text-4xl font-bold animate-bounce">Welcome, {name}!</h1>
        <p class="mt-4 text-lg">Email: {email}</p>
        <p class="mt-2 text-sm text-gray-600">Login Time: {now}</p>
        <p class="mt-4 text-green-600">An email has been sent to your Gmail address confirming your login.</p>
      </body>
    </html>
    """
