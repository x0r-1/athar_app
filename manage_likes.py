import json
import os
import sys

# اسم ملف البيانات
FILE_PATH = "videos.json"

def update_video_likes(video_id, action):
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found.")
        return

    # 1. فتح وقراءة الملف
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        videos = json.load(f)

    # 2. البحث عن الفيديو وتعديل اللايك
    found = False
    for video in videos:
        if str(video.get('id')) == str(video_id):
            if 'likes' not in video:
                video['likes'] = 0
                
            if action == "add":
                video['likes'] += 1
            elif action == "remove":
                video['likes'] = max(0, video['likes'] - 1)
            found = True
            break

    if not found:
        print(f"Video ID {video_id} not found")
        return

    # 3. حفظ التعديلات في الملف
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully {action}ed like to video {video_id}.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        v_id = sys.argv[1]
        v_action = sys.argv[2]
        update_video_likes(v_id, v_action)
