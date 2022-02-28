import argparse  # pragma: no cover
from dwnldr import extract_meta_from_url, write_book, extract_chapters_list


def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m project_name` and `$ project_name `.

    """
    parser = argparse.ArgumentParser(
        description="web-novel downloader.",
        epilog="Enjoy the web-novel downloader functionality!",
    )
    # This is required positional argument
    parser.add_argument(
        "url",
        type=str,
        help="Web-novel main url",
        default="url",
    )

    parser.add_argument(
        "-g",
        "--get_chapters",
        type=str,
        action="store",
        help="Get chapters list from chapter",
        required=False,
    )

    parser.add_argument(
        "-o",
        "--omit",
        action="store_true",
        help="omit writing book",
        required=False,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Optionally adds verbosity",
    )
    args = parser.parse_args()
    # print(f"{args.message} {args.name}!")
    meta = extract_meta_from_url(args.url)

    if args.verbose:
        print("Verbose mode is on.")

    if args.get_chapters:
        # print(args.get_chapters)
        chapter_list = extract_chapters_list(args.get_chapters)

    print("Executing main function")

    if args.omit:
        print("Writing book is omitted")
    else:
        write_book(
            book_name=meta["novel_name"],
            book_name_long=meta["novel_name"],
            author=", ".join(meta["author_names"]),
            chapters_length=meta["chapters"],
            chapter_url_template=meta["chapter_url_template"],
            chapter_list=chapter_list
        )

    print("End of main function")


if __name__ == "__main__":  # pragma: no cover
    main()
