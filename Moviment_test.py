import asyncio
from mavsdk import System

async def main():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyACM0:57600")

    print("Connecting to drone...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected to Pixhawk!")
            break

    print("Arming motors...")
    await drone.action.arm()

    print("Taking off to 2 meters...")
    await drone.action.takeoff()
    await asyncio.sleep(6)

    from mavsdk.offboard import VelocityNedYaw
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))
    await drone.offboard.start()

    print("Moving 2 meters...")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(1.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(2)

    print("Stopping...")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(1)

    print("Ending Offboard and landing...")
    await drone.offboard.stop()
    await drone.action.land()
    await asyncio.sleep(10)

    print("test completed")

if __name__ == "__main__":
    asyncio.run(main())