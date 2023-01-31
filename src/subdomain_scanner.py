from dotenv import load_dotenv
load_dotenv()
from collections.abc import Collection
from concurrent.futures import ThreadPoolExecutor
from reconlib import crtsh, hackertarget, virustotal


class SubdomainScanner:
    def __init__(
            self,
            url: Collection[str],
            output_file: str,
            threads: int
        ):
        self.url = url
        self.output_file = output_file
        self.threads = threads
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, result):
        for observer in self.observers:
            observer.update(result)

    def scan_url(self, url):
        found_domains = []
        crtsh_info = crtsh.API(target=url)
        crtsh_info.fetch()
        for d in crtsh_info.subdomains[url]:
            found_domains.append(d)
        found_domains.append(crtsh_info.subdomains)

        hackertarget_info = hackertarget.API(target=url)
        hackertarget_info.hostsearch()
        for d in hackertarget_info.subdomains[url]:
            found_domains.append(d)
        found_domains.append(hackertarget_info.subdomains)
        
        virustotal_info = virustotal.API(target=url)
        found_domains.append(virustotal_info.get_subdomains())
        found_domains.append(virustotal_info)

        return found_domains

    def scan(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            try:
                for result in executor.map(self.scan_url, self.url):
                    self.notify(result)
            except KeyboardInterrupt:
                print("\n[-] Scan ended by user input")

        for observer in self.observers:
            observer.end_output()
