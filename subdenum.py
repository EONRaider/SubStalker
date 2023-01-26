#!/usr/bin/python3
from src.cli_args import CLIArgumentsParser
from src.subdomain_scanner import SubdomainScanner
from src.output import *

class App:
    def __init__(self):
        self.cli_args = CLIArgumentsParser().parse()
        self.subdomain_scanner = SubdomainScanner(
                    url=self.cli_args.url,
                    output_file=self.cli_args.output,
                    threads=self.cli_args.threads
                )
        self.screen_output = ScreenOutput(self.subdomain_scanner)

    def run(self):
        try:
            self.subdomain_scanner.scan()
        except KeyboardInterrupt:
            print("\n[-] Scan ended by user input")


if __name__ == "__main__":
    App().run()
