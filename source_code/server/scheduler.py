from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from services.news_service import NewsService 


def start_scheduler(app_config):

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        NewsService.fetch_and_store_news, 
        IntervalTrigger(hours=app_config['NEWS_FETCH_INTERVAL_HOURS']),
        id='news_fetch_job',
        name='Fetch News Articles Periodically',
        replace_existing=True, 
        max_instances=1, 
        args=[app_config] 
    )
    scheduler.start()
    print(f"Scheduler started. News will be fetched every {app_config['NEWS_FETCH_INTERVAL_HOURS']} hours.")
    print("Initiating first news fetch now...")
    NewsService.fetch_and_store_news(app_config)
