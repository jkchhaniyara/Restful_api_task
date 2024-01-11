"""
* Create a simple command-line REST client called restful.py able to GET and POST from JSONPlaceholder.

"""
import argparse
import requests
import json
import csv


class Restful:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, method, endpoint, output=None, payload=None):
        self.method = method
        self.endpoint = endpoint
        self.output = output
        self.payload = payload

    def perform_request(self):
        url = f"{self.BASE_URL}{self.endpoint}"
        response = None

        try:
            if self.method == 'GET':
                response = requests.get(url)
            elif self.method == 'POST':
                response = requests.post(url, json=self.payload)

            response.raise_for_status()  

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            if response is not None:
                print(f"Server response: {response.text}")
            return

        if response is not None:
            print(f"HTTP Status Code: {response.status_code}")
            if 200 <= response.status_code < 300:
                if self.output:
                    self.save_response(response)
                else:
                    print(response.text)
            else:
                print("Request failed. Non-2XX status code received.")
                exit(1)
        else:
            print("Request failed. No response received.")
            exit(1)

    def save_response(self, response):
        if self.output.endswith(".json"):
            with open(self.output, "w") as json_file:
                json.dump(response.json(), json_file, indent=2)
            print(f"Response saved to {self.output}")
        elif self.output.endswith(".csv"):
            self.save_csv(response)
        else:
            print("Unsupported output format. Please use .json or .csv.")

    def save_csv(self, response):
        data = response.json() if response is not None else None
        if isinstance(data, list) and data:
            keys = data[0].keys()
            with open(self.output, "w", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            print(f"Response saved to {self.output}")
        else:
            print("Invalid data format for CSV.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("METHOD", choices=['get', 'post'],help="Request method")
    parser.add_argument("ENDPOINT",help="Request endpoint URI fragment")
    parser.add_argument("-o", "--output",help="Output to .json or .csv file (default: dump to stdout)")
    parser.add_argument("-d", "--data", help="Data to send with request")

    args = parser.parse_args()

    payload = json.loads(args.data) if args.data else None
    client = Restful(args.METHOD.upper(), args.ENDPOINT, args.output, payload)
    client.perform_request()


if __name__ == "__main__":
    main()
