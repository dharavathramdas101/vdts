import datetime
from ultralytics import YOLO
import cv2
from helper import create_video_writer

# Define constants
confidence_threshold = 0.8
green = (0, 255, 0)

# initialize the video capture object
video_cap = cv2.VideoCapture(r"C:\Users\DHARAVATH RAMDAS\vdts\input_video.mp4")

# initialize the video writer object
writer = create_video_writer(video_cap, "output.mp4")

#load the pretrained yolo v5 model
model = YOLO("yolov5s.pt")

# start looping video frame
while True:
    start = datetime.datetime.now()

    isTrue, frame = video_cap.read()

    # if there are no more frames to process then break out of loop
    if not isTrue:
        break

    # run the yolo model on the frame
    detections = model(frame)[0]

    # loop over detections
    for data in detections.boxes.data.tolist():
        # extract the confidence probability with detection

        confidence = data[4]

        # fileter out weak detections by ensuring the confidence is greater than the minimum confidence
        if float(confidence) < confidence_threshold:

            continue

        # if the confidence is greater than the minimum confidence
        # draw the bounding box on the frame
        x, y, w, h = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        cv2.rectangle(frame, (x, y), (w, h), green, 2)
        

        # end time to compute the fps
        end = datetime.datetime.now()

        # show the time it took to process 1 frame
        total = (end - start).total_seconds()
        print(f"time to process 1 frame: {total * 1000:.0f} milliseconds")

        # calculaate the frame per sencond and draw it on the frame
        fps = f"FPS: {1 / total:.2f}"
        cv2.putText(frame, fps, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 8)
        
        # show the to out screen
        cv2.imshow("Image", frame)
        writer.write(frame)
        if cv2.waitKey(1) == ord("q"):
            break
        
video_cap.release()
writer.release()
cv2.destroyAllWindows()
        




