import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_ICONS = {
            # Text
            '.txt':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Text.png'),
            '.md':   os.path.join(BASE_DIR, 'Icons', 'Files', 'Text.png'),
            '.rtf':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Text.png'),
            '.log':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Text.png'),
            '.pdf':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Text.png'),
            '.doc':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Text.png'),
            '.docx': os.path.join(BASE_DIR, 'Icons', 'Files', 'Text.png'),
            '.xls':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Text.png'),
            '.xlsx': os.path.join(BASE_DIR, 'Icons', 'Files', 'Text.png'),
            '.ppt':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Text.png'),
            '.pptx': os.path.join(BASE_DIR, 'Icons', 'Files', 'Text.png'),

            # Images
            '.jpg':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Image.png'),
            '.jpeg': os.path.join(BASE_DIR, 'Icons', 'Files', 'Image.png'),
            '.png':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Image.png'),
            '.gif':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Image.png'),
            '.bmp':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Image.png'),
            '.svg':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Image.png'),

            # Videos
            '.mp4':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Video.png'),
            '.mov':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Video.png'),
            '.avi':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Video.png'),
            '.mkv':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Video.png'),
            '.webm': os.path.join(BASE_DIR, 'Icons', 'Files', 'Video.png'),

            # Audio
            '.mp3':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Audio.png'),
            '.wav':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Audio.png'),
            '.ogg':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Audio.png'),
            '.flac': os.path.join(BASE_DIR, 'Icons', 'Files', 'Audio.png'),

            # Archives            
            '.zip':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Archive.png'),
            '.rar':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Archive.png'),
            '.7z':   os.path.join(BASE_DIR, 'Icons', 'Files', 'Archive.png'),
            '.tar':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Archive.png'),
            '.gz':   os.path.join(BASE_DIR, 'Icons', 'Files', 'Archive.png'),

            # Code
            '.py':   os.path.join(BASE_DIR, 'Icons', 'Files', 'Code.png'),
            '.java': os.path.join(BASE_DIR, 'Icons', 'Files', 'Code.png'),
            '.c':    os.path.join(BASE_DIR, 'Icons', 'Files', 'Code.png'),
            '.cpp':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Code.png'),
            '.js':   os.path.join(BASE_DIR, 'Icons', 'Files', 'Code.png'),
            '.html': os.path.join(BASE_DIR, 'Icons', 'Files', 'Code.png'),
            '.css':  os.path.join(BASE_DIR, 'Icons', 'Files', 'Code.png'),

            # Encrypted
            '.encrypted': os.path.join(BASE_DIR, 'Icons', 'Encrypt.png'),

            # Default fallback
            'default': os.path.join(BASE_DIR, 'Icons', 'Files', 'Generic.png'),

        }