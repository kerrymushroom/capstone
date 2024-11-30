import os
import subprocess
import time


################
# Start a local server "localhost:8000" to get a fixed URL address for csv files.
# Because NL4DV3.0 need a URL to record file address.
################


# Used for the internal call of the current file. Start local server
def _start_local_server():
    if not os.path.exists('uploaded_files'):
        os.makedirs('uploaded_files')

    server_command = ['python3', '-m', 'http.server', '8000', '--directory', 'uploaded_files']
    server_process = subprocess.Popen(server_command)
    time.sleep(2)  # 给服务器一点时间来启动
    return server_process


# Stop local server
def stop_server(server_process):
    server_process.terminate()
    server_process.wait()


# Start local server
def start_server():
    try:
        server_process = _start_local_server()
        print('Server started at 8000')
    except Exception as e:
        print(f"Error in server start: {e}")


# Copy file to the server
def local_file_upload(local_file, mode):
    if mode == 'upload':
        file_path = os.path.join("uploaded_files", local_file.name)
        with open(file_path, "wb") as f:
            f.write(local_file.getbuffer())
    else:
        if os.path.exists(local_file):
            file_name = os.path.basename(local_file)
            destination_path = os.path.join('uploaded_files', file_name)
        with open(local_file, "rb") as src_file:
            with open(destination_path, "wb") as dest_file:
                dest_file.write(src_file.read())
