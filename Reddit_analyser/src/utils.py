def save_results(results, filename='reddit_results.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        for result in results:
            if result['type'] == 'post':
                file.write(f"Post Title: {result['title']}\n")
                file.write(f"Author: {result['author']}\n")
                file.write(f"Score: {result['score']}\n")
                file.write(f"Subreddit: {result['subreddit']}\n")
                file.write(f"URL: {result['url']}\n")
                file.write(f"Text: {result['text']}\n")
                file.write(f"Sentiment: {result['sentiment']}\n")
                file.write("\n" + "="*80 + "\n")
            elif result['type'] == 'comment':
                file.write(f"Comment by: {result['author']}\n")
                file.write(f"Score: {result['score']}\n")
                file.write(f"Text: {result['text']}\n")
                file.write(f"From Post: {result['post_title']}\n")
                file.write(f"Post URL: {result['post_url']}\n")
                file.write(f"Sentiment: {result['sentiment']}\n")
                file.write("\n" + "="*80 + "\n")

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin-1') as file:
            return file.read() 