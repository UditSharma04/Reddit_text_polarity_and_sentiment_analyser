import asyncio
from src.reddit_client import RedditClient
from src.text_analysis import TextAnalyzer
from src.sentiment_analysis import calculate_sentiment_distribution
from src.entity_analysis import EntityAnalyzer
from src.visualization import Visualizer
from src.utils import save_results, read_file
from config.config import REDDIT_CONFIG
from src.content_generator import ContentGenerator

async def main():
    try:
        # Initialize components
        reddit_client = RedditClient(**REDDIT_CONFIG)
        text_analyzer = TextAnalyzer()
        entity_analyzer = EntityAnalyzer()
        visualizer = Visualizer()
        content_generator = ContentGenerator()

        # Get user input
        input_query = input("Enter your search query: ").strip()
        if not input_query:
            raise ValueError("Search query cannot be empty")
            
        limit = int(input("Enter number of results per keyword (default 20): ") or 20)
        if limit < 1:
            raise ValueError("Limit must be positive")
            
        # Extract and process keywords
        keywords = text_analyzer.extract_keywords(input_query)
        print(f"Extracted Keywords: {keywords}")
        
        search_query = " ".join(keywords)
        print(f"Searching Reddit for: '{search_query}'")

        # Search Reddit
        all_results = await reddit_client.search_reddit(search_query, limit=limit)

        if not all_results:
            print("No results found. Analysis cannot be performed.")
            return

        # Save results
        save_results(all_results, filename='reddit_results.txt')
        print("Results saved to 'reddit_results.txt'.")

        # Perform analyses
        sentiment_distribution = calculate_sentiment_distribution(all_results)
        
        if any(sentiment_distribution.values()):
            print("\nSentiment Distribution:")
            print(f"Positive: {sentiment_distribution['positive']:.2f}%")
            print(f"Negative: {sentiment_distribution['negative']:.2f}%")
            print(f"Neutral: {sentiment_distribution['neutral']:.2f}%")

            # Extract and analyze text content
            text = read_file('reddit_results.txt')
            texts = [r['text'] for r in all_results if r['text']]
            combined_text = " ".join(texts)

            # Perform various analyses
            top_keywords = text_analyzer.extract_top_keywords(text)
            topics = text_analyzer.perform_topic_analysis(texts)
            readability_scores = entity_analyzer.analyze_readability(combined_text)
            entities = entity_analyzer.extract_entities(combined_text)

            # Display results
            if top_keywords:
                print("\nTop 50 Keywords:")
                for score, phrase in top_keywords:
                    print(f"Keyword: {phrase} | Score: {score}")

            if topics:
                print("\nMain Topics Discovered:")
                for topic in topics:
                    print(topic)

            if readability_scores:
                print("\nReadability Scores:")
                for metric, score in readability_scores.items():
                    print(f"{metric}: {score:.2f}")

            if entities:
                print("\nNamed Entities Found:")
                for entity_type, entity_list in entities.items():
                    if entity_list:
                        print(f"\n{entity_type}:")
                        print(", ".join(set(entity_list)))

            # Generate content
            print("\nGenerating engaging content based on analysis...")
            generated_posts = content_generator.generate_content(
                query=input_query,
                keywords=top_keywords,
                sentiment_data=sentiment_distribution
            )
            
            if generated_posts:
                print("\nGenerated Post:")
                print("-" * 50)
                print(generated_posts[0])
                print("-" * 50)

            # Show visualization
            visualizer.plot_sentiment_distribution(sentiment_distribution)

    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())