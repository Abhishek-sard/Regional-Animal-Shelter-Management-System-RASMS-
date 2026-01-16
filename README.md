# Regional Animal Shelter Management System (RASMS)

**RASMS** is a comprehensive solution designed for the Regional Animal Welfare Authority to track animals, manage shelters, and handle adoptions across South Australia.

## 🚀 Features

### Core Management
- **Shelter Tracking**: Manage 10+ shelters across locations like Glenelg, Adelaide Hills, and more.
- **Animal Inventory**: Track animals by ID, name, type (Dog, Cat, Rabbit, etc.), age, and health status.
- **Move Animals**: Transfer animals between shelters with ease.
- **Update Status**: Update animal health (e.g., Healthy, Injured) and adoption status.

### Premium Web Dashboard
- **Visual Analytics**: Real-time charts showing revenue trends and animal population.
- **Live Search**: Instantly find animals in the inventory by typing their name or breed.
- **Revenue Reporting**: Detailed breakdown of adoption fees collecting across the region.
- **Automatic Fee Calculation**: Smart logic determines adoption fees based on animal type and age.

### Dual Interface
- **Web Application**: Modern, responsive UI managed via Flask.
- **CLI Mode**: Traditional command-line interface for quick backend operations.

---

## 🛠️ Prerequisites

- Python 3.x
- Flask (`pip install flask`)

## 📦 Installation

1. Clone or unzip the project folder.
2. Install the required dependencies:
   ```bash
   pip install flask
   ```

## ▶️ How to Run

### Option 1: Web Interface (Recommended)
This launches the modern web dashboard.
```bash
python app.py
```
> Open your browser and go to: `http://127.0.0.1:5000`

### Option 2: Command Line Interface (CLI)
This launches the text-based menu system.
```bash
python rasms.py
```

### Option 3: VS Code
- Open the project in VS Code.
- Go to the **Run and Debug** tab.
- Select **"Run RASMS Web App"** and hit Play.

---

## 📂 Project Structure

- **`app.py`**: Main Flask application file (Web Server).
- **`rasms.py`**: Core business logic and CLI implementation.
- **`shelters_data.json`**: Database file storing all shelter and animal records.
- **`templates/`**: HTML files for the web interface (Dashboard, Inventory, Forms).
- **`static/`**: CSS and assets for styling.

## 📝 Author
Developed by **Abhishek Sardar** for Task 2 Programming Assignment.
