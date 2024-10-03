
# Home Control Project

This project controls lights using a Django app deployed on Heroku and an ESP32 device acting as a server. Below are the steps for setting up the project locally, deploying it to Heroku, and configuring the ESP32 device using **VSCode with PlatformIO**.

---

## 1. Setting Up Django Locally

### Prerequisites:
- Python 3.x
- Git
- Virtualenv (optional but recommended)
- PostgreSQL (optional, if not using SQLite)

### Step-by-Step:

1. **Clone the repository**:
   open vscode and open terminal inside of your vscode
   then in terminal got o your needed place and add this command :
   ```bash
   git clone https://github.com/devbmv/home-control.git
   cd home-control
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the `env.py` file** in the project root directory:
   - In the root folder of the project, create a file named `env.py`.
   - Add the following environment variables:
     ```python
     import os

     os.environ["SECRET_KEY"] = "your_secret_key"
     os.environ["DEBUG"] = "True"  # Set to "False" in production
     os.environ["DATABASE_URL"] = "your_postgresql_database_url"
     os.environ["CLOUDINARY_URL"] = "your_cloudinary_url"
     os.environ["DJANGO_API_USERNAME"] = "your_api_username"
     os.environ["DJANGO_API_PASSWORD"] = "your_api_password"
     ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the site locally**: 
   Go to `http://127.0.0.1:8000` in your browser.

---

## 2. Deploying to Heroku

### Prerequisites:
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- GitHub account
- Heroku account

### Step-by-Step:

1. **Log in to Heroku**:
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**:
   ```bash
   heroku create home-control
   ```

3. **Set up environment variables on Heroku**:
   ```bash
   heroku config:set SECRET_KEY=your_secret_key DEBUG=False CLOUDINARY_URL=your_cloudinary_url DJANGO_API_USERNAME=your_api_username DJANGO_API_PASSWORD=your_api_password
   ```

4. **Add Heroku PostgreSQL**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

5. **Disable `collectstatic` if needed**:
   ```bash
   heroku config:set DISABLE_COLLECTSTATIC=1
   ```

6. **Push your code to Heroku**:
   ```bash
   git push heroku main
   ```

7. **Run migrations on Heroku**:
   ```bash
   heroku run python manage.py migrate
   ```

8. **Create a superuser on Heroku**:
   ```bash
   heroku run python manage.py createsuperuser
   ```

9. **Open the Heroku app**:
   ```bash
   heroku open
   ```

---

## 3. Setting Up the ESP32 Server Using VSCode + PlatformIO

### Prerequisites:
- Visual Studio Code
- PlatformIO extension for VSCode
- ESP32 board
- Access to Wi-Fi
- USB cable for uploading the code to ESP32

### Step-by-Step:

1. **Open the ESP32 project in VSCode with PlatformIO**:
   - Navigate to the folder containing the ESP32 code in the PlatformIO project structure.
   - Open the project in **VSCode**.

2. **Modify the platformio.ini file**:
   - In the project directory, open the `platformio.ini` file and configure the upload settings for ESP32, including the serial port for uploading the code:
     ```ini
     [env:esp32]
     platform = espressif32
     board = esp32dev
     framework = arduino
     monitor_speed = 115200
     upload_port = /dev/ttyUSB0  # Adjust for your system
     ```

3. **Update Wi-Fi credentials and Django server details in the ESP32 code**:
   - Modify the following variables in the ESP32 code:
     ```cpp
     String ssid = "your_wifi_ssid";
     String password = "your_wifi_password";
     String djangoUserName = "your_django_api_username";
     String djangoPassword = "your_django_api_password";
     ```

4. **Build and upload the code to the ESP32** using PlatformIO:
   - In VSCode, open the PlatformIO sidebar and click on **Build** to compile the code.
   - After a successful build, click on **Upload** to send the code to the ESP32 via USB.

5. **Monitor the Serial Console**:
   - Use the PlatformIO Serial Monitor to check for the ESP32's IP address and logs.

---

## 4. Setting Up Dynamic DNS Using NO-IP

To access your ESP32 device remotely, you will need to set up a Dynamic DNS service. Here’s how to do it using **NO-IP**:

### Step-by-Step:

1. **Create an account on NO-IP**:
   - Visit [NO-IP](https://www.noip.com/) and sign up for a free account.

2. **Create a Hostname**:
   - After logging in, go to the **Dynamic DNS** section and create a new hostname.
   - Choose a free domain and assign your current public IP address.


3. **Configure NO-IP on your router**:
   - Log in to your router's settings.
   - Find the **Dynamic DNS** section and enter your NO-IP credentials and hostname.
   - This ensures that your public IP is always updated.

4. **Add the NO-IP domain to Django**:
   - Modify your `ALLOWED_HOSTS` in Django’s `settings.py` to include your NO-IP domain:
     ```python
     ALLOWED_HOSTS = [
         "your-noip-domain.ddns.net",
         "127.0.0.1",
         "localhost",
     ]
     ```

5. **Port Forwarding**:
   - Forward port 80 (or the port ESP32 is using) to your ESP32’s local IP address.
   - Test the setup by accessing your ESP32 using the NO-IP domain.

---

## 6. Setting Up Environment Variables for ESP32 Project

You need to set environment variables on your system for Wi-Fi and Django credentials, as they are used during the build process in PlatformIO.

### For **Windows**:

1. **Open Command Prompt** as Administrator.
2. Set the environment variables using the following commands:
   ```bash
   setx WIFI_SSID "your_wifi_ssid"
   setx WIFI_PASSWORD "your_wifi_password"
   setx DJANGO_API_USERNAME "your_django_api_username"
   setx DJANGO_API_PASSWORD "your_django_api_password"
   ```

### For **Linux**:

1. **Open the terminal**.
2. Add the environment variables to your `~/.bashrc` or `~/.zshrc`:
   ```bash
   export WIFI_SSID="your_wifi_ssid"
   export WIFI_PASSWORD="your_wifi_password"
   export DJANGO_API_USERNAME="your_django_api_username"
   export DJANGO_API_PASSWORD="your_django_api_password"
   ```
3. **Reload the shell configuration**:
   ```bash
   source ~/.bashrc  # Or ~/.zshrc depending on your shell
   ```

---

## 6. Troubleshooting Tips

- **Debugging Django locally**:
   - Set `DEBUG=True` in `env.py` to see detailed error messages.
   - Use `python manage.py runserver --settings=home_control_project.settings.local` for local settings.

- **ESP32 connectivity issues**:
   - Check Wi-Fi credentials in the ESP32 code.
   - Verify the Django server is reachable from the ESP32 (use the Serial Monitor for diagnostics).

---

## 7. Future Automation Implementations

Once the light control functionality is working, you can expand to other automations (such as temperature control or motion detection). You’ll follow a similar process, modifying the `Light` model or add new models and creating new devices that interact with your ESP32 server.

---
