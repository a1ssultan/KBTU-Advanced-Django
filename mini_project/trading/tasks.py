from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_order_status_email(email, order_id, status):
    subject = f"Ваш заказ #{order_id} - {status.capitalize()}"

    if status == "created":
        message = f"Ваш заказ #{order_id} успешно создан и ожидает обработки."
    elif status == "completed":
        message = f"Ваш заказ #{order_id} успешно завершен. Спасибо за покупку!"
    elif status == "canceled":
        message = f"Ваш заказ #{order_id} был отменен. Если у вас есть вопросы, свяжитесь с нами."

    send_mail(
        subject,
        message,
        "aisultan.khalelov@gmail.com",
        [email],
        fail_silently=False,
    )
    return f"Email sent to {email} about order #{order_id} status: {status}"
