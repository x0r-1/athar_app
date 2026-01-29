import json
import os
import random

def update_json():
    # 1. استلام البيانات من GitHub Action
    file_id = os.getenv('FILE_ID')
    telegram_caption = os.getenv('VIDEO_TITLE')
    
    worker_url = "https://yellow-wind-75bb.ahhaga123456789.workers.dev/?file_id="
    file_path = 'videos.json'
    captions_path = 'captions.json'

    # 2. تحديد الوصف (من تليجرام أو عشوائي)
    # نتحقق إذا كان الوصف القادم من العامل (Worker) فارغاً أو جملة تلقائية
    is_empty = not telegram_caption or telegram_caption.strip() == "" or "فيديو جديد من أثر" in telegram_caption
    
    if is_empty:
        if os.path.exists(captions_path):
            with open(captions_path, 'r', encoding='utf-8') as f:
                random_captions = json.load(f)
                final_title = random.choice(random_captions)
        else:
            final_title = "اذكر الله" # وصف احتياطي جداً
    else:
        final_title = telegram_caption

    # 3. قراءة بيانات الفيديوهات الحالية
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                videos = json.load(f)
            except:
                videos = []
    else:
        videos = []

    # 4. التأكد من عدم التكرار
    full_url = f"{worker_url}{file_id}"
    if any(v.get('url') == full_url for v in videos):
        print("الفيديو موجود بالفعل!")
        return

    # 5. إضافة الفيديو الجديد بالوصف النهائي
    new_video = {
        "id": str(len(videos) + 1),
        "title": final_title,
        "url": full_url
    }
    videos.append(new_video)

    # 6. حفظ التعديلات
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم إضافة الفيديو بوصف: {final_title}")

if __name__ == "__main__":
    update_json()
