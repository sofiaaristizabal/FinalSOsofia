mkdir fastapi
cd fastapi
git clone https://github.com/sofiaaristizabal/FinalSOsofia.git .
cd punto2

sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip -y
sudo apt install python3.12-venv

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo cp fastapi.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start fastapi
sudo systemctl enable fastapi