# Auto-Start FastAPI Application on Windows Boot

This guide provides multiple methods to automatically start your FastAPI application when Windows starts.

## Method 1: Windows Task Scheduler (Recommended)

### Steps:

1. **Press `Win + R`**, type `taskschd.msc`, and press Enter to open Task Scheduler

2. **Click "Create Basic Task"** in the right panel

3. **Name your task**: e.g., "NECO Payment Manager Backend"

4. **Trigger**: Select "When the computer starts"

5. **Action**: Select "Start a program"

6. **Program/script**: Browse to `G:\Projects\neco-payment-manager-BE\start_server.bat`

7. **Click Finish**

8. **Additional Configuration** (Important):
   - Right-click the task you just created → Properties
   - Under "General" tab:
     - Check "Run whether user is logged on or not"
     - Check "Run with highest privileges"
   - Under "Conditions" tab:
     - Uncheck "Start the task only if the computer is on AC power" (if laptop)
   - Under "Settings" tab:
     - Check "Allow task to be run on demand"
     - Uncheck "Stop the task if it runs longer than"
   - Click OK

### Advantages:
✅ Most reliable method
✅ Runs even before login
✅ Easy to enable/disable
✅ Can view logs and status

---

## Method 2: Windows Startup Folder (Simpler)

### Steps:

1. **Press `Win + R`**, type `shell:startup`, and press Enter

2. **Create a shortcut** to `start_server.bat`:
   - Right-click in the Startup folder
   - New → Shortcut
   - Browse to: `G:\Projects\neco-payment-manager-BE\start_server.bat`
   - Click Next → Finish

### Advantages:
✅ Very simple to set up
✅ Easy to remove (just delete shortcut)

### Disadvantages:
❌ Only runs after user login
❌ Terminal window will be visible

---

## Method 3: Windows Service (Advanced)

For production environments, you can install the application as a Windows Service using **NSSM (Non-Sucking Service Manager)**.

### Steps:

1. **Download NSSM**: https://nssm.cc/download

2. **Extract NSSM** and open PowerShell as Administrator

3. **Navigate to NSSM directory** and run:
   ```powershell
   .\nssm.exe install NECOPaymentManager
   ```

4. **Configure the service**:
   - Path: `C:\Path\To\Python\python.exe` (your Python executable)
   - Startup directory: `G:\Projects\neco-payment-manager-BE`
   - Arguments: `-m uvicorn app.main:app --host 0.0.0.0 --port 8000`

5. **Start the service**:
   ```powershell
   nssm start NECOPaymentManager
   ```

### Advantages:
✅ Runs as a true Windows service
✅ Automatic restart on failure
✅ No visible terminal window
✅ Runs before user login

### Disadvantages:
❌ More complex setup
❌ Requires additional software (NSSM)

---

## Method 4: Production Batch Script with Hidden Window

Create an enhanced batch script that runs minimized:

**File: `start_server_hidden.vbs`**
```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "G:\Projects\neco-payment-manager-BE\start_server.bat", 0, False
Set WshShell = Nothing
```

Then add this `.vbs` file to the Startup folder instead of the `.bat` file.

### Advantages:
✅ No visible terminal window
✅ Simple to implement

---

## Recommended Approach

For **development**: Use **Method 2** (Startup Folder) - simple and easy to disable

For **production**: Use **Method 3** (Windows Service) - most robust and professional

---

## Important Notes

⚠️ **For production use**, you should:
- Remove the `--reload` flag from uvicorn (it's for development only)
- Use `--host 0.0.0.0` to allow external connections
- Consider using `--workers 4` for better performance
- Set up proper logging

**Production command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Testing Your Setup

1. **Restart your computer**
2. **Check if the application is running**:
   - Open browser and go to `http://localhost:8000/docs`
   - Or check Task Manager for the Python process

---

## Troubleshooting

**Application not starting?**
- Check if Python is in your system PATH
- Verify the paths in the batch script are correct
- Check Task Scheduler logs (if using Method 1)
- Ensure no other application is using port 8000

**Want to stop auto-start?**
- Method 1: Disable the task in Task Scheduler
- Method 2: Delete the shortcut from Startup folder
- Method 3: Run `nssm stop NECOPaymentManager` and `nssm remove NECOPaymentManager`
