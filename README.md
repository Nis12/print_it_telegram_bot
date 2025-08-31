# PrintIt telegram bot


This is a Telegram bot that receives files from registered users and prints them on a printer. 
Registration in the chat with the approval of the administrator.

Get a token for your bot from Telegram @BotFather. Insert it into the _TOKEN variable in file src/main.py

Find out your telegram account ID. Insert it into the field _admin_id_key: 1234567890 in src/config.py, 
(1234567890 - as example).

ALLOWED_FORMATS = ['.pdf', '.docx', '.doc', '.rtf', '.txt', '.odt']

Send the file to the chat and click on the print button. The bot will convert the file to pdf and start printing. 
If you are not an administrator, you will need to register before printing. In the chat, click on registration. The bot will send
a message to the administrator requesting user registration.

## Install:

### Before
 ```sh
   sudo apt update
 ```

Install requirements
 ```sh
   pip freeze > requirements.txt
 ```

### libreoffice
  ```sh
    sudo apt install libreoffice --no-install-recommends
    libreoffice --version
  ```

### cups
  ```sh
    sudo apt install cups cups-client lpr
    sudo usermod -a -G lp orangepi
    sudo reboot
  ```

After reboot

  ```sh
    which lpr
    lpr --version
  ```

### Look to available printers
  ```sh
    lpstat -p
  ```

If you don't see any of them, configure them. It's straightforward, but it can be specific. 
Find a way to configure your printer for cups on the web.

### Test print
  ```sh
    echo "Test print" > test.txt
    lp test.txt
  ```

