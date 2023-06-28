import subprocess


def capture_window(window_name):
    # Get window ID
    command = f"xdotool search --name '{window_name}'"
    output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
    window_id = int(output)

    output_file = "./images/browser_screenshot.png"
    command = f"import -window {window_id} {output_file}"
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    capture_window("Play Tetris")
