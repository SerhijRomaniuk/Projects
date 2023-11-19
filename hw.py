import os
import shutil
import sys

def process_folder(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path):
            process_folder(item_path)

        elif os.path.isfile(item_path):
            process_file(item_path)

def normalize(filename):
    trans_map = str.maketrans("абвгдеёзийклмнопрстуфхъыэ", "abvgdeezijklmnoprstufh'yie")
    filename = filename.lower().translate(trans_map)
    filename = ''.join(c if c.isalnum() or c == '.' else '_' for c in filename)
    
    return filename

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            normalized_filename = normalize(filename)
            normalized_file_path = os.path.join(root, normalized_filename)
            
            os.rename(file_path, normalized_file_path)
            
            _, file_extension = os.path.splitext(normalized_filename)
            
            if file_extension[1:].upper() in {'JPEG', 'PNG', 'JPG', 'SVG'}:
                shutil.move(normalized_file_path, os.path.join('images', normalized_filename))
            elif file_extension[1:].upper() in {'AVI', 'MP4', 'MOV', 'MKV'}:
                shutil.move(normalized_file_path, os.path.join('video', normalized_filename))
            elif file_extension[1:].upper() in {'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'}:
                shutil.move(normalized_file_path, os.path.join('documents', normalized_filename))
            elif file_extension[1:].upper() in {'MP3', 'OGG', 'WAV', 'AMR'}:
                shutil.move(normalized_file_path, os.path.join('audio', normalized_filename))
            elif file_extension[1:].upper() in {'ZIP', 'GZ', 'TAR'}:
                
                shutil.unpack_archive(normalized_file_path, os.path.join('archives', normalized_filename[:-len(file_extension)]))
            else:
                pass

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        sys.exit(1)

    folder_to_sort = sys.argv[1]

    if not os.path.exists(folder_to_sort):
        print(f"Error: Folder '{folder_to_sort}' does not exist.")
        sys.exit(1)

    process_folder(folder_to_sort)

    print("Sorting completed.")
