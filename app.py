import os
import sys
import qrcode
from datetime import datetime
from PIL import Image
from pyzbar.pyzbar import decode


OUTPUT_DIR = "output"
HISTORY_FILE = "history.log"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def log_history(action, data, output_path):
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{datetime.now()} | {action} | {data[:60]} | {output_path}\n")


def render_ascii(qr):
    matrix = qr.get_matrix()
    print("\nASCII QR Preview:\n")
    for row in matrix:
        line = ""
        for col in row:
            line += "██" if col else "  "
        print(line)


def generate_qr(data):
    ensure_output_dir()

    filename = input("Enter output filename (without extension): ").strip()
    if not filename:
        filename = f"qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    fg = input("Enter foreground color (default black): ").strip() or "black"
    bg = input("Enter background color (default white): ").strip() or "white"

    try:
        box_size = int(input("Enter box size (default 10): ") or 10)
        border = int(input("Enter border size (default 4): ") or 4)
    except ValueError:
        box_size = 10
        border = 4

    qr = qrcode.QRCode(
        version=None,
        box_size=box_size,
        border=border
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fg, back_color=bg)

    output_path = os.path.join(OUTPUT_DIR, f"{filename}.png")
    img.save(output_path)

    print("\nQR Code generated successfully.")
    print(f"Saved at: {os.path.abspath(output_path)}")

    render_ascii(qr)

    log_history("GENERATE", data, output_path)


def generate_from_text():
    while True:
        clear()
        print("Generate QR from Text")
        print("---------------------")
        data = input("Enter text (or type 'back'): ")
        if data.lower() == "back":
            return
        if not data.strip():
            print("Input cannot be empty.")
            input("Press Enter to continue...")
            continue
        generate_qr(data)
        input("\nPress Enter to continue...")
        return


def generate_from_file():
    while True:
        clear()
        print("Generate QR from File")
        print("---------------------")
        path = input("Enter file path (or type 'back'): ")
        if path.lower() == "back":
            return
        if not os.path.exists(path):
            print("File does not exist.")
            input("Press Enter to continue...")
            continue
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
        generate_qr(data)
        input("\nPress Enter to continue...")
        return


def decode_qr():
    while True:
        clear()
        print("Decode QR Image")
        print("----------------")
        path = input("Enter QR image path (or type 'back'): ")
        if path.lower() == "back":
            return
        if not os.path.exists(path):
            print("File does not exist.")
            input("Press Enter to continue...")
            continue
        img = Image.open(path)
        result = decode(img)
        if result:
            decoded_data = result[0].data.decode("utf-8")
            print("\nDecoded Data:")
            print(decoded_data)
            log_history("DECODE", decoded_data, path)
        else:
            print("No QR code detected in image.")
        input("\nPress Enter to continue...")
        return


def view_history():
    clear()
    print("QR History")
    print("----------")
    if not os.path.exists(HISTORY_FILE):
        print("No history available.")
    else:
        with open(HISTORY_FILE, "r") as f:
            print(f.read())
    input("\nPress Enter to return...")


def main_menu():
    while True:
        clear()
        print("QR Code Utility")
        print("---------------")
        print("1. Generate QR from Text")
        print("2. Generate QR from File")
        print("3. Decode QR Image")
        print("4. View History")
        print("5. Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            generate_from_text()
        elif choice == "2":
            generate_from_file()
        elif choice == "3":
            decode_qr()
        elif choice == "4":
            view_history()
        elif choice == "5":
            clear()
            print("Exiting application.")
            sys.exit()
        else:
            print("Invalid option.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main_menu()