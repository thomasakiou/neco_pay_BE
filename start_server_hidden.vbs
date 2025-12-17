Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "C:\apps\neco_payment_manager\neco-payment-manager-BE\start_server.bat", 0, False
Set WshShell = Nothing
