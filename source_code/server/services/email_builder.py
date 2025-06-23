from typing import List


class EmailBuilder:
    @staticmethod
    def build_email(articles: List):
        subject = "Your last 4 Hours News Updates!"
        body_lines = "Hi Geek, here are some recent news articles you might be interested in:\n\n"

        for index, article in enumerate(articles):
            body_lines += (
                f"- {index + 1}.) Article Id: {article.id}\n"
                f"  Title: {article.title}\n"
                f"  URL: {article.url}\n\n"
            )

        return subject, "\n" + body_lines