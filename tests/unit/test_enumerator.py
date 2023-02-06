from reconlib.core.base import ExternalService

from subenum.core.apis import all_providers
from subenum.enumerator import Enumerator


class TestEnumerator:
    def test_get_tasks(self, target_domain, setup_virustotal_api_key):
        enumerator = Enumerator(
            targets=(target_domain,),
            enumerators=[provider() for provider in all_providers],
            max_threads=10,
        )
        for target, api in enumerator.tasks:
            assert target == target_domain
            assert isinstance(api, ExternalService)
