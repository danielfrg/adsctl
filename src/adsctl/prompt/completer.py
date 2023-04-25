from __future__ import annotations

from typing import Iterable

from google.ads.googleads.v13.services.types import google_ads_service
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document


class MyCustomCompleter(Completer):
    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        text = document.text_before_cursor.lstrip()

        resources = vars(google_ads_service.GoogleAdsRow)["__annotations__"]
        if " " in text or "\n" in text:
            indices = [i for i, x in enumerate(text) if x == " " or x == "\n"]
            last_index = indices[-1]
            keep_text = text[last_index + 1 :]
            for resource in resources:
                yield Completion(resource, start_position=-len(keep_text))
            yield Completion("FROM", start_position=-len(keep_text))
            yield Completion("WHERE", start_position=-len(keep_text))
            yield Completion("ORDER", start_position=-len(keep_text))
        else:
            yield Completion("SELECT", start_position=-len(text))
