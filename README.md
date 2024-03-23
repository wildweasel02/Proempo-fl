# Proempo-fl Instructions
1. Download and install python on your computer
2. Run install_dep included in the source code or run 'pip install -r requirements.txt' in the terminal
3. Run app.py
4. Follow onscreen instructions to access website hosted from your local computer


If getting the error "ModuleNotFoundError: No module named 'flask' " despite having flask, you have to create a virtual environment by:
1. Navigate to View > Command Palette
2. Select Python: Create Envrionment
3. Create a .venv virtual environment
4. Select an interpreter (app is optimized for python 3.12) and select the requirements.txt file
This will fix it and app.py will run successfully. A development server will open and you will be prompted with an address to view the web app
