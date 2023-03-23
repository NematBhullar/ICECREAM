"""
data model of RecurringInvoice
"""
from src.db_models.entity import Entity
import peewee as pw
from playhouse.postgres_ext import JSONField, IntervalField


class RecurringInvoice(Entity):
    """
    data model representing the table of RecurringInvoice
    """
    id = pw.BigAutoField()
    uid = pw.TextField(null=False)
    invoice_data = JSONField(null=False)
    # integer and text instead of IntervalField
    # as there are different number of days in a month
    frequency = pw.IntegerField(null=False)
    interval = pw.TextField(null=False, constraints=[
        pw.Check("interval in ('Y', 'M', 'W', 'D', 'm')")
    ])
    due_period = IntervalField(null=False)
    recipient = pw.TextField(null=False)
    scheduled_time = pw.DateTimeField(index=True)
