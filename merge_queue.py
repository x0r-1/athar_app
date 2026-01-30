import json
import os

def merge_all():
    main_file = 'videos.json'
    queue_dir = 'queue'
    
    # لو مفيش فيديوهات جديدة في الطابور اقفل
    if not os.path.exists(queue_dir) or not os.listdir(queue_dir):
        print("المجلد فارغ.")
        return

    # 1. قراءة الملف الرئيسي
    if os.path.exists(main_file):
        with open(main_file, 'r', encoding='utf-8') as f:
            try: videos = json.load(f)
            except: videos = []
    else: videos = []

    # 2. قراءة كل الملفات في الطابور (queue)
    new_files = [f for f in os.listdir(queue_dir) if f.endswith('.json')]
    temp_entries = []
    for filename in new_files:
        path = os.path.join(queue_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            temp_entries.append(json.load(f))

    # ترتيبهم بالأقدم أولاً (حسب وقت الرفع) عشان يدخلوا الملف بالترتيب الصح
    temp_entries.sort(key=lambda x: x['timestamp'])

    # 3. الدمج وإعطاء الـ IDs العددي
    for entry in temp_entries:
        url = f"https://yellow-wind-75bb.ahhaga123456789.workers.dev/?file_id={entry['file_id']}"
        
        # منع التكرار
        if any(v['url'] == url for v in videos):
            continue

        # حساب الـ ID بناءً على أكبر رقم موجود
        max_id = max([int(v['id']) for v in videos if str(v['id']).isdigit()] + [0])
        
        new_video = {
            "id": str(max_id + 1),
            "title": entry['title'] if (entry['title'] and entry['title'].strip()) else "اذكر الله",
            "url": url,
            "likes": 0
        }
        # إضافة الفيديو في أول القائمة
        videos.insert(0, new_video)

    # 4. حفظ الملف النهائي وتنظيف الطابور
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    # مسح الملفات المؤقتة عشان الطابور يفضى للمرة الجاية
    for filename in new_files:
        os.remove(os.path.join(queue_dir, filename))
    print(f"✅ تم دمج {len(temp_entries)} فيديوهات بنجاح.")

if __name__ == "__main__":
    merge_all()
