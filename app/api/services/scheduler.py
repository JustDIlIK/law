import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from app.api.services.hemis_helper import (
    get_employee_list,
    get_student_list,
    save_student_from_api,
)

scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Tashkent"))


def start_scheduler():
    if not scheduler.running:
        # scheduler.add_job(get_employee_list, "interval", seconds=1, max_instances=1)
        # scheduler.add_job(get_student_list, "interval", seconds=10, max_instances=1)
        # scheduler.add_job(save_student_from_api, "interval", seconds=1, max_instances=1)
        scheduler.start()
        print("✅ Планировщик запущен")

    print("Старт")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("🛑 Планировщик остановлен")
