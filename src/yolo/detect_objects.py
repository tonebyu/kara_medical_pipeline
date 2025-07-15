from ultralytics import YOLO
import os
import pandas as pd
from sqlalchemy import create_engine

# Load YOLOv8 model (you can choose yolov8n.pt for speed or yolov8s.pt for accuracy)
model = YOLO('yolov8n.pt')

# Directory containing images scraped (from Task 1)

IMAGE_DIR = "C:/Users/ssss/Desktop/## 10 Acadamy/Week 7/kara_medical_pipeline/data/raw/Images/2025-07-14"
# PostgreSQL connection via SQLAlchemy
engine = create_engine('postgresql+psycopg2://postgres:1234@localhost:5432/kara_dbt')

results_list = []

for root, dirs, files in os.walk(IMAGE_DIR):
    for filename in files:
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(root, filename)
            try:
                results = model(filepath)
                boxes = results[0].boxes
                if boxes:
                    for box in boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        class_name = model.names[class_id]

                        # Extract message_id from filename if formatted like "msg_123.jpg"
                        try:
                            message_id = int(filename.split('_')[1].split('.')[0])
                        except Exception:
                            message_id = None

                        results_list.append({
                            'message_id': message_id,
                            'detected_object_class': class_name,
                            'confidence_score': round(confidence, 4),
                            'image_file': filename
                        })
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Save results to PostgreSQL if detections exist
if results_list:
    df = pd.DataFrame(results_list)
    df.to_sql('fct_image_detections', engine, schema='staging', if_exists='replace', index=False)
    print(f"✅ {len(results_list)} detections saved to staging.fct_image_detections")
else:
    print("⚠️ No detections found.")
