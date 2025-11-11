OmSaiMurugan Finance - Local Dev UI

What I changed:
- Updated UI title to "OmSaiMurugan Finance"
- Template will use a background image if you place it at `static/bg.jpg`.
- The background image URL includes a cache-busting `v` query param so changes show immediately.

How to use:
1. Place your background image in the project `static` folder and name it `bg.jpg`:
   - `c:\Users\Admin\OneDrive\Desktop\OMSAIMURUGAN\static\bg.jpg`

2. (Optional) Restart the Flask server. The template already includes a cache-buster, so you may only need a hard refresh on the phone (Ctrl/Cmd+Shift+R or long-press refresh on mobile)

3. Open the app from any device on the same Wi-Fi using:
   http://<PC_LAN_IP>:5000
   Example from your network earlier: http://172.16.177.116:5000

If your phone can't connect:
- Ensure phone is on the same Wi-Fi network.
- Allow the Python executable through Windows Firewall (or open port 5000). Example (PowerShell as Admin):
  New-NetFirewallRule -DisplayName "Allow Python for Flask" -Direction Inbound -Program "C:\Users\Admin\OneDrive\Desktop\OMSAIMURUGAN\.venv\Scripts\python.exe" -Action Allow -Profile Private

- To remove the rule later:
  Remove-NetFirewallRule -DisplayName "Allow Python for Flask"

Still seeing old UI?
- Clear the browser cache or hard refresh the page.
- The template now sends `bg_version` so image caching is handled; the HTML itself may be cached by the browser — hard refresh fixes that.

If you want, I can create the firewall rule for you if you confirm you can run an Administrator PowerShell command.
