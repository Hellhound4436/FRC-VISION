import requests
import time

class Limelight:
    def __init__(self, ip_address="10.0.0.2"):   #limelight'ın orijinal ip adresi girilmelidir.
        self.base_url = f"http://{ip_address}:5801"

    def get_limelight_data(self):
        try:
            response = requests.get(f"{self.base_url}/get").json()
            return response.get("Results", {})
        except Exception as e:
            print(f"Error fetching data from Limelight: {e}")
            return {}

    def get_target_info(self):
        data = self.get_limelight_data()
        return {
            "target_visible": data.get("tv", 0),
            "tx": data.get("tx", 0.0),
            "ty": data.get("ty", 0.0),
            "ta": data.get("ta", 0.0)
        }

    def get_robot_pose(self):
        data = self.get_limelight_data()
        botpose = data.get("botpose", [0.0] * 6)
        if len(botpose) >= 6:
            return {
                "x": botpose[0],
                "y": botpose[1],
                "z": botpose[2],
                "pitch": botpose[3],
                "yaw": botpose[4],
                "roll": botpose[5]
            }
        return None

    def get_fiducials(self):
        data = self.get_limelight_data()
        fiducials_raw = data.get("fiducials", [])
        fiducials = []
        for i in range(0, len(fiducials_raw), 2):
            fiducials.append({
                "id": fiducials_raw[i],
                "distance": fiducials_raw[i + 1] if i + 1 < len(fiducials_raw) else None
            })
        return fiducials

def main():
    limelight = Limelight()

    while True:
        try:
            # Display target information
            target_info = limelight.get_target_info()
            if target_info["target_visible"]:
                print(f"Target Detected: TX={target_info['tx']}, TY={target_info['ty']}, TA={target_info['ta']}")
            else:
                print("No target detected.")

            # Display robot pose
            robot_pose = limelight.get_robot_pose()
            if robot_pose:
                print(f"Robot Pose: X={robot_pose['x']}, Y={robot_pose['y']}, Z={robot_pose['z']}, "
                      f"Pitch={robot_pose['pitch']}, Yaw={robot_pose['yaw']}, Roll={robot_pose['roll']}")

            # Display fiducial information
            fiducials = limelight.get_fiducials()
            if fiducials:
                for fiducial in fiducials:
                    print(f"Fiducial ID={fiducial['id']}, Distance={fiducial['distance']} meters")
            else:
                print("No fiducials detected.")

        except Exception as e:
            print(f"Error in main loop: {e}")

        time.sleep(0.1)

if __name__ == "__main__":
    main()
