import asyncio
from pathlib import Path
DIR = Path(__file__).resolve().parent

async def read_stream(stream: asyncio.StreamReader):
    """Continuously reads line-by-line from the subprocess output stream."""
    try:
        while True:
            line = await stream.readline()
            if not line:
                print("[Reader] Stream reached EOF.")
                break
            # Decode and strip newline characters
            print(f"\n[Subprocess Output]: {line.decode().rstrip()}", flush = True)
    except asyncio.CancelledError:
        print("[Reader] Read task was cancelled.")

async def write_stream(writer: asyncio.StreamWriter):
    """Continuously prompts the user and sends input to the subprocess."""
    try:
        while True:
            # Run blocking input() inside an executor so it doesn't freeze the loop
            user_input = await asyncio.to_thread(input, "Enter command to send: ")
            
            if user_input.strip().lower() == "exit":
                print("[Writer] Initiating exit sequence...")
                break
            
            # Send input with a newline delimiter
            writer.write(f"{user_input}\n".encode())
            await writer.drain()  # Ensure data is sent over the pipe
            
    except asyncio.CancelledError:
        print("[Writer] Write task was cancelled.")
    finally:
        # Close the stdin stream cleanly
        if writer.can_write_eof():
            writer.write_eof()
        writer.close()
        await writer.wait_closed()

async def subprocess():
    args = "docker run -i --rm -e PYTHONUNBUFFERED=1 jython:latest"
    process = await asyncio.create_subprocess_exec(
        *args.split(" "),
        stdin =asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE, 
        stderr=asyncio.subprocess.STDOUT,
    )
    read_task = asyncio.create_task(read_stream(process.stdout))
    write_task = asyncio.create_task(write_stream(process.stdin))
    await write_task

    try:
        await asyncio.wait_for(process.wait(), timeout=3.0)
        print(f"Process terminated cleanly with exit code: {process.returncode}")
    except asyncio.TimeoutError:
        print("Process timed out. Forcing termination...")
        process.terminate()
        await process.wait()

    await read_task

if __name__ == "__main__":
    # Standard entry point to execute the event loop
    asyncio.run(subprocess())