import os
import cv2
import json
import redis
from celery import Celery
from moviepy.editor import VideoFileClip, ImageSequenceClip
import numpy as np

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mercury:mercury_password@nexus:5432/mercury_db")

app = Celery('herald-renderer', broker=REDIS_URL, backend=REDIS_URL)

@app.task
def render_video(video_path: str, output_path: str, match_id: int):
    print(f"Rendering video from {video_path} to {output_path} for match {match_id}")
    
    # In a real app, we'd fetch events from DB. 
    # For MVP, we'll just draw some dummy overlays or try to fetch if we can connect to DB.
    # Let's assume we just draw a circle on every frame for now to prove the pipeline.
    
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Create a temporary directory for frames
        temp_dir = "temp_frames"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        frame_count = 0
        frames = []
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
                
            # Draw a simple overlay (e.g., frame counter)
            cv2.putText(frame, f"Frame: {frame_count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Save frame
            frame_path = os.path.join(temp_dir, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_path, frame)
            frames.append(frame_path)
            
            frame_count += 1
            if frame_count > 100: # Limit to 100 frames for MVP speed
                break
        
        cap.release()
        
        # Create video from frames using MoviePy
        clip = ImageSequenceClip(frames, fps=fps)
        clip.write_videofile(output_path, codec='libx264')
        
        # Cleanup
        for f in frames:
            os.remove(f)
        os.rmdir(temp_dir)
        
        return {"status": "completed", "output": output_path}
    except Exception as e:
        print(f"Error rendering video: {e}")
        return {"status": "failed", "error": str(e)}
