"""
Web-novel Downloader Utils module.

"""
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def extract_meta_from_url(url) -> dict:
    """
    :param url: main web-novel url to download
    :return: dict
    """
    print("Extract metadata from URL ", url)

    # variables

    author_href_regex = re.compile(r"^/author/\S*")
    chapters_regex = re.compile(r"^\s*CH\s\d*$")
    chapter_number_regex = re.compile(r"\b\d+\b")
    chapter_url_template = url + "/chapter-"

    # Page request and getting soup from it

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Extracting data
    novel_name = soup.h1.text
    name_list = soup.find_all("a", attrs={"href": author_href_regex}, class_="_link")
    author_names = [name.text for name in name_list]
    chapters = int(re.findall(
        chapter_number_regex,
        soup.find(string=chapters_regex).text)[0])  # extracting last chapter number

    # Printing output
    # print("Novel name: ", novel_name)
    # print("Author(s): ", author_names)
    # print("Chapters: ", chapters)
    # print("Links: ", chapter_url_template)

    # Prepare dict
    return {
        "novel_name": novel_name,
        "author_names": author_names,
        "chapters": chapters,
        "chapter_url_template": chapter_url_template
    }

    # with open("output.html", "wb") as output:
    #     output.write(soup.prettify("utf-8"))


def extract_chapter_text(url, chapter_number) -> str:
    """

    :param chapter_number:
    :param url: chapter url
    :return: string with chapter
    """

    # Clean tag/classes lists
    tag_list = ["div", "center"]
    class_list = ["display-hide"]

    # vars
    chapter_url = url
    page = requests.get(chapter_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    article = soup.article
    clean_html(article, tag_list, class_list)
    chapter_text = ""
    chapter_name = ""
    if article.find("h1"):
        chapter_name = article.find("h1").text
    if article.find("h2"):
        chapter_name = article.find("h2").text

    if len(re.findall(r"^Chapter", chapter_name)) > 0:
        chapter_name = ""
    else:
        chapter_name = f"<h2>Chapter {chapter_number}</h2>"

    chapter_text += chapter_name
    chapter_text += "".join([str(x) for x in article.children])

    return chapter_text


def clean_html(article, tag_list, class_list):
    for tag in tag_list:
        found_tags = article.find_all(tag)
        for el in found_tags:
            el.decompose()

    for single_class in class_list:
        found_tags = article.find_all(class_=single_class)
        for el in found_tags:
            el.decompose()


def write_book(book_name, book_name_long, author, chapters_length, chapter_url_template, chapter_list):
    # HTML Structure
    html_boilerplate_start = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <meta name="author" content="{author}">
        <title>{book_name_long}</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
    """

    html_boilerplate_end = """
    </body>
    </html>
    """

    with open(book_name, "a") as output_html:
        output_html.writelines(html_boilerplate_start)

        if len(chapter_list) > 0:
            pbar = tqdm(total=len(chapter_list)+1)
            for chapter_link in chapter_list:
                chapter_number = re.search(r"\d+-?\d$", chapter_link).group(0)
                # print("Chapter num: ", chapter_number)
                output_html.write(extract_chapter_text(url=chapter_link, chapter_number=chapter_number))
                pbar.update(1)
            pbar.close()
        else:
            pbar = tqdm(total=chapters_length)
            for idx in range(1, chapters_length + 1):
                output_html.write(extract_chapter_text(url=chapter_url_template + str(idx), chapter_number=idx))
                pbar.update(1)
            pbar.close()

        output_html.writelines(html_boilerplate_end)

        output_html.close()


def extract_chapters_list(url) -> list:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    tags = soup.find_all("option", attrs={"value": re.compile(r"^https\S*")})
    tag_list = [tag["value"] for tag in tags]
    # print(tag_list)
    # for tag in tags:
    #     print(tag["value"])
    # print("Tags:", tags)
    return tag_list
