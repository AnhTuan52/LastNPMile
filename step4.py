import json

def detect_phantom(repo_hashes, repo_lines, artifact_hashes, artifact_lines, output_json):
    with open(repo_hashes) as f:
        repo_hashes = set(f.read().splitlines())
    with open(repo_lines) as f:
        repo_lines = set(f.read().splitlines())
    with open(artifact_hashes) as f:
        artifact_hashes = set(f.read().splitlines())
    with open(artifact_lines) as f:
        artifact_lines = set(f.read().splitlines())

    phantom_lines = list(artifact_lines - repo_lines)
    phantom_hashes = list(artifact_hashes - repo_hashes)

    # Tính tỉ lệ phần trăm
    total_lines = len(artifact_lines)
    total_files = len(artifact_hashes)
    ratio_lines = (len(phantom_lines) / total_lines * 100) if total_lines > 0 else 0
    ratio_files = (len(phantom_hashes) / total_files * 100) if total_files > 0 else 0

    result = {
        "phantom_lines": len(phantom_lines),
        "phantom_files": len(phantom_hashes),
        "total_lines": total_lines,
        "total_files": total_files,
        "ratio_lines_percent": round(ratio_lines, 2),
        "ratio_files_percent": round(ratio_files, 2),
        "summary": f"Tìm thấy {len(phantom_lines)} phantom lines ({ratio_lines:.2f}%) và {len(phantom_hashes)} phantom files ({ratio_files:.2f}%)."
    }
    with open(output_json, "w") as f:
        json.dump(result, f, indent=4)
    print(result["summary"])

# Chạy cho malicious
detect_phantom("repo_hashes.txt", "repo_lines.txt", "artifact_hashes.txt", "artifact_lines.txt", "malicious_result.json")
