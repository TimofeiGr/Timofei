import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import threading
from queue import Queue
import time
from collections import Counter
import re
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class InterfaxCrawler:
    def __init__(self, start_url, max_pages=200, threads=5, timeout=10):
        self.start_url = start_url
        self.max_pages = max_pages
        self.threads = threads
        self.timeout = timeout


        self.queue = Queue()
        self.visited = set()
        self.visited_lock = threading.Lock()


        self.word_counter = Counter()
        self.counter_lock = threading.Lock()
        self.processed_count = 0


        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }


        self.allowed_domains = {'www.interfax.ru', 'interfax.ru'}


        self.word_pattern = re.compile(r'[а-яё]+', re.IGNORECASE)


        self.stop_words = {
            'и', 'в', 'на', 'с', 'к', 'у', 'о', 'об', 'от', 'до', 'за', 'из', 'по', 'для',
            'что', 'как', 'это', 'было', 'были', 'был', 'была', 'не', 'но', 'а', 'или', 'же',
            'то', 'так', 'вот', 'при', 'без', 'через', 'под', 'над', 'перед', 'между',
            'который', 'которая', 'которое', 'которые', 'этот', 'эта', 'это', 'эти',
            'весь', 'вся', 'все', 'всё', 'всех', 'всем', 'всеми', 'однако', 'потому',
            'поэтому', 'затем', 'тогда', 'там', 'тут', 'здесь', 'туда', 'сюда'
        }

    def is_valid_url(self, url):

        try:
            parsed = urlparse(url)

            if parsed.netloc not in self.allowed_domains:
                return False


            if parsed.fragment or 'javascript:' in url:
                return False

            # Только http/https
            if parsed.scheme not in ('http', 'https'):
                return False


            ignored_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.css', '.js')
            if url.lower().endswith(ignored_extensions):
                return False

            return True
        except:
            return False

    def extract_links(self, soup, base_url):

        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            absolute_url = urljoin(base_url, href)
            if self.is_valid_url(absolute_url):
                links.add(absolute_url)
        return links

    def extract_text(self, soup):

        for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()


        text_parts = []


        article = soup.find('article')
        if article:
            text_parts.append(article.get_text())
        else:

            content_div = soup.find('div', class_=re.compile(r'(content|article|news|text|body)'))
            if content_div:
                text_parts.append(content_div.get_text())
            else:

                body = soup.find('body')
                if body:
                    text_parts.append(body.get_text())

        return ' '.join(text_parts)

    def process_page(self, url):

        try:

            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )


            if response.status_code == 200:
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import threading
from queue import Queue
import time
from collections import Counter
import re
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class InterfaxCrawler:
    def __init__(self, start_url, max_pages=200, threads=5, timeout=10):
        self.start_url = start_url
        self.max_pages = max_pages
        self.threads = threads
        self.timeout = timeout


        self.queue = Queue()
        self.visited = set()
        self.visited_lock = threading.Lock()


        self.word_counter = Counter()
        self.counter_lock = threading.Lock()
        self.processed_count = 0


        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }


        self.allowed_domains = {'www.interfax.ru', 'interfax.ru'}


        self.word_pattern = re.compile(r'[а-яё]+', re.IGNORECASE)


        self.stop_words = {
            'и', 'в', 'на', 'с', 'к', 'у', 'о', 'об', 'от', 'до', 'за', 'из', 'по', 'для',
            'что', 'как', 'это', 'было', 'были', 'был', 'была', 'не', 'но', 'а', 'или', 'же',
            'то', 'так', 'вот', 'при', 'без', 'через', 'под', 'над', 'перед', 'между',
            'который', 'которая', 'которое', 'которые', 'этот', 'эта', 'это', 'эти',
            'весь', 'вся', 'все', 'всё', 'всех', 'всем', 'всеми', 'однако', 'потому',
            'поэтому', 'затем', 'тогда', 'там', 'тут', 'здесь', 'туда', 'сюда'
        }

    def is_valid_url(self, url):

        try:
            parsed = urlparse(url)

            if parsed.netloc not in self.allowed_domains:
                return False


            if parsed.fragment or 'javascript:' in url:
                return False

            # Только http/https
            if parsed.scheme not in ('http', 'https'):
                return False


            ignored_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.css', '.js')
            if url.lower().endswith(ignored_extensions):
                return False

            return True
        except:
            return False

    def extract_links(self, soup, base_url):

        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            absolute_url = urljoin(base_url, href)
            if self.is_valid_url(absolute_url):
                links.add(absolute_url)
        return links

    def extract_text(self, soup):

        for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()


        text_parts = []


        article = soup.find('article')
        if article:
            text_parts.append(article.get_text())
        else:

            content_div = soup.find('div', class_=re.compile(r'(content|article|news|text|body)'))
            if content_div:
                text_parts.append(content_div.get_text())
            else:

                body = soup.find('body')
                if body:
                    text_parts.append(body.get_text())

        return ' '.join(text_parts)

    def process_page(self, url):

        try:

            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )


            if response.status_code == 200:
                logger.debug(f"OK (200): {url}")
            elif response.status_code == 404:
                logger.warning(f"Страница не найдена (404): {url}")
                return None
            elif response.status_code == 403:
                logger.warning(f"Доступ запрещен (403): {url}")
                return None
            elif response.status_code >= 500:
                logger.error(f"Ошибка сервера ({response.status_code}): {url}")
                return None
            else:
                logger.warning(f"Неожиданный код {response.status_code}: {url}")
                return None


            if response.encoding == 'ISO-8859-1':
                response.encoding = 'utf-8'

            # Парсим HTML
            soup = BeautifulSoup(response.text, 'html.parser')


            text = self.extract_text(soup)
            words = self.word_pattern.findall(text.lower())


            filtered_words = [w for w in words if len(w) > 3 and w not in self.stop_words]


            with self.counter_lock:
                self.word_counter.update(filtered_words)


            links = self.extract_links(soup, url)

            return links

        except requests.exceptions.Timeout:
            logger.error(f"Таймаут соединения: {url}")
        except requests.exceptions.ConnectionError:
            logger.error(f"Ошибка соединения: {url}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка HTTP: {url} - {str(e)}")
        except Exception as e:
            logger.error(f"Ошибка парсинга {url}: {str(e)}")

        return None

    def worker(self, thread_id):
        """Рабочий поток для обработки URL из очереди"""
        while True:
            try:
                url = self.queue.get(timeout=2)
            except:

                if self.processed_count >= self.max_pages or self.queue.empty():
                    break
                continue

            if url in self.visited:
                self.queue.task_done()
                continue


            with self.visited_lock:
                if url in self.visited:
                    self.queue.task_done()
                    continue
                self.visited.add(url)
                self.processed_count += 1
                current_processed = self.processed_count


            logger.info(
                f"[Поток {thread_id}] Обработка: {url[:80]}... | Обработано: {current_processed}/{self.max_pages} | В очереди: {self.queue.qsize()}")


            links = self.process_page(url)


            if links and current_processed < self.max_pages:
                with self.visited_lock:
                    for link in links:
                        if link not in self.visited and link not in list(self.queue.queue):
                            self.queue.put(link)

            self.queue.task_done()

    def crawl(self):
        """Запуск краулера"""
        logger.info(f"Запуск краулера для {self.start_url}")
        logger.info(f"Максимум страниц: {self.max_pages}, потоков: {self.threads}")
        logger.info("-" * 80)

        start_time = time.time()


        self.queue.put(self.start_url)


        threads = []
        for i in range(self.threads):
            t = threading.Thread(target=self.worker, args=(i + 1,))
            t.daemon = True
            t.start()
            threads.append(t)


        self.queue.join()


        for t in threads:
            t.join(timeout=1)

        elapsed_time = time.time() - start_time

        logger.info("-" * 80)
        logger.info(f"Краулер завершен за {elapsed_time:.2f} секунд")
        logger.info(f"Обработано страниц: {self.processed_count}")


        self.print_top_words()

    def print_top_words(self, n=10):

        logger.info("\n" + "=" * 60)
        logger.info(f"ТОП-{n} САМЫХ ЧАСТЫХ СЛОВ НА САЙТЕ INTERFAX.RU")
        logger.info("=" * 60)

        top_words = self.word_counter.most_common(n)

        print("\n{:<5} {:<20} {}".format("№", "СЛОВО", "ЧАСТОТА"))
        print("-" * 40)
        for i, (word, count) in enumerate(top_words, 1):
            print("{:<5} {:<20} {}".format(i, word, count))
        print()


def main():
    # Настройки краулера
    CRAWLER_CONFIG = {
        'start_url': 'https://www.interfax.ru/',
        'max_pages': 200,
        'threads': 5,
        'timeout': 10
    }

    crawler = InterfaxCrawler(**CRAWLER_CONFIG)

    try:
        crawler.crawl()
    except KeyboardInterrupt:
        logger.info("\nОбход прерван пользователем")
        crawler.print_top_words()


if __name__ == "__main__":
    main()
