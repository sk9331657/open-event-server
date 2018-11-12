from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema
from flask_rest_jsonapi import ResourceList

from app.api.bootstrap import api
from app.api.helpers.utilities import dasherize
from app.models import db
from app.models.event import Event


class AdminSalesFeesSchema(Schema):
    """
    Sales fees and revenue for all events
    """

    class Meta:
        type_ = 'admin-sales-fees'
        self_view = 'v1.admin_sales_fees'
        inflect = dasherize

    id = fields.String()
    name = fields.String()
    payment_currency = fields.String()
    fee_percentage = fields.Float(attribute='fee')
    revenue = fields.Method('calc_revenue')
    ticket_count = fields.Method('calc_ticket_count')

    @staticmethod
    def calc_ticket_count(obj):
        """Count all tickets in all orders of this event"""
        return sum([o.amount for o in obj.orders])

    @staticmethod
    def calc_revenue(obj):
        """Returns total revenues of all completed orders for the given event"""
        return sum(
            [o.get_revenue() for o in obj.orders if o.status == 'completed'])


class AdminSalesFeesList(ResourceList):
    """
    Resource for sales fees and revenue
    """

    methods = ['GET']
    decorators = (api.has_permission('is_admin'), )
    schema = AdminSalesFeesSchema
    data_layer = {'model': Event, 'session': db.session}
