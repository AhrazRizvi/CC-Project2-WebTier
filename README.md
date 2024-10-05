# CC-Project2-WebTier
## CSE 546 Cloud Computing

This repository outlines the steps and key notes for developing and deploying a basic FastAPI application on an EC2 instance.

### Step 1: Creating a FastAPI Application
FastAPI works with Python versions 3.8 and above. To run the application, you can use Uvicorn with the following command:
```
uvicorn {server_filename}:app --host 0.0.0.0 --port 8000 --reload --workers=k
```
- `--host` (optional): Binds the server to the machine's IP (important for EC2).
- `--port`: Specifies the port for the application.
- `--reload` (optional): Useful in development to auto-restart on changes.
- `--workers` (optional): Allows specifying multiple workers for concurrency.

### Step 2: Testing with FastAPI Docs
You can test the APIs you’ve created via the FastAPI documentation interface at: `https://url:port/docs`.

### Step 3: Testing with Workload Generator
The Workload Generator mimics client-side requests and tests the API’s responsiveness and correctness. Run the following command to test it:
```
python ./Resources/workload_generator/workload_generator.py --num_request 100 --url http://127.0.0.1:8000/ --image_folder "./Resources/dataset/face_images_1000/" --prediction_file "./Resources/dataset/Classification Results on Face Dataset (1000 images).csv"
```

### Creating EC2 Instance
You can automatically create an EC2 instance using the provided `createEC2.py` script.

### Setting up the Project in EC2
To set up the project on an EC2 instance, you need to update the existing packages, pull the project from GitHub, create a virtual environment, and install the required dependencies:
```
sudo apt-get update -y
sudo apt install python3.10-venv -y
python3 -m venv project2env
source project2env/bin/activate
git clone -q https://github.com/husainasad/Cloud-Computing.git
pip install --upgrade pip
pip install --upgrade setuptools
pip install "fastapi[all]"
pip install pandas python-multipart
```

### Running Server After Reboot
To ensure that the FastAPI server runs automatically even after the EC2 instance reboots, add the server start command to the boot files:
```
echo "[Unit]
Description=My Uvicorn server
After=multi-user.target
StartLimitIntervalSec=0

[Service]
Type=simple
ExecStart=/home/ubuntu/project2env/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8000
WorkingDirectory=/home/ubuntu/Cloud-Computing
User=ubuntu
Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/uvicorn-server.service
```

### Enabling the Script
Once the script is created, apply the following commands to ensure it runs on boot:
```
sudo chmod 644 /etc/systemd/system/uvicorn-server.service
sudo systemctl start uvicorn-server
sudo systemctl enable uvicorn-server
```

### Application Deployment
The `createEC2.py` script automates the creation of the EC2 instance and starts the server. The server will automatically restart after any reboot, eliminating the need for manual intervention.
You can verify the server functionality either through the FastAPI docs or by using the Workload Generator from another machine.
