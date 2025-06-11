# **Pepi AI Chat - Setup Guide**

This project is a chatbot-powered web application that integrates **Ollama** for text-based AI responses and **Stable Diffusion** for image generation.

---

NOTE
python 3.10 is required no higear version works 

## **1. Prerequisites**
Ensure you have the following installed:
- **Python 3.10** ([Download Here](https://www.python.org/downloads/))
- **Git** ([Download Here](https://git-scm.com/downloads))
- **Ollama** (for text AI)
- **Stable Diffusion WebUI (AUTOMATIC1111)** (for image generation)

---

## **2. Installing Ollama**
Ollama is a local LLM model runner. To install:

### **Windows & Mac**
1. Download Ollama from the official site: [https://ollama.com](https://ollama.com)
2. Install the package and follow the setup instructions.
3. Open a terminal and run:
   ```sh
   ollama pull wizardlm2:7b
   ```
   This downloads the **WizardLM-2 7B** model required for chatbot responses.
4. To start Ollama as a service:
   ```sh
   ollama serve
   ```

### **Linux (Ubuntu/Debian)**
1. Open a terminal and run:
   ```sh
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. Pull the required AI model:
   ```sh
   ollama pull wizardlm2:7b
   ```
3. Start Ollama:
   ```sh
   ollama serve
   ```
4. ## Troubleshooting
  ### Error: "Only one usage of each socket address (protocol/network address/port) is normally permitted."
  If you see this error when running `ollama serve`:
  
  Error: listen tcp 127.0.0.1:11434: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.
  
  It means that port `11434` is already in use on your system, likely by another running instance of Ollama or another process.

#### ✅ Solution

1. **Check which process is using the port** (Windows PowerShell):

```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 11434).OwningProcess
Stop the process using the port:
```

```powershell
Stop-Process -Id (Get-NetTCPConnection -LocalPort 11434).OwningProcess -Force
Restart the server:
```

```bash
ollama serve
Alternatively, run Ollama on a different port:
```

```bash
ollama serve --port 11500
Then access it at: http://127.0.0.1:11500
```

## **3. Installing Stable Diffusion WebUI (AUTOMATIC1111)**
Stable Diffusion is required for image generation.

### **Windows**
1. Download **Stable Diffusion WebUI** from [GitHub](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
2. Extract the folder and open a terminal inside the directory.
cd stable-diffusion-webui
3. Run the following command to install dependencies:
   ```sh
   webui-user.bat
   ```
4. Once loaded, it will start a local server at `http://127.0.0.1:7860`.

### **Linux & Mac**
1. Open a terminal and clone the repository:
   ```sh
   git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
   cd stable-diffusion-webui
   ```
2. Install dependencies:
   ```sh
   bash webui.sh
   ```
3. Run Stable Diffusion:
   ```sh
   python launch.py --api
   ```

---

## **4. Setting Up the Flask App**

### **Step 1: Clone the Repository**
```sh
git clone https://github.com/your-repo/pepi-ai-chat.git
cd Pepi-AI-Chat
```

### **Step 2: Create and Activate a Virtual Environment**
```sh
python -m venv venv
```
- **Windows:**
  ```sh
  venv\Scripts\activate
  ```
- **Linux/Mac:**
  ```sh
  source venv/bin/activate
  ```

### **Step 3: Install Dependencies**
```sh
pip install -r requirements.txt
```

### **Step 4: Run the Flask App**
Ensure **Ollama** and **Stable Diffusion** are running, then start the Flask server:
```sh
python app.py
```
The app will be available at `http://127.0.0.1:5000`.

---

## **5. How to Use**
- **Chat with Ollama**: Type messages in the chat, and Ollama will respond.
- **Generate an Image**: Type `generate an image of a cat`, and Stable Diffusion will create an image.
- **View Images**: Generated images will be saved in `static/images/generated/` and displayed in the chat.

---

## **6. Troubleshooting**
- **Ollama not responding?** Ensure it is running using `ollama serve`.
- **Stable Diffusion not generating images?** Ensure it's running at `http://127.0.0.1:7860`.
- **App not loading?** Try restarting Flask using `python app.py`.
"try py if python not works"

---

## **7. Future Enhancements**
- Add **Undo/Redo** for image edits
- Implement **voice chat support**
- Improve **user interface and animations**

---

### **Author**
Virendar Oza 🚀

