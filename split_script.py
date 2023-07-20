import argparse
import os
import shutil


def split_by_bytes(path, size_limit=25000, mode='move', name='Teil'):
    # Get the list of all files in directory tree at given path
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames]

    # If there are one or zero files just return None
    if len(files) <= 1:
        return None

    files.sort()  # sort files alphabetically

    # Create directories and distribute files
    directory_index = 1
    current_size = 0
    current_dir = os.path.join(path, f"{name}{str(directory_index).zfill(2)}")
    os.makedirs(current_dir, exist_ok=True)
    for file in files:
        file_size = os.path.getsize(file)
        if current_size + file_size > size_limit:
            directory_index += 1
            current_dir = os.path.join(path, f"{name}{str(directory_index).zfill(2)}")
            os.makedirs(current_dir, exist_ok=True)
            current_size = 0
        if mode == 'move':
            shutil.move(file, current_dir)
        elif mode == 'copy':
            shutil.copy(file, current_dir)
        current_size += file_size


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split files into directories based on size limit.')
    parser.add_argument('-p', '--path', type=str, default='./', help='Path to the directory with files.')
    parser.add_argument('-b', '--bytes', type=int, help='Size limit in bytes.')
    parser.add_argument('-mb', '--megabytes', type=int, help='Size limit in megabytes.')
    parser.add_argument('-gb', '--gigabytes', type=int, help='Size limit in gigabytes.')
    parser.add_argument('-m', '--move', action='store_const', const='move', default='move',
                        help='Move files into new directories.')
    parser.add_argument('-c', '--copy', action='store_const', const='copy', help='Copy files into new directories.')
    parser.add_argument('-n', '--name', type=str, default='Teil', help='Name prefix for the new directories.')
    args = parser.parse_args()

    size_limit = args.bytes
    if args.megabytes is not None:
        size_limit = args.megabytes * 10 ** 6
    if args.gigabytes is not None:
        size_limit = args.gigabytes * 10 ** 9

    mode = 'move'
    if args.copy is not None:
        mode = 'copy'

    split_by_bytes(args.path, size_limit, mode, args.name)
