from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor
import logging
from threading import Lock


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()
    #print(TRANS)

path_parent = 'C://Users/Yaroslav/OneDrive/Рабочий стол/ToSort/'
#text_file = 'C://Users/Yaroslav/OneDrive/Рабочий стол/ToSort/text_1.txt'

p = Path(path_parent)
p_audio = Path(path_parent + '/' + 'audio')
p_img = Path(path_parent + '/' + 'images')
p_docs = Path(path_parent + '/' + 'documents')
p_arhs = Path(path_parent + '/' + 'archives')
p_video = Path(path_parent + '/' + 'video')

def delete_empty_dirs_with_thread():
    with ThreadPoolExecutor() as executor:
        executor.submit(check_and_delete_empty_dir, p)


def normalize(name):
    #print(name)
    element = name.translate(TRANS)
    return element

def check_and_delete_empty_dir(p):
    for i in p.iterdir():
        if i.is_dir() and i.stat().st_size == 0 \
                and i.name != p_audio.name \
                    and i.name != p_arhs.name \
                        and i.name != p_img.name \
                            and i.name != p_docs.name \
                                and i.name != p_video.name:        
            shutil.rmtree(i)
    
def sort_files_folders(p):
    
    # print(p)
    for i in p.iterdir():
        
        p_new = ''
        if i.is_dir():
            print(i.name)
            p_new = str(i)
        
            sort_files_folders(Path(p_new))
        
        if i.is_file():  
            name_without_extension = i.stem
            ext = i.suffix
            #print(ext)
            new_name = normalize(name_without_extension) #передать имя каждого файла
            if ext == '.jpeg' or ext == '.png' or ext == '.jpg' or ext == '.svg':
                i.rename(Path(p_img, new_name + ext))
            elif ext == '.doc' or ext == '.docx' or ext == '.txt' or ext == '.pdf' or ext == '.xlsx' or ext == '.pptx': 
                i.rename(Path(p_docs, new_name + ext))
            elif ext == '.mp3' or ext == '.ogg' or ext == '.wav' or ext == '.amr': 
                i.rename(Path(p_audio, new_name + ext))
            elif ext == '.avi' or ext == '.mp4' or ext == '.mov' or ext == '.mkv': 
                i.rename(Path(p_video, new_name + ext))
            elif ext == '.zip' or ext == '.gz' or ext == '.tar': 
                i.rename(Path(p_arhs, new_name + ext))
                for arc in p_arhs.iterdir():
                    if arc.exists() and arc.is_file():
                        shutil.unpack_archive(arc, Path(str(p_arhs) + '/' + name_without_extension))
            else: 
                i.rename(Path(p, new_name + ext))

        
                 


if __name__ == '__main__':
    sort_files_folders(p)
    
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    
    delete_empty_dirs_with_thread()
    
    logging.debug("Done")