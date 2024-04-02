import argparse
import os
import sys
from common.upload import upload_to_s3

parser = argparse.ArgumentParser(description="Run either tel, dis, or upload function")

parser.add_argument("command", choices=["tel", "dis", "upload"], help="Choose tel, dis, or upload")

# For upload command, add an optional argument for file path
if "upload" in sys.argv:
    parser.add_argument("file_id", type=str, help="ID of the file")
    parser.add_argument("file_path", type=str, help="Path to the file to upload")

args = parser.parse_args()

# Check the command and run the corresponding function
if args.command == "tel":
    from bot import bot_runner
    bot_runner()
elif args.command == "upload":
    # Call the upload.py script with the provided file path
    if hasattr(args, "file_path"):
        upload_to_s3(fargs.ile_path, args.file_id)
