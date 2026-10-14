"""Thực hành requests và BeautifulSoup trên Books to Scrape.

Chạy riêng: python src/book_scraper.py [--max-pages 2]
Dữ liệu sách dùng cho thực hành HTML, không ghép với UCI Online Retail.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


PROJECT_ROOT = Path(__file__).resolve().parents[1]
START_URL = "https://books.toscrape.com/"
OUTPUT_FILE = PROJECT_ROOT / "data" / "external" / "books_scraped.csv"
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_books(soup: BeautifulSoup, page_url: str, page_number: int) -> list[dict]:
    """Đọc các thẻ sản phẩm trên một trang HTML thành danh sách dictionary."""
    # find_all(): lấy mọi thẻ <article> có class="product_pod".
    book_tags = soup.find_all("article", class_="product_pod")
    if not book_tags:
        raise ValueError(f"Không tìm thấy article.product_pod tại {page_url}")

    records = []
    for book in book_tags:
        # select_one(): CSS selector 'h3 a' tìm <a> nằm trong <h3>.
        title_tag = book.select_one("h3 a")
        # find(): lấy thẻ <p> đầu tiên có class="price_color".
        price_tag = book.find("p", class_="price_color")
        rating_tag = book.select_one("p.star-rating")
        availability_tag = book.select_one("p.instock.availability")
        if any(tag is None for tag in (title_tag, price_tag, rating_tag, availability_tag)):
            raise ValueError(f"Thiếu thẻ tên, giá, rating hoặc tồn kho tại {page_url}")

        # Rating nằm trong class (ví dụ ['star-rating', 'Three']), không nằm trong text.
        rating = next(
            (RATING_MAP[name] for name in rating_tag.get("class", []) if name in RATING_MAP),
            None,
        )
        if rating is None:
            raise ValueError(f"Không đọc được class rating tại {page_url}")

        records.append(
            {
                # title giữ tên đầy đủ; text của <a> có thể đã bị rút gọn.
                "Title": title_tag["title"],
                "PriceGBP": float(price_tag.get_text(strip=True).replace("£", "")),
                "Rating": rating,
                # get_text(): lấy nội dung chữ, gộp khoảng trắng và bỏ thẻ <i>.
                "Availability": availability_tag.get_text(" ", strip=True),
                # href là thuộc tính của <a>; urljoin đổi link tương đối thành tuyệt đối.
                "ProductURL": urljoin(page_url, title_tag["href"]),
                "PageNumber": page_number,
            }
        )
    return records


def scrape_books(max_pages: int | None = None) -> pd.DataFrame:
    """HTTP GET, parse HTML và theo link next đến hết hoặc đủ số trang yêu cầu."""
    if max_pages is not None and max_pages < 1:
        raise ValueError("max_pages phải là số nguyên dương.")

    records = []
    page_url = START_URL
    visited_pages = set()
    page_number = 1
    with requests.Session() as session:
        session.headers.update({"User-Agent": "RetailAnalytics-EducationalScraper/1.0"})
        while page_url:
            if page_url in visited_pages:
                raise ValueError(f"Link pagination bị lặp: {page_url}")
            visited_pages.add(page_url)

            # GET tải HTML; timeout giới hạn chờ; raise_for_status báo lỗi HTTP 4xx/5xx.
            response = session.get(page_url, timeout=30)
            response.raise_for_status()
            # Website dùng UTF-8; đặt encoding để đọc đúng ký hiệu £ và tên sách.
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            page_records = parse_books(soup, response.url, page_number)
            records.extend(page_records)
            print(f"Page {page_number}: HTTP {response.status_code}, {len(page_records)} books")

            # <li class="next"><a href="...">next</a></li> chứa link trang kế tiếp.
            next_tag = soup.select_one("li.next a")
            if next_tag is None or (max_pages is not None and page_number >= max_pages):
                break
            page_url = urljoin(response.url, next_tag["href"])
            page_number += 1
            time.sleep(0.5)

    return pd.DataFrame(records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Cào Books to Scrape bằng requests và bs4.")
    parser.add_argument("--max-pages", type=int, help="Giới hạn số trang; mặc định cào hết.")
    args = parser.parse_args()
    if args.max_pages is not None and args.max_pages < 1:
        parser.error("--max-pages phải là số nguyên dương.")

    try:
        books = scrape_books(max_pages=args.max_pages)
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        # Chỉ ghi CSV sau khi cào thành công; UTF-8 BOM giúp Excel đọc đúng tên sách.
        books.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    except (requests.RequestException, ValueError, OSError) as error:
        raise SystemExit(f"Scraping failed: {error}") from error
    print(f"Exported {len(books):,} books to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
