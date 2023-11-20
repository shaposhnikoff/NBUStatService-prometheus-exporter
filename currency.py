from prometheus_client import Gauge, start_http_server
import requests,json,logging,time
logging.basicConfig(level=logging.DEBUG)
nbu_api_endpoint = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
currencies_metrics = {}
def create_metrics():
    logging.info("Creating metrics")
    for item in json.loads(requests.get(nbu_api_endpoint).text):
        currency_metric = Gauge(item['cc'], "currency rate", ["date", "currency_name"])
        currencies_metrics[item['cc']] = currency_metric

def reload_currencies():
    logging.info("Reloading currencies")
    for item in json.loads(requests.get(nbu_api_endpoint).text):
        currencies_metrics[item['cc']].labels(date=time.strftime("%Y-%m-%d"), currency_name=item['cc']).set(item['rate'])

if __name__ == '__main__':
    start_http_server(8000)
    create_metrics()
    while True:
        logging.info("Updating metrics")
        # print date and time for debug
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
        reload_currencies()
        time.sleep(60*60*4)

