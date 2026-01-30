import json
import os

def merge_all():
    main_file = 'videos.json'
    queue_dir = 'queue'
    
    if not os.path.exists(queue_dir) or not os.listdir(queue_dir):
        print("المجلد فارغ، لا يوجد شيء لدمجه.")
        return

    # 1. قراءة الملف الرئيسي
    if os.path.exists(main_file):
        with open(main_file, 'r', encoding='utf-8') as f:
            try: videos = json.load(f)
            except: videos = []
    else: videos = []

    # 2. قراءة كل الملفات في الطابور
    new_files = os.listdir(queue_dir)
    temp_entries = []
    for filename in new_files:
        if filename.endswith('.json'):
            with open(os.path.join(queue_dir, filename), 'r', encoding='utf-8') as f:
                temp_entries.append(json.load(f))

    # ترتيبهم بالأقدم أولاً عشان لما نضيفهم يبقوا صح
    temp_entries.sort(key=lambda x: x['timestamp'])

    # 3. الدمج وإعطاء IDs
    for entry in temp_entries:
        url = f"https://yellow-wind-75bb.ahhaga123456789.workers.dev/?file_id={entry['file_id']}"
        if any(v['url'] == url for v in videos): continue

        max_id = max([int(v['id']) for v in videos if str(v['id']).isdigit()] + [0])
        
        new_video = {
            "id": str(max_id + 1),
            "title": entry['title'] if entry['title'] else "اذكر الله",
            "url": url,
            "likes": 0
        }
        videos.insert(0, new_video)

    # 4. حفظ وتنظيف
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    for filename in new_files:
        os.remove(os.path.join(queue_dir, filename))

if __name__ == "__main__":
    merge_all()
