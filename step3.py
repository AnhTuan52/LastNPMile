import hashlib
import os

extract_dir = "/home/kali/Desktop/DEMO/benign_extract/package/"  # Thay <id> bằng ID thực từ unzip (e.g., tmpex51nra1)
output_hashes = "artifact_hashes.txt"
output_lines = "artifact_lines.txt"

artifact_hashes = set()
artifact_lines = set()
for root, _, files in os.walk(extract_dir):
    for file in files:
        path = os.path.join(root, file)
        with open(path, "r", errors="ignore") as f:
            content = f.read()
            file_hash = hashlib.sha256(content.encode()).hexdigest()
            artifact_hashes.add(file_hash)
            lines = content.splitlines()
            artifact_lines.update(lines)

with open(output_hashes, "w") as f:
    f.write("\n".join(artifact_hashes))
with open(output_lines, "w") as f:
    f.write("\n".join(artifact_lines))
print(f"Thu thập {len(artifact_hashes)} hashes và {len(artifact_lines)} lines từ artifact.")
