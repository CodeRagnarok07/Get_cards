import os
import requests
import time

def downloader(champion: str, data: list):
    extension = ".ogg"
    new_data = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'audio/webm,audio/ogg,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://leagueoflegends.fandom.com/',
        'Origin': 'https://leagueoflegends.fandom.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    output_dir = f'data/{champion}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    with requests.Session() as req:
        req.headers.update(headers)
        
        for index, item in enumerate(data):
            file_name = f'{champion}_{index+1}{extension}'
            file_path = f'{output_dir}/{file_name}'
            
            # Si el archivo ya existe y no está vacío, saltamos la descarga
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                item["file_path"] = file_path
                new_data.append(item)
                continue

            try:
                # Clean URL (remove cache buster if present)
                url = item["audio_url"].split('?')[0] if '?' in item["audio_url"] else item["audio_url"]
                
                print(f"Downloading File {file_name}...")
                download = req.get(url, timeout=30)

                if download.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(download.content)
                    print(f"Success Download File {file_name}")
                    item["file_path"] = file_path
                    new_data.append(item)
                    # Increased delay for stability
                    time.sleep(1)
                else:
                    print(f"Download Failed (Status {download.status_code}) For File {file_name}")
            except Exception as e:
                print(f"Error downloading {file_name}: {e}")
                time.sleep(3)

    return new_data
