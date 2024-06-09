"""
    This program produces messages to a queue on the RabbitMQ server.
    Messages are sent from a defined CSV file (stock_data.csv in this example).
"""

import pika
import sys
import webbrowser
import csv
import time

def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()

def send_message(host: str, queue_name: str, message: str):
    """Send messagese to a queue."""
    try:
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        ch = conn.channel()
        ch.queue_declare(queue=queue_name, durable=True)
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(f"{message}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        conn.close()

def main(host: str, filename:str):
    with open(filename, 'r', newline='') as file:
        reader = csv.DictReader(file)
        # Skip header row
        next(reader)
        # Iterate through each row and grab the data elements we want
        for row in reader:
            stock_date = row['Date']
            stock_open = row['Open']
            stock_close = row['Open']

            if stock_date:
                # Skip null values
                if all(value =='' for value in row.values()):
                    # Continue iterating after skipping a null row
                    continue
                # Example message reading: "AMZN: On 2023-01-04, the stock price opened at 86.55 and closed at 86.55."
                message = f"AMZN: On {stock_date}, the stock price opened at {stock_open} and closed at {stock_close}."
                # Send the message to the 'stock-queue'
                send_message(host, "stock-queue", message)
            time.sleep(5)

if __name__ == "__main__":  
    offer_rabbitmq_admin_site()    

    host = 'localhost'
    stock_file = 'stock_data.csv'

    main(host, stock_file)