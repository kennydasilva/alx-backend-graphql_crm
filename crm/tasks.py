from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    graphql_url = "http://localhost:8000/graphql/"

    transport = RequestsHTTPTransport(url=graphql_url)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
        customers {
            id
        }
        orders {
            totalAmount
        }
    }
    """)

    result = client.execute(query)

    total_customers = len(result.get("customers", []))
    orders = result.get("orders", [])
    total_orders = len(orders)
    total_revenue = sum(o.get("totalAmount", 0) for o in orders)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_message = (
        f"{timestamp} - Report: "
        f"{total_customers} customers, "
        f"{total_orders} orders, "
        f"{total_revenue} revenue\n"
    )

    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(log_message)

    return "CRM report generated"
