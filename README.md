# VISITOR-MANAGEMENT-SYSTEM

functionalities and technologies:

Raspberry Pi: The code is specifically written to run on a Raspberry Pi device, utilizing the RPi.GPIO library for GPIO (General Purpose Input/Output) operations.

Email Integration: The code includes functionality to send an email notification when an unknown visitor is detected. It utilizes the email, ssl, and smtplib libraries to compose and send the email with an attached image.

Web Interface: The code sets up a simple web interface that can be accessed to control an LED. It listens for HTTP requests on a specific port, and when a request is received with the parameter led=on, it turns on the LED.

Socket Programming: The code uses socket programming to listen for connections and serve the web interface to the client. It creates a socket, binds it to a specific address and port, and listens for incoming connections.
