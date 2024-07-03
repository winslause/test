# test
Algorthmic science test

Installation Instructions
Place the script files in a directory.
Create and edit config.ini with the correct paths and options.
Install required packages:
bash
.......

pip install pytest

Start the server:
bash
.......

python server_script.py
Running the Server as a Service

[Install]
WantedBy=multi-user.target
Place the service file in /etc/systemd/system/ and name it string_search_server.service.
Reload the systemd manager configuration:
bash
.......
sudo systemctl daemon-reload
Start the service:
bash
.......
sudo systemctl start string_search_server
Enable the service to start on boot:
bash
.......
sudo systemctl enable string_search_server
