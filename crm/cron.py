import os
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs a heartbeat message to confirm CRM application health.
    Message format: DD/MM/YYYY-HH:MM:SS CRM is alive
    File: /tmp/crm_heartbeat_log.txt
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"
    
    log_file_path = "/tmp/crm_heartbeat_log.txt"

    
    try:
        # Append to file (does not overwrite)
        with open(log_file_path, "a") as f:
            f.write(message)
        print(f"Heartbeat logged: {message.strip()}")
    except Exception as e:
        print(f"Error writing to heartbeat log: {str(e)}")
    
    # Optionally query the GraphQL hello field to verify endpoint is responsive
    try:
        query_graphql_hello()
    except Exception as e:
        print(f"GraphQL hello query failed: {str(e)}")

def query_graphql_hello():
    """
    Queries the GraphQL hello field to verify the endpoint is responsive.
    """
    # GraphQL endpoint URL
    graphql_url = "http://localhost:8000/graphql/"
    
    # Create transport with requests
    transport = RequestsHTTPTransport(url=graphql_url)
    
    # Create GraphQL client
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    # Define query
    query = gql("""
    query {
        hello
    }
    """)
    
    try:
        result = client.execute(query)
        print(f"GraphQL hello response: {result}")
    except Exception as e:
        print(f"Failed to execute GraphQL hello query: {str(e)}")


def updatelowstock():
    """
    Executes the UpdateLowStockProducts mutation via GraphQL endpoint.
    Logs updated product names and new stock levels to /tmp/lowstockupdates_log.txt.
    """
    # GraphQL endpoint URL
    graphql_url = "http://localhost:8000/graphql/"
    
    # Create transport with requests
    transport = RequestsHTTPTransport(url=graphql_url)
    
    # Create GraphQL client
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    # Define mutation
    mutation = gql("""
    mutation {
        updateLowStockProducts {
            products {
                id
                name
                stock
            }
            message
            updatedCount
        }
    }
    """)
    
    log_file_path = "/tmp/lowstockupdates_log.txt"
    
    try:
        result = client.execute(mutation)
        
        if result and 'updateLowStockProducts' in result:
            update_data = result['updateLowStockProducts']
            updated_products = update_data.get('products', [])
            message = update_data.get('message', '')
            updated_count = update_data.get('updatedCount', 0)
            
            # Log the update
            timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
            log_message = f"{timestamp} - {message}\n"
            
            if updated_products:
                for product in updated_products:
                    product_info = f"  Product: {product['name']} (ID: {product['id']}) - New Stock: {product['stock']}\n"
                    log_message += product_info
            
            log_message += "\n"
            
            # Append to log file
            with open(log_file_path, "a") as f:
                f.write(log_message)
            
            print(f"Low stock update logged: {updated_count} products updated")
        else:
            print("No update data received from mutation")
            
    except Exception as e:
        print(f"Failed to execute UpdateLowStockProducts mutation: {str(e)}")
        # Log the error
        try:
            timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
            error_message = f"{timestamp} - Error: {str(e)}\n"
            with open(log_file_path, "a") as f:
                f.write(error_message)
        except Exception as write_error:
            print(f"Error writing to log file: {str(write_error)}")


