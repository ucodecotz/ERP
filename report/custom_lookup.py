from django.db.models import Lookup
from django.db.models.fields import Field, CharField

class CustomDateLookup(Lookup):
    """A custom lookup, that lets you query DateField and DateTimeFields by a date"""

    lookup_name = 'cudate'  # This enables us to use __date='2015-10-18' in a query

    def as_sql(self, compiler, connection):
        # The left-hand-side (lhs) in the query's WHERE clause. It consists
        # of your app name and field name. e.g. '"myapp"."scheduled"'
        # In this case, the left-hand-side has no params.
        lhs, lhs_params = self.process_lhs(compiler, connection)

        # The right-hand-side (rhs) + its params will define the input used
        # in the query's WHERE clause. At this point, the rhs_params will
        # be a datetime object, e.g.: datetime(2015, 10, 18, 0, 0, tzinfo=)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        # Both PostgreSQL and MySQL have a DATE function that lets us query
        # by date. The where clause in the generated SQL will look something
        # like, WHERE DATE(scheduled) = '2015-10-18'
        params = lhs_params + rhs_params
        return 'DATE(%s) = %s' % (lhs, rhs), params


CharField.register_lookup(CustomDateLookup)
# DateTimeField.register_lookup(DateLookup)