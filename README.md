# To-do List - Django Project

## Description
This project is a simple web application developed with Django, which allows users to register tasks, view pending tasks, and mark tasks as completed on a weekly basis. The application displays a summary of completed and pending tasks for the current week, with the ability to view the previous week.

## Features
- **Task Registration:** Users can register tasks with a desired weekly frequency.
- **Task Management:** View pending tasks and tasks marked as completed.
- **Weekly Progress:** A progress bar indicating the percentage of tasks completed for the week.
- **Previous Week:** View tasks completed in the previous week.
- **Delete Completed Tasks:** Users can delete completed tasks from the list.

## Technologies Used
- Django (for the web framework)
- Python (as the programming language)
- MySQL (for the database)
- Bootstrap (for additional UI components)

## Installation

### Requirements
- Python 3.8 or higher
- Django 5.1 or higher
- MySQL

### Installation Steps
1. **Clone the repository:**

   ```bash
   git clone https://github.com/uBittencourt/to-do-list.git
2. **Install Dependencies:**
    ```bash
    cd repository-name
    python -m venv venv

    # Activate the virtual environment
    # On Windows
        venv\Scripts\activate

    # On Linux/MacOS
        source venv/bin/activate

    pip install -r requirements.txt
3. **Database Configuration:**
    - Create a MySQL database called _tasks_list_ (or use another name, but update the database settings in the _settings.py_ file).
    - Atualize as credenciais no arquivo _settings.py_:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tasks_list',
            'USER': 'root',  # or your MySQL user
            'PASSWORD': 'your_password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
4. **Run Migrations:**
    ```bash
    python manage.py migrate
5. **Run the Server:**
    ```bash
    python manage.py runserver
The application will be accessible at http://127.0.0.1:8000.

## Page Functionality
### Main Page (/)
- Displays a list of pending tasks for the current week;
- Shows the progress bar with the percentage of completed tasks;
- Allows adding tasks as "completed";
- Displays a summary of completed tasks by date;
- Allows deleting the completion of a task.

### Task Registration Page (/create)
- Allows users to register new tasks and set the desired weekly frequency.

### Previous Week Page (/previous_week)
- Displays a summary of completed and pending tasks from the previous week.

## Contributing
Feel free to contribute! If you find a bug or have suggestions for improvements, please submit a pull request.
