import os
from datetime import datetime
import requests
from django.conf import settings

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
    from django.urls import reverse
    from django.test import RequestFactory
    from alx_backend_graphql.schema import schema
    
    query = """
    query {
        hello
    }
    """
    
    try:
        result = schema.execute(query)
        if result.errors:
            print(f"GraphQL errors: {result.errors}")
        else:
            print(f"GraphQL hello response: {result.data}")
    except Exception as e:
        print(f"Failed to execute GraphQL hello query: {str(e)}")
