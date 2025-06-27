from datetime import datetime


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

    for i, article in enumerate(batch, start=start_index):
        display_single_article(article, index=i)


def display_single_article(article, index):
    print(f"\n--- Article {index} ---")
    print(f"Article Id: {article.get('id')}")
    print(f"Title: {article.get('title', 'N/A')}")
    


def display_article_information(article: dict):
    print(f"Article Id: {article.get('id')}")
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



def get_article_published_date(published_at_str):
    
    if '.' in published_at_str and 'Z' in published_at_str:
        pub_dt = datetime.strptime(published_at_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    
    elif ',' in published_at_str and 'GMT' in published_at_str:
            pub_dt = datetime.strptime(published_at_str, '%a, %d %b %Y %H:%M:%S GMT')
        
    elif 'T' in published_at_str: 
        pub_dt = datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
        
    else: 
        pub_dt = datetime.strptime(published_at_str, '%Y-%m-%d %H:%M:%S')

    
    return pub_dt


def get_date():
    while True:
        try:
            start_date_str = input("Enter start date (YYYY-MM-DD): ")
            end_date_str = input("Enter end date (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            return start_date, end_date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def print_menu(title, options):
    print(f"\n--- {title} ---")
    for i, opt in enumerate(options, start=1):
        print(f"{i}. {opt}")
    return input("Enter your option: ").strip()

def get_valid_article_id():
    article_id_str = input("Enter the Article ID: ").strip()
    if article_id_str.isdigit():
        return int(article_id_str)
    print("Invalid Article ID.")
    return None
