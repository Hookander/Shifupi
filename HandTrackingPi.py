import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

filecords = open("shifumi/scissorsCoords.txt", "w") #avec les coordonnées directement
filedists = open("shifumi/scissorsDistances.txt", "w") #avec les distances calculées directement
cptImg = 0
# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)
    image_height, image_width, _ = image.shape
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    filecords.write(str(cptImg) + "\n")
    filedists.write(str(cptImg) + "\n")
    print(cptImg)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        # Here is How to Get All the Coordinates
        cx0, cy0 = hand_landmarks.landmark[0].x * image_width, hand_landmarks.landmark[0].y * image_height
        for ids, landmrk in enumerate(hand_landmarks.landmark):
            # print(ids, landmrk)
            cx, cy = landmrk.x * image_width, landmrk.y*image_height
            #print(cx, cy)
            """premier essai : landmarks 8, 12, 16, 20 (position relative par rapport au numéro 0)
                Donc on les enregistre dans un fichier .txt
            """
            wantedLM = [0, 8, 12,  16, 20]
            
            if ids in wantedLM:
              filecords.write(str(ids) + " " + str(cx) + " " +str(cy))
              filecords.write("\n")
              
              if ids != 0:
                dist = np.sqrt( (cx - cx0)**2 + (cy - cy0)**2)
                filedists.write(str(ids) + " " + str(dist) + ("\n"))
            #print (ids, cx, cy)
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    # BM peut pas marcher s'il n'y a pas d'écran :)
    # cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
    cptImg += 1
cap.release()
file.close()