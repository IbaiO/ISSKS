import zipfile
import hashlib
import os
import subprocess
import shutil
import pexpect

# Step 1: Check if steghide is installed, and install it if not
def install_steghide():
    if shutil.which("steghide") is None:
        print("steghide not found. Installing...")
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "steghide"], check=True)
    else:
        print("steghide is already installed.")

install_steghide()

# Step 2: Unzip the file
zip_path = '/home/ibaio/Downloads/imagen.zip'
extract_path = '/home/ibaio/Downloads/imagen_extracted'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Step 3: Calculate the MD5 hash of each image
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Step 4: Identify the image with the matching MD5 hash
target_md5 = 'e5ed313192776744b9b93b1320b5e268'
target_image = None

for root, dirs, files in os.walk(extract_path):
    for file in files:
        file_path = os.path.join(root, file)
        if calculate_md5(file_path) == target_md5:
            target_image = file_path
            break

if target_image:
    print(f"Target image found: {target_image}")
else:
    print("Target image not found.")
    exit()

# Step 5: Extract the hidden message using steghide with pexpect
output_path = '/home/ibaio/Downloads/secret_message.txt'
command = f"steghide extract -sf {target_image} -xf {output_path}"

child = pexpect.spawn(command)
child.expect("Enter passphrase:")
child.sendline("")  # Send an empty passphrase
child.expect(pexpect.EOF)

# Debugging information
print("Command output:", child.before.decode())
print("Command error:", child.before.decode())

# Check if the command was successful
if not os.path.exists(output_path):
    print("steghide command failed.")
    exit()

# Read and print the extracted message
try:
    with open(output_path, 'r') as f:
        secret_message = f.read()
        if secret_message:
            print("Secret message:", secret_message)
        else:
            print("No secret message found.")
except FileNotFoundError:
    print(f"Output file {output_path} not found.")