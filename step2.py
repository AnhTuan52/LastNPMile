import os
import git
import hashlib
import logging
from tqdm import tqdm

# ================== CẤU HÌNH ==================

# Đường dẫn tới repo cần quét
REPO_PATH = "/home/kali/Desktop/LastNPMile/malicious_repo/"   # 👉 chỉnh lại cho đúng, vd: "/home/tuan/Desktop/malicious_repo"

# Các loại file text quan tâm
TEXT_EXTENSIONS = {
    ".js", ".jsx",
    ".ts", ".tsx",
    ".json",
    ".md", ".txt",
    ".yml", ".yaml",
    ".c", ".h", ".cpp", ".cc"
}

# Bật logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ================== HÀM XỬ LÝ 1 COMMIT ==================

def process_commit(commit):
    """
    Xử lý 1 commit:
    - Duyệt toàn bộ file (blob) trong commit
    - Nếu file là text -> đọc nội dung, tính SHA-256, gom hash + các dòng
    """
    local_hashes = set()
    local_lines = set()

    try:
        for blob in commit.tree.traverse():
            if blob.type != "blob":
                continue

            ext = os.path.splitext(blob.name)[1].lower()
            if ext not in TEXT_EXTENSIONS:
                continue

            try:
                raw = blob.data_stream.read()
                if isinstance(raw, bytes):
                    content = raw.decode(errors="ignore")
                else:
                    content = str(raw)

                # Hash nội dung file
                file_hash = hashlib.sha256(
                    content.encode("utf-8", errors="ignore")
                ).hexdigest()
                local_hashes.add(file_hash)

                # Gom các dòng
                for line in content.splitlines():
                    line = line.rstrip("\r\n")
                    if line:  
                        local_lines.add(line)

            except Exception as e:
                logging.warning(
                    f"Lỗi xử lý blob '{blob.path}' ở commit {commit.hexsha[:8]}: {e}"
                )

        logging.info(
            f"Hoàn thành commit {commit.hexsha[:8]}: {len(local_hashes)} hash, {len(local_lines)} dòng"
        )

    except Exception as e:
        logging.error(f"Lỗi duyệt commit {commit.hexsha[:8]}: {e}")

    return local_hashes, local_lines

# ================== MAIN ==================

def main():
    if not os.path.isdir(REPO_PATH):
        logging.error(f"Không tìm thấy thư mục repo: {REPO_PATH}")
        return

    logging.info(f"Đang mở repo ở: {REPO_PATH}")
    repo = git.Repo(REPO_PATH)

    # 🔹 LẤY TẤT CẢ COMMITS TRÊN MỌI BRANCH
    commits = list(repo.iter_commits("master"))

    if not commits:
        logging.error("Không tìm thấy commit nào trong repo (có thể repo trống?).")
        return

    logging.info(f"Tổng số commit cần xử lý (FULL lịch sử): {len(commits)}")

    all_hashes = set()
    all_lines = set()

    # Quét tuần tự từng commit, có tqdm để xem tiến trình
    for commit in tqdm(commits, desc="Xử lý commits"):
        h_set, l_set = process_commit(commit)
        all_hashes.update(h_set)
        all_lines.update(l_set)

    # Ghi ra file
    hashes_file = "repo_hashes.txt"
    lines_file = "repo_lines.txt"

    with open(hashes_file, "w", encoding="utf-8") as f:
        for h in sorted(all_hashes):
            f.write(h + "\n")

    with open(lines_file, "w", encoding="utf-8") as f:
        for line in sorted(all_lines):
            f.write(line + "\n")

    logging.info(f"Thu thập {len(all_hashes)} hash và {len(all_lines)} dòng từ repo.")
    logging.info(f"Đã ghi kết quả ra: {hashes_file}, {lines_file}")

if __name__ == "__main__":
    main()
