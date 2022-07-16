import praw
from praw.models import MoreComments
import pymongo


reddit = praw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    user_agent="script by u/user"
)

MONGO_DB_CONNECTION = "mongodb+srv://<username>:<password>@cluster0.muvhy.mongodb.net/?retryWrites=true&w=majority"

LIST_OF_SUBREDDITS = ["explainlikeimfive", "IWantToLearn", "askscience", "YouShouldKnow"]
SUBMISSION_FETCH_LIMIT = 10


def parse_list_of_replies(comment, top_level_replies):

    list_of_replies = []

    for reply in top_level_replies:

        reply_data = {}

        if isinstance(comment, MoreComments):
            continue

        reply_data['author_fullname'] = reply.author_fullname if hasattr(reply, 'author_fullname') else ''
        reply_data['body'] = reply.body if hasattr(reply, 'body') else ''
        reply_data['body_html'] = reply.body_html if hasattr(reply, 'body_html') else ''
        reply_data['created_utc'] = reply.created_utc if hasattr(reply, 'created_utc') else ''
        reply_data['downs'] = reply.downs if hasattr(reply, 'downs') else ''
        reply_data['likes'] = reply.likes if hasattr(reply, 'likes') else ''
        reply_data['parent_id'] = reply.parent_id if hasattr(reply, 'parent_id') else ''
        reply_data['permalink'] = reply.permalink if hasattr(reply, 'permalink') else ''
        reply_data['reply_id'] = reply.id if hasattr(reply, 'id') else ''
        reply_data['submission'] = reply.submission.id if hasattr(reply, 'submission') else ''
        reply_data['score'] = reply.score if hasattr(reply, 'score') else ''
        reply_data['subreddit'] = reply.subreddit.display_name if hasattr(reply, 'subreddit') else ''
        reply_data['subreddit_id'] = reply.subreddit_id if hasattr(reply, 'subreddit_id') else ''
        reply_data['total_awards_received'] = reply.total_awards_received if hasattr(reply, 'total_awards_received') else ''
        reply_data['ups'] = reply.ups if hasattr(reply, 'ups') else ''

        list_of_replies.append(reply_data)

    return list_of_replies


def parse_list_of_comments(top_level_comments):

    list_of_comments = []

    for comment in top_level_comments:

        comment_data = {}

        if isinstance(comment, MoreComments):
            continue

        if hasattr(comment, 'score'):
            if int(comment.score) < 1:
                continue

        comment_data['author_fullname'] = comment.author_fullname if hasattr(comment, 'author_fullname') else ''
        comment_data['body'] = comment.body if hasattr(comment, 'body') else ''
        comment_data['body_html'] = comment.body_html if hasattr(comment, 'body_html') else ''
        comment_data['controversiality'] = comment.controversiality if hasattr(comment, 'controversiality') else ''
        comment_data['comment_id'] = comment.id if hasattr(comment, 'id') else ''
        comment_data['created_utc'] = comment.created_utc if hasattr(comment, 'created_utc') else ''
        comment_data['downs'] = comment.downs if hasattr(comment, 'downs') else ''
        comment_data['likes'] = comment.likes if hasattr(comment, 'likes') else ''
        comment_data['parent_id'] = comment.parent_id if hasattr(comment, 'parent_id') else ''
        comment_data['num_reports'] = comment.num_reports if hasattr(comment, 'num_reports') else ''
        comment_data['permalink'] = comment.permalink if hasattr(comment, 'permalink') else ''
        comment_data['score'] = comment.score if hasattr(comment, 'score') else ''
        comment_data['submission'] = comment.submission.id if hasattr(comment, 'submission') else ''
        comment_data['subreddit'] = comment.subreddit.display_name if hasattr(comment, 'subreddit') else ''
        comment_data['total_awards_received'] = comment.total_awards_received if hasattr(comment, 'total_awards_received') else ''
        comment_data['ups'] = comment.ups if hasattr(comment, 'ups') else ''

        top_level_replies = list(comment.replies)
        comment_data['replies'] = parse_list_of_replies(comment, top_level_replies)

        list_of_comments.append(comment_data)

    return list_of_comments


def parse_submission_post(submission):

    submission_data = {}

    submission_data['approved_at_utc'] = submission.approved_at_utc if hasattr(submission, 'approved_at_utc') else ''
    submission_data['author_fullname'] = submission.author_fullname if hasattr(submission, 'author_fullname') else ''
    submission_data['banned_at_utc'] = submission.banned_at_utc if hasattr(submission, 'banned_at_utc') else ''
    submission_data['category'] = submission.category if hasattr(submission, 'category') else ''
    submission_data['num_comments'] = submission.num_comments if hasattr(submission, 'num_comments') else ''
    submission_data['comment_sort'] = submission.comment_sort if hasattr(submission, 'comment_sort') else ''
    submission_data['content_categories'] = submission.content_categories if hasattr(submission, 'content_categories') else ''
    submission_data['created_utc'] = submission.created_utc if hasattr(submission, 'created_utc') else ''
    submission_data['downs'] = submission.downs if hasattr(submission, 'downs') else ''
    submission_data['fullname'] = submission.fullname if hasattr(submission, 'fullname') else ''
    submission_data['hidden'] = submission.hidden if hasattr(submission, 'hidden') else ''
    submission_data['hide_score'] = submission.hide_score if hasattr(submission, 'hide_score') else ''
    submission_data['is_meta'] = submission.is_meta if hasattr(submission, 'is_meta') else ''
    submission_data['is_original_content'] = submission.is_original_content if hasattr(submission, 'is_original_content') else ''
    submission_data['is_reddit_media_domain'] = submission.is_reddit_media_domain if hasattr(submission, 'is_reddit_media_domain') else ''
    submission_data['is_self'] = submission.is_self if hasattr(submission, 'is_self') else ''
    submission_data['is_video'] = submission.is_video if hasattr(submission, 'is_video') else ''
    submission_data['likes'] = submission.likes if hasattr(submission, 'likes') else ''
    submission_data['media'] = submission.media if hasattr(submission, 'media') else ''
    submission_data['media_embed'] = submission.media_embed if hasattr(submission, 'media_embed') else ''
    submission_data['media_only'] = submission.media_only if hasattr(submission, 'media_only') else ''
    submission_data['name'] = submission.name if hasattr(submission, 'name') else ''
    submission_data['over_18'] = submission.over_18 if hasattr(submission, 'over_18') else ''
    submission_data['permalink'] = submission.permalink if hasattr(submission, 'permalink') else ''
    submission_data['pinned'] = submission.pinned if hasattr(submission, 'pinned') else ''
    submission_data['removed_by'] = submission.removed_by if hasattr(submission, 'removed_by') else ''
    submission_data['score'] = submission.score if hasattr(submission, 'score') else ''
    submission_data['secure_media'] = submission.secure_media if hasattr(submission, 'secure_media') else ''
    submission_data['secure_media_embed'] = submission.secure_media_embed if hasattr(submission, 'secure_media_embed') else ''
    submission_data['selftext'] = submission.selftext if hasattr(submission, 'selftext') else ''
    submission_data['selftext_html'] = submission.selftext_html if hasattr(submission, 'selftext_html') else ''
    submission_data['submission_id'] = submission.id if hasattr(submission, 'id') else ''
    submission_data['subreddit'] = submission.subreddit.display_name if hasattr(submission, 'subreddit') else ''
    submission_data['subreddit_id'] = submission.subreddit_id if hasattr(submission, 'subreddit_id') else ''
    submission_data['subreddit_name_prefixed'] = submission.subreddit_name_prefixed if hasattr(submission, 'subreddit_name_prefixed') else ''
    submission_data['subreddit_type'] = submission.subreddit_type if hasattr(submission, 'subreddit_type') else ''
    submission_data['suggested_sort'] = submission.suggested_sort if hasattr(submission, 'suggested_sort') else ''
    submission_data['thumbnail'] = submission.thumbnail if hasattr(submission, 'thumbnail') else ''
    submission_data['title'] = submission.title if hasattr(submission, 'title') else ''
    submission_data['top_awarded_type'] = submission.top_awarded_type if hasattr(submission, 'top_awarded_type') else ''
    submission_data['total_awards_received'] = submission.total_awards_received if hasattr(submission, 'total_awards_received') else ''
    submission_data['treatment_tags'] = submission.treatment_tags if hasattr(submission, 'treatment_tags') else ''
    submission_data['ups'] = submission.ups if hasattr(submission, 'ups') else ''
    submission_data['upvote_ratio'] = submission.upvote_ratio if hasattr(submission, 'upvote_ratio') else ''
    submission_data['url'] = submission.url if hasattr(submission, 'url') else ''
    submission_data['view_count'] = submission.view_count if hasattr(submission, 'view_count') else ''

    top_level_comments = list(submission.comments)

    submission_data['comments'] = parse_list_of_comments(top_level_comments)

    return submission_data


def get_subreddit_posts_data(name, number_of_posts):

    subreddit = reddit.subreddit(name)

    list_of_posts = []

    for submission in subreddit.top(limit=number_of_posts):
        post_data = parse_submission_post(submission)
        list_of_posts.append(post_data)

    return list_of_posts


def upload_to_mongo_db():

    client = pymongo.MongoClient(MONGO_DB_CONNECTION)
    db = client["reddit"]
    collection = db["articles"]

    for SUBREDDIT in LIST_OF_SUBREDDITS:
        print("Getting data from Reddit API for %s" % SUBREDDIT)
        list_of_posts = get_subreddit_posts_data(SUBREDDIT, 50)

        for post in list_of_posts:
            collection.insert_one(post)

    client.close()


def drop_mongo_db_collection(name):

    client = pymongo.MongoClient(MONGO_DB_CONNECTION)
    db = client["reddit"]
    collection = db[name]
    collection.delete_many({})


if __name__ == "__main__":

    upload_to_mongo_db()

    print("\n**** Done ****")
