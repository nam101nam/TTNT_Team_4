import os
import shutil
import random


duong_dan_goc = "/home/nam/Documents/TTNT/HumanVision/Data/natural_images"  # Thư mục gốc bạn tải về và giải nén
thu_muc_dich = "HumanVisionData"  # Tên thư mục mới sẽ được tạo ra

#Ti le chia 70/15/15

ty_le_train = 0.7
ty_le_val = 0.15
ty_le_test = 0.15


def chia_du_lieu():
    # 1. Kiểm tra xem thư mục gốc có tồn tại không
    if not os.path.exists(duong_dan_goc):
        print(f"LỖI: Không tìm thấy thư mục '{duong_dan_goc}'")
        return

    # 2. Tạo cấu trúc thư mục mới (train, validation, test)
    if os.path.exists(thu_muc_dich):
        shutil.rmtree(thu_muc_dich)  # Xóa cũ nếu có để làm lại từ đầu

    for split in ['train', 'validation', 'test']:
        for label in ['person', 'no_person']:
            os.makedirs(os.path.join(thu_muc_dich, split, label))

    # 3. Thu thập đường dẫn ảnh
    print("--- Đang quét và gom nhóm dữ liệu ---")

    # Lấy ảnh PERSON
    path_person = os.path.join(duong_dan_goc, 'person')
    files_person = [os.path.join(path_person, f) for f in os.listdir(path_person)]
    print(f"-> Tìm thấy {len(files_person)} ảnh Person.")

    # Lấy ảnh NO_PERSON (Gom từ các folder còn lại)
    cac_lop_khac = ['airplane', 'car', 'cat', 'dog', 'flower', 'fruit', 'motorbike']
    files_no_person = []
    for lop in cac_lop_khac:
        path_lop = os.path.join(duong_dan_goc, lop)
        if os.path.exists(path_lop):
            imgs = [os.path.join(path_lop, f) for f in os.listdir(path_lop)]
            files_no_person.extend(imgs)

    print(f"-> Tìm thấy {len(files_no_person)} ảnh các loại khác.")

    # 4. CÂN BẰNG DỮ LIỆU (Bước quan trọng nhất)
    # Trộn ngẫu nhiên để không bị lấy toàn ảnh máy bay hay toàn ảnh chó
    random.shuffle(files_person)
    random.shuffle(files_no_person)

    # Cắt bớt phe No-Person cho bằng phe Person
    so_luong_chuan = min(len(files_person), len(files_no_person))
    files_person = files_person[:so_luong_chuan]
    files_no_person = files_no_person[:so_luong_chuan]

    print(f"-> Đã cân bằng: Mỗi bên lấy {so_luong_chuan} ảnh.")

    # 5. Hàm chia và copy file
    def copy_vao_folder(danh_sach_file, nhan):
        # Tính toán điểm cắt
        n_train = int(len(danh_sach_file) * ty_le_train)
        n_val = int(len(danh_sach_file) * ty_le_val)

        # Chia list
        tap_train = danh_sach_file[:n_train]
        tap_val = danh_sach_file[n_train: n_train + n_val]
        tap_test = danh_sach_file[n_train + n_val:]

        # Thực hiện copy
        print(f"   Đang copy {nhan}: Train={len(tap_train)}, Val={len(tap_val)}, Test={len(tap_test)}")

        for f in tap_train: shutil.copy(f, os.path.join(thu_muc_dich, 'train', nhan, os.path.basename(f)))
        for f in tap_val: shutil.copy(f, os.path.join(thu_muc_dich, 'validation', nhan, os.path.basename(f)))
        for f in tap_test: shutil.copy(f, os.path.join(thu_muc_dich, 'test', nhan, os.path.basename(f)))

    # Tiến hành chia
    print("--- Bắt đầu chia file ---")
    copy_vao_folder(files_person, 'person')
    copy_vao_folder(files_no_person, 'no_person')

    print(f"\n✅ XONG! Dữ liệu mới nằm trong thư mục: {thu_muc_dich}")


# Chạy hàm
#chia_du_lieu()


# Thay đường dẫn cụ thể vào đây
train_person = "/home/nam/Documents/TTNT/HumanVision/Data/HumanVisionData/train/person"
train_no_person = "/home/nam/Documents/TTNT/HumanVision/Data/HumanVisionData/train/no_person"

validation_person = "/home/nam/Documents/TTNT/HumanVision/Data/HumanVisionData/validation/person"
validation_no_person = "/home/nam/Documents/TTNT/HumanVision/Data/HumanVisionData/validation/no_person"

test_person = "/home/nam/Documents/TTNT/HumanVision/Data/HumanVisionData/test/person"
test_no_person = "/home/nam/Documents/TTNT/HumanVision/Data/HumanVisionData/test/no_person"



print(f"Thư mục có: {len(os.listdir(train_person))} file.")
print(f"Thư mục có: {len(os.listdir(train_no_person))} file.")
print(f"Thư mục có: {len(os.listdir(validation_person))} file.")
print(f"Thư mục có: {len(os.listdir(validation_no_person))} file.")
print(f"Thư mục có: {len(os.listdir(test_person))} file.")
print(f"Thư mục có: {len(os.listdir(test_no_person))} file.")
