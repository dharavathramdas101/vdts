import cv2
import datetime
from ultralytics import YOLO
from helper import create_video_writer
from deep_sort_realtime.deepsort_tracker import DeepSort

confidence_threshold = 0.8
green = (0, 255, 0)
white = (255, 255, 255)

#initialize the video capture object
video_capture = cv2.VideoCapture("input_video.mp4")
# initialize the video writer object
writer = create_video_writer(video_capture, "output2.mp4")

# load the pre-trained yolo v5 model
model = YOLO("yolov5s.pt")
tracker = DeepSort(max_age=50)

while True:
    # loop
    start = datetime.datetime.now()

    isTrue, frame = video_capture.read()
    
    if not isTrue:
        break
    # run the yolo model on the frame
    detections = model(frame)[0]
    
    # initialize the list of bounding boxes and confidences
    results = []

    # detections

    # loop over the detections
    for data in detections.boxes.data.tolist():
        # extract the confidence with predictions

        confidence = data[4]

        # filter out weak detections by ensuring the confidence is greater than the minimum confidence
        if float(confidence) > confidence_threshold:
            continue

        # if the confidence is greater than the minimum confidence get the bounding box and the class id
        x, y, w, h = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        class_id = int(data[5])

        # add the bounding box (x,y, w,h), confidence and class id to the result list
        results.append([[x, y, w-x, h-y], confidence, class_id])
        

        # tracking

        # update the tracker with the new detections
        tracks = tracker.update_tracks(results, frame=frame)

        #loop over the tracks
        for track in tracks:
            # if the track is not confirmed, ignore it
            if not track.is_confirmed():
                continue

            # get track id and bbox 
            track_id = track.track_id
            ltrb = track.to_ltrb()

            x, y, w, h = int(ltrb[0]), int(ltrb[1]), int(ltrb[2]), int(ltrb[3])
            
            # draw the bounding box and the track id
            cv2.rectangle(frame, (x, y), (w, h), green, 2)
            cv2.rectangle(frame, (x, y - 20), (x + 20, y), green, -1)
            cv2.putText(frame, str(track_id), (x + 5, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, white, 2)
            
        # end time to compute the fps
        end = datetime.datetime.now()
        # show the time it tool to process 1 frame
        print(f" time to process 1 frame: {(end-start).total_seconds() * 100:.0f} mills")
        # calculate the frame per second and draw it on the frame
        fps = f"fps: {1 / (end-start).total_seconds():.2f}"
        cv2.putText(frame, fps, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 8)
        
        # show the frame to out screen
        cv2.imshow("image", frame)
        writer.write(frame)
        if cv2.waitKey(1) == ord("q"):
            break

video_cap.realse()
writer.release()
cv2.destroyAllWindows()

            


