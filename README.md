Giới Thiệu
Dự án này là bản demo thực hành công cụ LastNPMile (hay LastJSMile trong paper) dựa trên nghiên cứu "On the feasibility of detecting injections in malicious npm packages" (ARES 2022, tác giả Simone Scalco et al.).
Mục tiêu: Phát hiện mã độc được chèn vào gói npm trong giai đoạn "last mile" (từ source code trên GitHub đến artifact publish trên npm registry). Phương pháp so sánh sự khác biệt (discrepancies) giữa artifact và repo nguồn để tìm "phantom" (file/dòng mã lạ không tồn tại trong lịch sử repo).
Điểm nổi bật từ paper:

Giảm false positives (FP) 69% so với scanner truyền thống.
Nhanh hơn 20.7x so với git-log.
Test trên malicious (phantom cao) và benign (phantom thấp/0).

Gói test trong demo:

Malicious: custom-tg-bot-plan@1.0.1 (từ dataset DataDog, chèn postinstall tải malware Vidar).
Benign: chalk@5.0.1 (gói sạch, popular, phantom thấp).

Yêu Cầu

Kali Linux (hoặc Linux có Python 3).
Python 3.12+.
Thư viện: gitpython, tqdm, hashlib, multiprocessing.
npm (để tải gói benign).

Bước 1: Chuẩn Bị Artifact Và Repo Nguồn
  Malicious (custom-tg-bot-plan@1.0.1):

      Clone dataset DataDog:textgit clone https://github.com/DataDog/malicious-software-packages-dataset.git
      cd malicious-software-packages-dataset
      find samples/npm -name "*custom-tg-bot-plan*.zip"
      cd ~/Desktop/LastNPMile
      mkdir -p temp
      unzip -o -P infected "<đường_dẫn_ZIP_tìm_được>" -d temp/
      Clone repo nguồn (giả mạo):textgit clone https://github.com/yagop/node-telegram-bot-api.git malicious_repo

  Benign (chalk@5.0.1):

      Tải artifact:textnpm pack chalk@5.0.1
      mkdir benign_extract
      tar -xzf chalk-5.0.1.tgz -C benign_extract/
      Clone repo nguồn:textgit clone https://github.com/chalk/chalk.git benign_repo
Bước 2: Thu Thập Hash Và Dòng Mã Từ Repo (step2.py)

  Code step2.py (của bạn, với logging/tqdm).
  Chỉnh REPO_PATH cho malicious_repo hoặc benign_repo.
  Chạy cho malicious:textpython3 step2.py  # Tạo repo_hashes.txt, repo_lines.txt
  Cho benign: Sao chép thành step2_benign.py, chỉnh REPO_PATH = "benign_repo/", commits = "main", chạy python3 step2_benign.py (tạo benign_repo_hashes.txt, benign_repo_lines.txt).

Bước 3: Thu Thập Hash Và Dòng Mã Từ Artifact (step3.py)

  Code step3.py (dùng os.walk để duyệt thư mục artifact).
  Chỉnh extract_dir cho malicious (temp/tmp/.../package/) và benign (benign_extract/package/).
  Chạy: python3 step3.py – tạo malicious_artifact_hashes.txt, malicious_artifact_lines.txt và benign tương ứng.

Bước 4: So Sánh Và Phát Hiện Phantom (step4.py)

  Code step4.py (dùng sets trừ để tìm phantom).
  Chạy cho malicious và benign (chỉnh input file tương ứng).
  Chạy: python3 step4.py – tạo malicious_result.json và benign_result.json.
  
KẾT QUẢ:

     Sạch: Tỉ lệ <5% (hoặc thấp như 0.6% ở benign ) – gói an toàn, phantom chỉ do thay đổi nhỏ
     Bị độc: Tỉ lệ >20% (hoặc cao như 41% lines ở malicious ) – nghi ngờ chèn độc, cần kiểm tra thủ công 
