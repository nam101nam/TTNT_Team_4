import gdown

# ID của folder
folder_id = "1doAMnyk0j-mqfLZFFr-bEDOmH1x_jvIY?hl=vi"
output_dir = "./"   # ví dụ: "./du_lieu/"

gdown.download_folder(id=folder_id, output=output_dir, quiet=False, use_cookies=False)