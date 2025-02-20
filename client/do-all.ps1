& .\1-install-choco.ps1
& .\2-install-python-3.11-from-choco.ps1
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
& .\3-install-pip-requirements.ps1
& .\4-move-to-program-files.ps1
& .\5-register-flamonitor-task.ps1
