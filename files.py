import os
import sys


def parse_bytes(bytes: int):
    # Parse bytes to human-readable format
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024


def split_file_into_chunks(absolute_path: str):
    # Splits the file into chunks so Telegram can handle it (2GB max)
    chunks = []
    file_size = os.path.getsize(absolute_path)

    # Define root and temp directories
    root_dir = os.path.dirname(sys.argv[0])
    temp_dir = os.path.join(root_dir, "temp")

    # Ensure the `temp` directory exists
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    if file_size > 2 * 1024 * 1024 * 1024:  # 2GB max file size for Telegram
        # Split the file into chunks
        with open(absolute_path, "rb") as file:
            print(f"Splitting {absolute_path} into chunks...")
            chunk_num = 0
            while True:
                chunk = file.read(50 * 1024 * 1024)  # 50MB per chunk
                if not chunk:
                    break

                chunk_file_path = os.path.join(temp_dir, f"{os.path.basename(absolute_path)}-{chunk_num}.chunk")
                print(f"Writing chunk to {chunk_file_path}...")

                with open(chunk_file_path, "wb") as chunk_file:
                    chunk_file.write(chunk)

                chunks.append(chunk_file_path)
                chunk_num += 1

        return chunks
    else:
        # No need to split the file if it's under 2GB
        chunk_file_path = os.path.join(temp_dir, f"{os.path.basename(absolute_path)}.chunk")

        with open(absolute_path, "rb") as file:
            chunk_data = file.read()
            with open(chunk_file_path, "wb") as chunk_file:
                chunk_file.write(chunk_data)

        chunks.append(chunk_file_path)

        return chunks
