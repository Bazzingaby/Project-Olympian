import time
import os
import redis
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
INPUT_DIR = "/data/input"

r = redis.from_url(REDIS_URL)

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".mp4"):
            print(f"New video detected: {event.src_path}")
            self.process_video(event.src_path)

    def process_video(self, file_path):
        # Wait a bit to ensure file is fully written (basic check)
        time.sleep(1)
        
        task = {
            "video_path": file_path,
            "status": "pending"
        }
        
        # Push to Redis queue for Hawkeye (or Renderer directly for now)
        # For MVP, we might want to trigger Hawkeye first.
        # Let's assume a 'video_processing_queue'
        r.lpush("video_processing_queue", json.dumps(task))
        print(f"Task pushed to queue: {task}")

if __name__ == "__main__":
    print(f"Harvester watching {INPUT_DIR}...")
    
    # Ensure input directory exists
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR, exist_ok=True)

    event_handler = VideoHandler()
    observer = Observer()
    observer.schedule(event_handler, INPUT_DIR, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
