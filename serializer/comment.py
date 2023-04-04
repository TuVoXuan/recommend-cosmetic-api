from typing import Any, Dict, List

from models.comment import OutputComment


def comment_serializer(comment: Dict[str, Any]) -> OutputComment:
    return OutputComment(
        str(comment['user']),
        comment['avgRate'],
        str(comment['productItem'][0])
    )


def comments_serializer(comments: List[OutputComment]) -> List[OutputComment]:
    return [comment_serializer(item) for item in comments]
