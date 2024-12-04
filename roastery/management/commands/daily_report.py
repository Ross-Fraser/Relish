import os
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from checkout.models import Order
from django.utils.timezone import localtime, now
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Send daily report"

    def handle(self, *args, **kwargs):
        today_date = localtime(now()).date()

        today_orders = Order.objects.filter(date__date=today_date)
        total_sales = sum(order.grand_total for order in today_orders)
        total_orders = today_orders.count()

        summary = f"""
            Relish Daily Sales Report for {today_date}:
            - Total Orders: {total_orders}
            - Total Sales: £{total_sales:.2f}
            """

        self.stdout.write(summary)

        # Fetch admin emails
        admin_emails = User.objects.filter(is_staff=True, is_active=True).values_list(
        "email", flat=True
        )

        # Send the report via email
        try:
            send_mail(
                subject=f"Daily Report: {now().date()}",
                message=summary,
                from_email=os.environ.get("EMAIL_HOST_USER"),
                recipient_list=list(admin_emails),
            )
        except Exception as e:
            self.stderr.write(f"Error sending email: {e}")
