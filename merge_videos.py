import json
import os

def merge():
    main_file = 'videos.json'
    temp_dir = 'temp_videos'
    
    if os.path.exists(main_file):
        with open(main_file, 'r', encoding='utf-8') as f:
            try: videos = json.load(f)
            except: videos = []
    else: videos = []

    if not os.path.exists(temp_dir): return

    temp_files = os.listdir(temp_dir)
    if not temp_files: return

    new_entries = []
    for filename in temp_files:
        path = os.path.join(temp_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            new_entries.append(json.load(f))

    # الترتيب حسب وقت الرفع
    new_entries.sort(key=lambda x: x['timestamp'])

    for entry in new_entries:
        if any(v['url'] == entry['url'] for v in videos):
            continue
            
        # حساب ID عددي صحيح بناءً على أكبر ID موجود
        max_id = max([int(v['id']) for v in videos if str(v['id']).isdigit()] + [0])
        
        final_video = {
            "id": str(max_id + 1),
            "title": entry['title'],
            "url": entry['url'],
            "likes": entry['likes']
        }
        videos.insert(0, final_video)

    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    # مسح الملفات المؤقتة بعد الدمج
    for filename in temp_files:
        os.remove(os.path.join(temp_dir, filename))

if __name__ == "__main__":
    merge()
