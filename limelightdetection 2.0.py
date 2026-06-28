import logging
import time
from networktables import NetworkTables

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Limelight:
    def __init__(self, ip_address="10.0.0.2"):   #limelight'ın kendi orijinal ip adresi girilmeli
        self.ip_address = ip_address
        self.table = None

    def initialize(self):
        NetworkTables.initialize(server=self.ip_address)
        self.table = NetworkTables.getTable("limelight")
        logging.info(f"Connected to Limelight at {self.ip_address}")

    def get_number(self, key, default):
        try:
            return self.table.getNumber(key, default)
        except Exception as e:
            logging.error(f"Error retrieving {key}: {e}")
            return default

    def get_number_array(self, key, default):
        try:
            return self.table.getNumberArray(key, default)
        except Exception as e:
            logging.error(f"Error retrieving {key}: {e}")
            return default

    def get_target_data(self):
        return {
            "tx": self.get_number("tx", 0.0),
            "ty": self.get_number("ty", 0.0),
            "ta": self.get_number("ta", 0.0),
            "tv": self.get_number("tv", 0)
        }

    def get_robot_pose(self):
        pose = self.get_number_array("botpose", [0.0] * 6)
        if len(pose) >= 6:
            return {
                "x": pose[0],
                "y": pose[1],
                "z": pose[2],
                "pitch": pose[3],
                "yaw": pose[4],
                "roll": pose[5]
            }
        return None

    def get_fiducials(self):
        raw_data = self.get_number_array("fiducials", [])
        fiducials = []
        for i in range(0, len(raw_data), 2):
            fiducials.append({"id": raw_data[i], "distance": raw_data[i + 1] if i + 1 < len(raw_data) else None})
        return fiducials

def display_target_data(limelight):
    target_data = limelight.get_target_data()
    if target_data["tv"] == 1:
        logging.info(f"Target detected: TX={target_data['tx']}, TY={target_data['ty']}, TA={target_data['ta']}")
    else:
        logging.info("No target detected.")

def display_robot_pose(limelight):
    robot_pose = limelight.get_robot_pose()
    if robot_pose:
        logging.info(f"Robot Pose: X={robot_pose['x']}, Y={robot_pose['y']}, Z={robot_pose['z']}, "
                     f"Pitch={robot_pose['pitch']}, Yaw={robot_pose['yaw']}, Roll={robot_pose['roll']}")

def display_fiducials(limelight):
    fiducials = limelight.get_fiducials()
    if fiducials:
        for fiducial in fiducials:
            logging.info(f"Fiducial ID={fiducial['id']} Distance={fiducial['distance']} meters")

def main():
    limelight = Limelight()
    try:
        limelight.initialize()
    except Exception as e:
        logging.critical("Failed to initialize Limelight. Exiting.")
        return

    while True:
        try:
            display_target_data(limelight)
            display_robot_pose(limelight)
            display_fiducials(limelight)
        except Exception as e:
            logging.error(f"Error during main loop: {e}")
        time.sleep(0.1)

if __name__ == "__main__":
    main()