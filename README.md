# **OpenModelica Model Simulation App**
This repository contains a **Desktop Application** built with **PyQt6** to **Execute the OpenModelica Model Simulation executable**. The app allows users to customize **Start-Time** and **Stop-Time** and **Plots Simulation Data** for selected variables, providing an interactive way to visualize and analyze model behavior dynamically.

![Python](https://img.shields.io/badge/Python-3.6%2B-blue?style=for-the-badge&logo=python)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green?style=for-the-badge&logo=qt)
![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-yellow?style=for-the-badge)
![License](https://img.shields.io/github/license/mhsuhail00/OpenModelica-Model-Simulation-App?style=for-the-badge)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/mhsuhail00/your-repository?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%2010/11-lightgrey?style=for-the-badge)

## **Table of Contents**
- [Features](#features)
- [Installation and Execution Guide](#installation-and-execution-guide)
- [Demo](#-demo-application-in-action)
- [Usage Instructions](#usage-instructions)
- [Build the Executable](#️-build-the-executable)
- [License](#license)
- [Contact](#contact)

## **Features**
### **🎯 Core Functionalities**
1️⃣ **Interactive GUI**:
   - Built with **PyQt6** for a responsive and user-friendly interface.
   - Includes **custom buttons with icons** for improved usability.
   - Supports **mouse and keyboard events** for added interaction.
   - **Tab** button to navigate and **Space** button for click action.

2️⃣ **File Handling**:
   - Restricts file selection to `.exe` files for safety and convenience.
   - Seamless browsing and selection of OpenModelica simulation executables.

3️⃣ **Input Validation**:
   - Ensures input parameters adhere to the required condition:  
     `0 ≤ Start-Time < Stop-Time < 5`.

4️⃣ **Subprocess Execution**:
   - Executes the selected `.exe` file in the background.
   - Displays real-time feedback, including **success or error messages**.

5️⃣ **Graph Plotting**:
   - Dynamically generates **interactive plots** for simulation variables.
   - Allows users to visualize data trends and analyze model behavior.
---

## **Installation and Execution Guide**
Follow these steps to set up the project, run it locally, and export a standalone executable.

### **1️⃣ Clone the Repository**

#### Option 1: Clone the Repository
1. Open your terminal or command prompt.
2. Navigate to the folder where you want to clone the repository.
3. Clone the repository using Git:
   ```bash
   git clone https://github.com/mhsuhail00/OpenModelica-Model-Simulation-App.git
4. Navigate into the project directory:
   ```bash
   cd OpenModelica-Model-Simulation-App/app

 #### Option 2: Download the Repository
 1. Click the green **Code** button at the top of this GitHub repository.
 2. Select **Download ZIP** and save the file to your desired folder.
 3. Extract the ZIP file and navigate into the extracted folder.

### **2️⃣ Set Up the Python Environment**

1. **Check Python Installation**:
   Ensure Python 3.6+ is installed on your system:
   ```bash
   python --version
2. **Create a Virtual Environment**:
   Create a dedicated virtual environment to manage the dependencies:
   ```bash
   python -m venv venv
3. **Activate the Virtual Environment**:
    - On **Windows:** 
      ```bash
      venv\Scripts\activate
    - On **macOS/Linux:** 
      ```bash
      source venv/bin/activate
    
### **3️⃣ Install Dependencies**

1. Use the `requirements.txt` file to install all the necessary libraries:
   ```bash
   pip install -r ../requirements.txt

### **4️⃣ Run the Application**

1. Use the `requirements.txt` file to install all the necessary libraries:
   ```bash
   python main.py
---
## **👀 Demo: Application in Action**
![App Demo](docs/demo.gif)
---
## **Usage Instructions**

### 1️⃣ **Run the App**
- Launch the GUI by:
  - Running the command: `python main.py` (for development).
  - Or double-clicking the `.exe` file (if using the standalone executable).

### 2️⃣ **Browse for a Simulation File**
- Click the **Browse** button.
- Select an OpenModelica `.exe` simulation file.

### 3️⃣ **Input Start and Stop Times**
- Enter the desired **Start-Time** and **Stop-Time** in the input fields.
- Ensure the times meet the condition: `0 ≤ Start-Time < Stop-Time < 5`.

### 4️⃣ **Run the Simulation**
- Click the **Run** button.
- The app will:
  - Execute the simulation.
  - Display a **Success** or **Error** message based on the outcome.

### 5️⃣ **Plot Graphs**
- Possible only if the SImulation was Successfully Executed.
- Click the variable buttons to generate dynamic plots.
- Analyze the simulation data interactively.
---
## 🛠️ **Build the Executable**

### 1️⃣ **Navigate to the App Directory**
- Make sure you are in the application directory where `main.py` is located:
  ```bash
   cd OpenModelica-Model-Simulation-App/app

### 2️⃣ **Install cx_Freeze**
- Install the `cx_Freeze` library to enable executable creation:
  ```bash
  pip install cx-Freeze

### 3️⃣ **Build the Executable**
- Run the following command to build your `.exe` file:
  ```bash
  python setup.py build

### 4️⃣ **Locate the Executable**
- After the build process completes, the `.exe` file will be located in:
  ```bash
  build/exe.<platform>/

---
## **License**
This project is licensed under the [MIT License](LICENSE).

## **Contact**
- **Developer**: Mohammad Suhail
- **Email**: [mhsuhail00@gmail.com](mailto:mhsuhail00@gmail.com)
- **GitHub Profile**: [mhsuhail00](https://github.com/mhsuhail00)
