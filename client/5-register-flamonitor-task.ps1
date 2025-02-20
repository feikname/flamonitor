$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c run.bat" -WorkingDirectory "C:\Program Files\flamonitor-v0.1.0-dist"
$Trigger = New-ScheduledTaskTrigger -AtStartup
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Principal $Principal -Description "Runs flamonitor every 5 minutes after startup"

Register-ScheduledTask -TaskName "flamonitor v0.1.0" -InputObject $Task

#https://superuser.com/questions/1373275/how-to-schedule-a-task-with-powershell-to-run-every-hour-monday-to-friday-betwe
# $Task = Get-ScheduledTask -TaskName "flamonitor v0.1.0"
# $Task.Triggers.Repetition.Interval = "PT5M"
# $Task.Triggers.Repetition.Duration = ""
# $Task | Set-ScheduledTask -User "NT AUTHORITY\SYSTEM"
