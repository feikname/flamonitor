$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
python.exe -m pip install --upgrade pip
python.exe -m pip install -r flamonitor-v0.1.0-dist/requirements.txt
