from os import getcwd, makedirs, path, remove, scandir
from re import search
from shutil import move

from colorifix.colorifix import ppaint
from gopro_sync.utils.arguments import argparsing
from tqdm import tqdm

VIDEO_EXT = ".mp4"
PHOTO_EXT = ".jpg"
PROXY_EXT = ".lrv"
THUMB_EXT = ".thm"

# ---- Utils


def scan_files(folder, extensions):
    files = [file for file in scandir(folder) if file.is_file()]
    return [
        [file for file in files if file.name.lower().endswith(ext)]
        for ext in extensions
    ]


def files_size(files):
    b_size = sum(path.getsize(file) for file in files)
    if (kb_size := b_size / 1000) < 1:
        return f"{b_size:.0f} B"
    if (mb_size := kb_size / 1000) < 1:
        return f"{kb_size:.0f} KB"
    if (gb_size := mb_size / 1000) < 1:
        return f"{mb_size:.0f} MB"
    return f"{gb_size:.2f} GB"


def remove_files(files):
    for file in files:
        remove(file.path)


def save_files(files, folder, to=None):
    if not files:
        return
    makedirs(folder)
    out_ext = to or path.splitext(files[0].name)[1][1:]
    for file in tqdm(files, desc=path.basename(folder)):
        filename_match = search(r"G\w_?(\d{2})(\d{4})\.(\w+)", file.name)
        if not filename_match:
            continue
        chapter, number, ext = filename_match.groups()
        filename = f"GoPro_{number}_{chapter}.{out_ext}"
        out_file = path.join(folder, filename)
        move(file.path, out_file)


# ---- Main


def main():
    # parse args
    args = argparsing()
    in_folder = path.join(args.i or getcwd())
    out_folder = path.join(args.o or getcwd(), args.name)
    is_test = args.test

    # check folders
    if not is_test and path.exists(out_folder):
        return ppaint(
            f"\n[#red]ERROR![/] Project [@underline]{path.basename(out_folder)}"
            "[/] already exists!"
        )
    if not path.exists(in_folder):
        return ppaint(
            "\n[#red]ERROR![/] GoPro videos folder [@underline]"
            f"{in_folder}[/] not found!"
        )

    # scan files
    extensions = (VIDEO_EXT, PHOTO_EXT, PROXY_EXT, THUMB_EXT)
    videos, photos, proxies, thumbnails = scan_files(in_folder, extensions)
    ppaint(
        f"\n> Found [#magenta]{len(videos)}[/] videos ([@underline]{files_size(videos)}"
        f"[/]) and [#magenta]{len(photos)}[/] photos ([@underline]{files_size(photos)}"
        "[/])\n"
    )

    # test run
    if is_test:
        ppaint("[@bold]# Testing run..")
        lrv_action = "Moving" if not args.no_lrv else "Removing"
        ppaint(f"> {lrv_action} [#magenta]{len(proxies)}[/] proxy file(s) [.LRV]")
        thm_action = "Moving" if args.save_thm else "Removing"
        ppaint(f"> {thm_action} [#magenta]{len(proxies)}[/] thumbnail file(s) [.THM]")
        ppaint(f"> Moving [#magenta]{len(videos)}[/] video file(s) [.MP4]")
        ppaint(f"> Moving [#magenta]{len(photos)}[/] photo file(s) [.JPG]")
        return

    # remove unused files
    if args.no_lrv:
        if not is_test:
            remove_files(proxies)
    if not args.save_thm:
        remove_files(thumbnails)

    # move files
    if not args.no_lrv:
        save_files(proxies, path.join(out_folder, "proxies"), to="mp4")
    if args.save_thm:
        save_files(thumbnails, path.join(out_folder, "thumbnails"), to="jpg")
    save_files(videos, path.join(out_folder, "videos"))
    save_files(photos, path.join(out_folder, "photos"))


if __name__ == "__main__":
    main()
