#!/usr/bin/env python3
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime
from datetime import timezone as dt_timezone
import sys

transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', use_json=True)
client = Client(transport=transport, fetch_schema_from_transport=False)

query = gql('''
{
  allOrders(first: 100) {
    edges {
      node {
        id
        orderDate
        customer {
          email
        }
      }
    }
  }
}
''')

try:
    result = client.execute(query)
except Exception as e:
    print("GraphQL query failed:", e)
    sys.exit(1)

now = datetime.datetime.now(dt_timezone.utc)
cutoff = now - datetime.timedelta(days=7)
log_lines = []

for edge in result.get('allOrders', {}).get('edges', []):
    node = edge.get('node')
    if not node:
        continue
    order_id = node.get('id')
    order_date_str = node.get('orderDate')
    email = node.get('customer', {}).get('email', '')
    if not order_date_str:
        continue
    try:
        od = datetime.datetime.fromisoformat(order_date_str.replace('Z', '+00:00'))
    except Exception:
        continue
    if od >= cutoff:
        ts = now.strftime('%Y-%m-%d %H:%M:%S')
        log_lines.append(f"{ts} - Order ID {order_id} - {email}")

if log_lines:
    with open('/tmp/order_reminders_log.txt', 'a') as f:
        for l in log_lines:
            f.write(l + '\n')

print("Order reminders processed!")
