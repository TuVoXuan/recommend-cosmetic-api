from typing import List
from googletrans import Translator
from common import Comment, CommentTrans

translator = Translator()

def translate_to_english(body: List[Comment]):
    commentTrans: List[CommentTrans] = []
    for comment in body:
        translated_comment = translator.translate(comment.content, dest='en')
        trans = CommentTrans(comment.id, translated_comment.text)
        commentTrans.append(trans)
    return commentTrans