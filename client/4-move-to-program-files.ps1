# Source folder
$sourceFolder = "./flamonitor-v0.1.0-dist" # Replace with the actual path to your source folder

# Destination folder
$destinationFolder = "C:\Program Files\"

# Create the destination directory if it doesn't exist
if (!(Test-Path -Path $destinationFolder)) {
  New-Item -ItemType Directory -Path $destinationFolder | Out-Null
}

try {
  Copy-Item -Path $sourceFolder -Destination $destinationFolder -Recurse -Force -ErrorAction Stop
  Write-Host "Files copied successfully to $destinationFolder"
}
catch {
  Write-Error "Error copying files: $_"
  return # Exit the script if copying fails
}
