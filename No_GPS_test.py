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

    print("Waiting for sensors to initialize...")
    async for health in drone.telemetry.health():
        if health.is_gyrometer_calibration_ok and health.is_accelerometer_calibration_ok:
            print("Sensors OK (GPS not required).")
            break

    print("Arming motors...")
    try:
        await drone.action.arm()
        print("Motors armed.")
    except Exception as e:
        print(f"Failed to arm: {e}")
        return

    print("Sending initial offboard setpoints...")
    initial_setpoint = VelocityNedYaw(0.0, 0.0, 0.0, 0.0)
    for _ in range(10):
        await drone.offboard.set_velocity_ned(initial_setpoint)
        await asyncio.sleep(0.1)

    print("Starting Offboard mode...")
    try:
        await drone.offboard.start()
        print("Offboard started (stationary mode).")
    except OffboardError as error:
        print(f"Offboard start failed: {error._result.result}")
        print("Attempting to disarm for safety.")
        try:
            await drone.action.disarm()
            print("Drone disarmed safely.")
        except Exception as e:
            print(f"Failed to disarm: {e}")
        return

    print("Holding position for 30 seconds...")
    for i in range(30):
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))
        await asyncio.sleep(1)
        print(f"  {i+1}s...")

    print("Stopping Offboard and landing...")
    try:
        await drone.offboard.stop()
        await drone.action.land()
        print("Landing command sent.")
    except Exception as e:
        print(f"Error stopping offboard or landing: {e}")

    await asyncio.sleep(10)
    print("Test completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())