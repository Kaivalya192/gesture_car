import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

def detect_gesture(landmarks):
    thumb_is_up = landmarks[4].x < landmarks[3].x
    index_is_up = landmarks[8].y < landmarks[6].y
    pinky_is_up = landmarks[20].y < landmarks[18].y
    middle_is_up = landmarks[12].y < landmarks[10].y
    ring_is_up = landmarks[16].y < landmarks[14].y

    if index_is_up and pinky_is_up and not middle_is_up and not ring_is_up:
        return "forward"  
    elif thumb_is_up and not index_is_up and not middle_is_up and not ring_is_up and not pinky_is_up:
        return "backward"  
    elif index_is_up and not middle_is_up and not ring_is_up and not pinky_is_up:
        return "left"  
    elif pinky_is_up and not index_is_up and not middle_is_up and not ring_is_up:
        return "right"  
    else:
        return None
    
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    gesture_detected = False
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            gesture = detect_gesture(hand_landmarks.landmark)
            if gesture:
                print(gesture) 
                gesture_detected = True           
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)    
    if not gesture_detected:
        print("stop")
    cv2.imshow('Hand Gesture Control', image)
    if cv2.waitKey(5) & 0xFF == 27:  
        break

cap.release()
cv2.destroyAllWindows()