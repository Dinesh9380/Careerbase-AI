$WshShell = New-Object -ComObject WScript.Shell

$s1 = $WshShell.CreateShortcut("C:\Users\rohit\OneDrive\Desktop\Open Career Platform in VS Code.lnk")
$s1.TargetPath = "code"
$s1.Arguments = """C:\Users\rohit\career-intelligence-platform"""
$s1.WorkingDirectory = "C:\Users\rohit\career-intelligence-platform"
$s1.Description = "Open AI Career Intelligence Platform in VS Code"
$s1.Save()

$s2 = $WshShell.CreateShortcut("C:\Users\rohit\OneDrive\Desktop\Career Intelligence Platform Folder.lnk")
$s2.TargetPath = "explorer.exe"
$s2.Arguments = """C:\Users\rohit\career-intelligence-platform"""
$s2.Description = "Open Career Intelligence Platform Folder in File Explorer"
$s2.Save()

Write-Host "Desktop shortcuts successfully updated!"
