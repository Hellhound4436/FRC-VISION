import networktables
import time

def main():
    networktables.NetworkTables.initialize()
    networktables.NetworkTable.setClientMode()
    networktables.NetworkTable.setIPAddress("10.0.0.2")  # Replace with the actual IP address of Limelight

    limelight_table = networktables.NetworkTable.getTable("limelight")

    while True:
        tx = limelight_table.getNumber("tx", 0.0)
        ty = limelight_table.getNumber("ty", 0.0)
        ta = limelight_table.getNumber("ta", 0.0)
        target_visible = limelight_table.getNumber("tv", 0)

        if target_visible == 1:
            print(f"Target X: {tx}, Target Y: {ty}, Target Area: {ta}")

            botpose = limelight_table.getNumberArray("botpose", [0, 0, 0, 0, 0, 0])
            if botpose:
                x = botpose[0]
                y = botpose[1]
                print(f"Robot Location: ({x}, {y})")

            fiducials = limelight_table.getNumberArray("fiducials", [])
            for fiducial in fiducials:
                fiducial_id = fiducial[0]
                distance = fiducial[1]
                print(f"Fiducial {fiducial_id} is {distance} meters away")

        else:
            print("No target detected")

        time.sleep(0.1)

if __name__ == "__main__":
    main()