# Chaotix Assignment

This project generates images using Stability AI's Text-to-image generation API, with Django, Celery, and WebSockets for real-time updates.

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Redis (for Celery)
- A Stability AI API key

### Installation

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd chaotix_assignment
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv env
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```bash
        .\env\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source env/bin/activate
        ```

4. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Create a `.env` file:**

    ```bash
    cp .env.example .env
    ```

    Edit the `.env` file to set your Stability AI API key and any other necessary environment variables.

6. **Apply migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. **Start Celery for background tasks:**

    ```bash
    celery -A chaotix_assignment worker --loglevel=info
    ```

8. **Run the Django development server:**

    ```bash
    python manage.py runserver
    ```

### Usage

Once the server is running, you can access the application at:

- Django: [https://127.0.0.1:8000](https://127.0.0.1:8000)
- API Endpoint: [https://127.0.0.1:8000/api/v1/generate/](https://127.0.0.1:8000/api/v1/generate/)

### Changing the Prompt For Apis Response

To change the prompt, you need to modify the code in `base/api/views.py`.



