import os
import redis
import json
import cv2
import psycopg2
from ultralytics import YOLO

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mercury:mercury_password@nexus:5432/mercury_db")

r = redis.from_url(REDIS_URL)
model = YOLO('yolov8n.pt')  # Load pretrained model

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def process_video(video_path):
    print(f"Processing video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create a new match entry (simplified for MVP)
    cur.execute("INSERT INTO matches (home_team, away_team, date) VALUES (%s, %s, NOW()) RETURNING match_id", ("Home", "Away"))
    match_id = cur.fetchone()[0]
    conn.commit()
    
    frame_count = 0
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        frame_count += 1
        if frame_count % 5 != 0: # Process every 5th frame for speed in MVP
            continue
            
        results = model.track(frame, persist=True, verbose=False)
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                if box.id is None:
                    continue
                    
                track_id = int(box.id.item())
                cls = int(box.cls.item())
                x, y, w, h = box.xywh.tolist()[0]
                
                # Store event/track data (simplified)
                # In a real app, we'd have a separate Tracks table. 
                # For MVP, let's just log it as an 'event' or create a Tracks table if we can.
                # Let's use the 'events' table for now to store raw detections as a JSON blob
                
                detection_data = {
                    "track_id": track_id,
                    "class": cls,
                    "x": x, "y": y, "w": w, "h": h,
                    "frame": frame_count
                }
                
                cur.execute(
                    "INSERT INTO events (match_id, type, timestamp, details) VALUES (%s, %s, %s, %s)",
                    (match_id, "detection", frame_count / 30.0, json.dumps(detection_data))
                )
    
    conn.commit()
    cur.close()
    conn.close()
    cap.release()
    print(f"Finished processing {video_path}")

def main():
    print("Hawkeye started, waiting for tasks...")
    while True:
        # Blocking pop from queue
        task_data = r.brpop("video_processing_queue")
        if task_data:
            task = json.loads(task_data[1])
            video_path = task.get("video_path")
            if video_path and os.path.exists(video_path):
                try:
                    process_video(video_path)
                except Exception as e:
                    print(f"Error processing video: {e}")
            else:
                print(f"Video not found: {video_path}")

if __name__ == "__main__":
    main()
