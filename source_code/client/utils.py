from datetime import datetime
import os

def check_articles(articles):
    response = True
    if not articles:
        print("No articles found.")
    else:
        response = False
    
    return response


def display_articles(articles, page_size=10):
    
    if(check_articles(articles)):
        return
    
    total = len(articles)
    for start in range(0, total, page_size):
        end = min(start + page_size, total)
        show_article_batch(articles[start:end], start_index=start + 1)

        if end < total:
            input(f"\nShowing {start + 1} to {end} of {total}. Press Enter to continue...\n")

    


def show_article_batch(batch, start_index=1):

    for index, article in enumerate(batch, start=start_index):
        display_single_article(article, index=index)


def display_single_article(article: dict, index: int):
    print(f"\n--- Article {index} ---")
    print(f"Article Id: {article.get('id')}")
    print(f"Title: {article.get('title', 'N/A')}")
    


def display_article_information(article: dict):
    print(f"\n\nArticle Id: {article.get('id')}")
    print(f"Title: {article.get('title', 'N/A')}")
    print(f"Source: {article.get('source', 'N/A')}")
    print(f"Published: {format_published_date(article.get('published_at'))}")
    print(f"Category: {article.get('category_name', 'Uncategorized')}")
    print(f"Description: {article.get('description', 'No description available')}")
    print(f"URL: {article.get('url', 'N/A')}")
    print(f"Likes: {article.get('like_count')}")
    print(f"Dislikes: {article.get('dislike_count')}")
    

def format_published_date(published_at):
    response = None
    if not published_at or published_at == 'N/A':
        response = 'N/A'

    try:
        response = get_article_published_date(published_at)
    except ValueError:
        return f"{published_at} (format error)"
    
    return response



def get_article_published_date(article_published_at):
    
    if '.' in article_published_at and 'Z' in article_published_at:
        article_published_at = datetime.strptime(article_published_at, '%Y-%m-%dT%H:%M:%S.%fZ')
    
    elif ',' in article_published_at and 'GMT' in article_published_at:
        article_published_at = datetime.strptime(article_published_at, '%a, %d %b %Y %H:%M:%S GMT')
        
    elif 'T' in article_published_at: 
        article_published_at = datetime.fromisoformat(article_published_at.replace('Z', '+00:00'))
        
    else: 
        article_published_at = datetime.strptime(article_published_at, '%Y-%m-%d %H:%M:%S')

    
    return article_published_at


def get_date():
    while True:
        try:
            return user_input_date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def user_input_date():
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    end_date_str = input("Enter end date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    return start_date, end_date


def print_menu(title, options):
    print(f"\n--- {title} ---")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")
    return input("Enter your option: ").strip()


def get_valid_article_id():
    result = None
    article_id_str = input("Enter the Article ID: ").strip()
    if article_id_str.isdigit():
        result = int(article_id_str)
    else:
        print("Invalid Article ID.")
    return result


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')