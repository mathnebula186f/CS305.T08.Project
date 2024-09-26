# CS305.Project.T08

## Steps to Initialize

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
2. **Install Django if not already installed:**
   ```bash
   pip install django

3. **Navigate to the Backend and Create and Activate a Virtual Environment:**
    ```bash
    cd Backend
    python -m venv env1
    ./env1/Scripts/activate

4. **Install Requirements:**
    ```bash
    pip install -r requirements.txt  
    python -m spacy download en_core_web_md 

5. **Create .env file:**
    Create .env file with variables same as .env.example replacing their values with original credentials

6. **Make Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate 

    In case of conflicts: Delete migrations all files and folders from /Backend/HandymanHive/migrations except __init__.py and run above commands again.

7. **Run Backend**
    ```bash
    python manage.py runserver
8. **Navigate to App folder to install frontend dependencies**
    ```bash
    cd zappfix
    npm i
9. **Run App**
    ```bash
    npx expo start