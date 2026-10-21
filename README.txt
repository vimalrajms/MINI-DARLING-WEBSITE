MINI DARLING WEBSITE
====================

Files
-----
- index.html: complete responsive pink DARLING message-sender website.

What it does
------------
- Shows a cute girl placeholder and the DARLING name.
- Lets you type and send a message.
- Does not show Darling's reply on the website; the reply is intended for the OLED.
- Sends POST /message with JSON: {"message":"your text"}.

Important
---------
This website is the frontend only. The ESP32 firmware still needs to:
1. Create its Wi-Fi access point.
2. Serve this index.html.
3. Implement POST /message.
4. Read the message, choose a programmed reply, and show that reply on the OLED.

For the intended ESP32 setup, connect your phone/laptop to the ESP32 Wi-Fi and open
the local address served by the ESP32 (commonly http://192.168.4.1).

If you double-click index.html from your computer, the message request will not reach
the ESP32 because the page is not being served by the ESP32. The ESP32 firmware/API
is the next integration step. This project does not require a cloud AI API.
