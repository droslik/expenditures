from datetime import datetime, timedelta
from django.db.models import Count, Sum
from users.models import User
from django.core.mail import send_mail
from .settings import EMAIL_HOST_USER


def send_stat_email(key, value, previous_date):
    subject = "Everyday statistics on incomes/outcomes"
    message = f"Please find below report on your operations for {previous_date}!\n" \
              f"Total number of transactions: {value[0]['total_quantity']}\n" \
              f"Number of income transactions: {value[1]['quantity_income_per_day']}\n" \
              f"Amount of income transactions: {value[2]['amount_per_day']}\n" \
              f"Number of outcome transactions: {value[3]['quantity_outcome_per_day']}\n" \
              f"Amount of outcome transactions: {value[4]['amount_per_day']}\n"
    email_from = EMAIL_HOST_USER
    recipient_list = [key]
    print(message)
    send_mail(
        subject, message, email_from,
        recipient_list, fail_silently=False
    )


def get_everyday_statistics():
    emails = [user.email for user in User.objects.all()]
    previous_day = datetime.now().date() - timedelta(days=1)
    transactions = [
        user.transactions.filter(
            transaction_date__date__lte=previous_day
        ) for user in User.objects.all()
    ]
    statistics = [[transaction.aggregate(total_quantity=Count('id')),
                   transaction.filter(
                       category_id__is_income=True
                   ).aggregate(
                       quantity_income_per_day=Count('id')
                   ),
                   transaction.filter(
                       category_id__is_income=True).aggregate(
                       amount_per_day=Sum('amount')
                   ),
                   transaction.filter(
                       category_id__is_income=False
                   ).aggregate(
                       quantity_outcome_per_day=Count('id')),
                   transaction.filter(
                       category_id__is_income=False
                   ).aggregate(amount_per_day=Sum('amount'))
                   ] for transaction in transactions]

    data = dict(zip(emails, statistics))
    for key, value in data.items():
        send_stat_email(key, value, previous_day)


