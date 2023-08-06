#!/usr/bin/env python3
"""
Analyse a HackerNews post by looking at the comments and calculating the sentiment
"""
import logging
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from time import sleep
from typing import Any, Optional

import requests
from py_executable_checklist.workflow import WorkflowBase, run_workflow
from vaderSentiment import vaderSentiment  # type: ignore

from hn_sentiment import setup_logging


# Common functions across steps
def http_get_request(url: str, headers: Optional[dict] = None, timeout: int = 10) -> Any:
    if headers is None:
        headers = {}
    logging.info("Sending GET request to %s", url)
    response = requests.get(url, headers=headers, timeout=timeout)
    if response.status_code != 200:
        raise LookupError(f"Failed to get {url} with status code {response.status_code}")
    else:
        return response.json()


# Workflow steps


class GetHackerNewsStory(WorkflowBase):
    """
    Fetches Hacker News Story
    """

    story_id: str

    def execute(self) -> dict:
        resp_json: dict = http_get_request(f"https://hacker-news.firebaseio.com/v0/item/{self.story_id}.json")

        # output
        return {"comment_ids": resp_json["kids"]}


class GetHackerNewsComments(WorkflowBase):
    """
    Fetches Hacker News Comments
    """

    comment_ids: list[str]

    def execute(self) -> dict:
        comment_bodies = []

        for comment_id in self.comment_ids:
            comment_url = f"https://hacker-news.firebaseio.com/v0/item/{comment_id}.json"
            resp_json: dict = http_get_request(comment_url)
            if resp_json is not None and resp_json.get("deleted") is not True:
                comment_bodies.append(resp_json["text"])
            sleep(0.5)

        # output
        return {"comments": zip(self.comment_ids, comment_bodies)}


class AnalyseSentiment(WorkflowBase):
    """
    Analyse the sentiment of the comments
    """

    comments: tuple

    def execute(self) -> dict:
        comment_id_with_sentiments = {}
        sentiment_analyser = vaderSentiment.SentimentIntensityAnalyzer()
        for comment_id, comment_body in self.comments:
            sentiment = sentiment_analyser.polarity_scores(comment_body)
            logging.info("Comment ID: %s, Sentiment: %s", comment_id, sentiment)
            comment_id_with_sentiments[comment_id] = {"text": comment_body, "sentiment": sentiment.get("compound")}

        # output
        return {"comment_id_with_sentiments": comment_id_with_sentiments}


class CreateMarkdown(WorkflowBase):
    """
    Create a markdown file
    """

    comment_id_with_sentiments: dict[str, dict[str, str]]

    @staticmethod
    def emoji_for_sentiment(sentiment: float) -> str:
        if sentiment > 0.5:
            return "😀 👍"
        elif sentiment < -0.5:
            return "😡 👎"
        else:
            return "😐 🤷"

    def execute(self) -> dict:
        markdown = """
### Hacker News Sentiment Analysis

"""

        for comment_id, comment in self.comment_id_with_sentiments.items():
            markdown += """
----------------
[Comment ID: {0}](https://news.ycombinator.com/item?id={0})
Sentiment: {1} {2}
""".format(
                comment_id, comment["sentiment"], self.emoji_for_sentiment(float(comment["sentiment"]))
            )

        return {"markdown": markdown}


class WriteMarkdownToFile(WorkflowBase):
    """
    Write the markdown to a file
    """

    markdown: str
    output_file_path: Path

    def execute(self) -> None:
        output_file_directory = self.output_file_path.parent
        output_file_directory.mkdir(parents=True, exist_ok=True)
        self.output_file_path.write_text(self.markdown)


def workflow() -> list[type]:
    return [
        GetHackerNewsStory,
        GetHackerNewsComments,
        AnalyseSentiment,
        CreateMarkdown,
        WriteMarkdownToFile,
    ]


def parse_args():  # type: ignore
    parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-s", "--story-id", type=str, required=True, help="Hacker News Story ID")
    parser.add_argument("-o", "--output-file-path", type=Path, required=True, help="Output markdown file path")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        dest="verbose",
        help="Display context variables at each step",
    )
    return parser.parse_args()


def main() -> None:  # pragma: no cover
    args = parse_args()
    setup_logging(args.verbose)
    context = args.__dict__
    run_workflow(context, workflow())


if __name__ == "__main__":  # pragma: no cover
    main()
