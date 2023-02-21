from pathlib import Path

import pydicom
import os


def main():
    # Файл, сопоставляющий исходную
    # и конечную структуры файлов
    new_file = open("matches.txt", "w")

    folder_path = Path("recruit-main", "src")
    file_list = os.listdir(folder_path)

    for file_name in file_list:
        ds = pydicom.dcmread(Path(folder_path, str(file_name)))
        first_lvl_dir = Path(ds.StudyInstanceUID)
        second_lvl_dir = Path(first_lvl_dir, ds.SeriesInstanceUID)
        third_lvl_dir = Path(second_lvl_dir, ds.SOPInstanceUID + ".dcm")

        try:
            # Удаляется информация из ключа PatientName
            if hasattr(ds, "PatientName"):
                ds.PatientName = None

            # Создается структура файлов
            if not Path.is_dir(first_lvl_dir):
               os.mkdir(first_lvl_dir)
            if not Path.is_dir(second_lvl_dir):
               os.mkdir(second_lvl_dir)
            if not Path.is_file(third_lvl_dir):
                ds.save_as(third_lvl_dir)

            # Файл, сопоставляющий исходную
            # и конечную структуры файлов
            match = fr"{folder_path}\{file_name} = {third_lvl_dir}" + "\n"
            new_file.write(match)

        except FileExistsError as e:
            print(e)

    new_file.close()


if __name__ == '__main__':
    main()




