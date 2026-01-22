#!/bin/bash
#Delete customers with no orders since one year ago and log the result
PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

DELETED_COUNT=$(python3 "$PROJECT_DIR/manage.py" shell -c "from django.utils import timezone; import datetime; from crm.models import Customer; cutoff=timezone.now()-datetime.timedelta(days=365); qs=Customer.objects.exclude(order__order_date__gte=cutoff).distinct(); count=qs.count(); qs.delete(); print(count)")

echo "$TIMESTAMP - Deleted $DELETED_COUNT customers" >> /tmp/customer_cleanup_log.txt