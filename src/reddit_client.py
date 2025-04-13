import asyncpraw
import asyncio
from langdetect import detect

class RedditClient:
    def __init__(self, client_id, client_secret, user_agent):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        
    async def search_reddit(self, query, limit=100, max_retries=3, retry_delay=2):
        results = []
        reddit = None
        
        for attempt in range(max_retries):
            try:
                reddit = asyncpraw.Reddit(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    user_agent=self.user_agent
                )
                
                subreddit = await reddit.subreddit("all")
                async for post in subreddit.search(query, limit=limit):
                    try:
                        if not post.author:
                            continue
                            
                        if self.is_english(post.title + " " + post.selftext):
                            results.append(self.process_post(post))
                            await self.process_comments(post, results)

                    except Exception as e:
                        print(f"Error processing post: {e}")
                        continue
                        
                break
                    
            except Exception as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                else:
                    print("Max retries reached. Could not connect to Reddit.")
            
            finally:
                if reddit:
                    await reddit.close()
                    
        if not results:
            print("No results found. Please try a different search query.")
            
        return results

    @staticmethod
    def is_english(text):
        try:
            return detect(text) == 'en'
        except:
            return False

    def process_post(self, post):
        from .sentiment_analysis import analyze_sentiment
        return {
            'type': 'post',
            'title': post.title,
            'author': str(post.author),
            'score': post.score,
            'url': post.url,
            'subreddit': str(post.subreddit),
            'text': post.selftext,
            'sentiment': analyze_sentiment(post.title + " " + post.selftext)
        }

    async def process_comments(self, post, results):
        from .sentiment_analysis import analyze_sentiment
        try:
            await post.load()
            comments = await post.comments()
            await comments.replace_more(limit=0)
            async for comment in comments:
                if self.is_english(comment.body):
                    results.append({
                        'type': 'comment',
                        'author': str(comment.author),
                        'score': comment.score,
                        'text': comment.body,
                        'post_title': post.title,
                        'post_url': post.url,
                        'sentiment': analyze_sentiment(comment.body)
                    })
        except Exception as e:
            print(f"Error fetching comments: {e}") 