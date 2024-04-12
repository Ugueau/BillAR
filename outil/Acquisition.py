import threading
from pydispatch import dispatcher
from ultralytics import YOLO
import cv2
from Model.EventYolo import EventYolo
from Singleton.SingletonCache import SingletonCache
from Model.Bille import Bille
from Model.Point import Point
from Model.Queue import Queue
from constants.EventConstants import ACQUISITION_KEY
from Controller import CueController, TrajectoryController
from Controller import BallsController
class AcquisitionThread(threading.Thread):

    def __init__(self):
        super(AcquisitionThread, self).__init__()
        self._stop_event = threading.Event()
        print("fin creation thread Acisition press suite ...")

    def run(self):
        print("run thread Acisition press suite ...")
        # Load YOLO model
        model = YOLO('./YoloModel/v1.pt')

        # Open video camera
        self.cap = cv2.VideoCapture(SingletonCache().index_web_cam_choice, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, -1)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, -1)

        # Restrict the analysis to the table
        webcam_top_left = SingletonCache().profil.webcam_billard_coordonnees_top_left
        webcam_top_right = SingletonCache().profil.webcam_billard_coordonnees_top_right
        webcam_bot_left = SingletonCache().profil.webcam_billard_coordonnees_bot_left
        webcam_bot_right = SingletonCache().profil.webcam_billard_coordonnees_bot_right

        margin = (((webcam_bot_left.y -webcam_top_left.y)+(webcam_bot_right.y-webcam_top_right.y))/2)/6

        while not self._stop_event.is_set() and self.cap.isOpened():
            ret, frame = self.cap.read()

            if not ret:
                break

            # Start prediction with confidence interval (0.7 = 70%)
            results = model.predict(
                frame,
                conf=0.48, verbose=False)

            event_yolo_tmp = EventYolo()

            # Run through the found objects
            for result in results:
                detection_count = result.boxes.shape[0]
                for i in range(detection_count):
                    # Extract coordinates of the object
                    indexName = int(result.boxes.cls[i].item())
                    bounding_box = result.boxes.xyxy[i].cpu().numpy()
                    x1 = bounding_box[0]
                    y1 = bounding_box[1]
                    x2 = bounding_box[2]
                    y2 = bounding_box[3]

                    # If it is a ball create a Bille and add it into SingletonEvent
                    if indexName == 0:
                        if ((min(webcam_top_left.x, webcam_bot_left.x)-margin < min(x1,x2) and
                                max(x1,x2) < max(webcam_top_right.x, webcam_bot_right.x)+margin and
                                min(webcam_top_left.y,webcam_top_right.y)-margin < min(y1,y2)) and
                                max(y1,y2) < max(webcam_bot_left.y, webcam_bot_right.y))+margin:
                            center = Point(((x1 + x2) / 2), ((y1 + y2) / 2))
                            new_ball = Bille(center, abs(x1 - x2)/2)
                            event_yolo_tmp.ball_list.append(new_ball)

                    # If it is a white ball create a Bille and add it into SingletonEvent
                    if indexName == 1:
                        if ((min(webcam_top_left.x, webcam_bot_left.x) - margin < min(x1, x2) and
                             max(x1, x2) < max(webcam_top_right.x, webcam_bot_right.x) + margin and
                             min(webcam_top_left.y, webcam_top_right.y) - margin < min(y1, y2)) and
                            max(y1, y2) < max(webcam_bot_left.y, webcam_bot_right.y)) + margin:
                            center = Point((x1 + x2) / 2, (y1 + y2) / 2)
                            new_white_ball = Bille(center, abs(x1 - x2)/2)

                            event_yolo_tmp.white_ball = new_white_ball


                    # If it is a cue compute the direction and add it into SingletonEvent
                    if indexName == 2:

                        roi = frame[
                              int(y1):int(y2),
                              int(x1):int(x2)
                              ]

                        direction = CueController.find_end_of_cue_stick(roi)
                        coord_x, coord_y = CueController.get_side_coordinate(direction, x1, y1, x2, y2)
                        blue_point_cue_stick = Point(coord_x, coord_y)
                        coord_x, coord_y = CueController.get_opposite_side_coordinate(direction, x1, y1, x2, y2)
                        direction_point_cue_stick = Point(coord_x, coord_y)

                        new_cue_stick = Queue(blue_point_cue_stick, direction_point_cue_stick, direction)
                        event_yolo_tmp.cue_stick_list.append(new_cue_stick)

            self.calculate_trajectory_cue_stick(event_yolo_tmp)

            if event_yolo_tmp.white_ball is not None:
                for ball in event_yolo_tmp.ball_list:
                    ball.radius = ball.radius + event_yolo_tmp.white_ball.radius

            self.calculate_trajectory_ball_white(event_yolo_tmp)
            self.calculate_trajectory_other_ball_impact_with_white_ball(event_yolo_tmp)

            dispatcher.send(ACQUISITION_KEY, event_yolo=event_yolo_tmp)

        # Release the camera
        self.cap.release()
        print("thead end")

    def stop(self):
        self._stop_event.set()

    def calculate_trajectory_ball_white(self, event_yolo: EventYolo):
        if event_yolo.white_ball is not None:
            trajectoire = BallsController.get_trajectory_ball(event_yolo.white_ball, event_yolo.ball_list)
            event_yolo.white_ball.trajectoire = trajectoire
    def calculate_trajectory_other_ball_impact_with_white_ball(self, event_yolo: EventYolo):
        for ball in event_yolo.ball_list:
            if ball.impact is not None:
                liste_ball_copiee = event_yolo.ball_list[:]
                liste_ball_copiee.remove(ball)

                trajectoire = BallsController.get_trajectory_ball(ball, liste_ball_copiee)
                ball.trajectoire = trajectoire
    def calculate_trajectory_cue_stick(self, event_yolo: EventYolo):
        for cue_stick in event_yolo.cue_stick_list:
            if event_yolo.white_ball is not None:
                intersection = TrajectoryController.get_intersection_ball_or_billard(cue_stick.origine_point,
                                                                                     cue_stick.blue_point,
                                                                                     [event_yolo.white_ball])

                cue_stick.trajectoire = (cue_stick.blue_point, intersection)
            else:
                intersection = TrajectoryController.get_intersection_ball_or_billard(cue_stick.origine_point,
                                                                                     cue_stick.blue_point,
                                                                                     [])

                cue_stick.trajectoire = (cue_stick.blue_point, intersection)