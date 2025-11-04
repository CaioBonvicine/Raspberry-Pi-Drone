import asyncio
from mavsdk import System
from mavsdk.offboard import VelocityNedYaw, OffboardError

async def main():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyACM0:57600")

    print("Connecting to drone...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected to Pixhawk!")
            break

    print("Waiting for telemetry to initialize...")
    async for health in drone.telemetry.health():
        if health.is_gyrometer_calibration_ok and health.is_accelerometer_calibration_ok:
            print("Sensors OK (no GPS required).")
            break

    print("Arming motors...")
    try:
        await drone.action.arm()
        print("Motors armed.")
    except Exception as e:
        print(f"Arming error: {e}")
        return

    print("Starting Offboard (no movement)...")
    try:
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))
        await drone.offboard.start()
        print("Offboard started (drone will remain stationary).")
    except OffboardError as error:
        print(f"Offboard start error: {error._result.result}")
        print("Attempting to disarm for safety.")
        await drone.action.disarm()
        return

    print("Maintaining stationary flight for 30 seconds...")
    for i in range(30):
        await asyncio.sleep(1)
        print(f"  {i+1}s...")

    print("Stopping Offboard and landing...")
    await drone.offboard.stop()

    try:
        await drone.action.land()
        print("Land command sent.")
    except Exception as e:
        print(f"Landing failed: {e}")

    await asyncio.sleep(10)
    print("Test complete!")

if __name__ == "__main__":
    asyncio.run(main())