from sklearn.metrics import f1_score
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from configparser import ConfigParser
from bs4 import BeautifulSoup

# from sqlalchemy import create_engine

import pandas as pd
import psycopg2 as pg
import requests

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def scrap_data():
    base_url = "https://www.malaysiastock.biz/Listed-Companies.aspx"
    index = []
    company_name = []
    stock_name = []
    stock_code = []
    market_name = []
    shariah = []
    sector = []
    market_Cap = []
    last_price = []
    PE = []
    DY = []
    ROE = []

    default_param = "?type=A&value=A"
    url = base_url + default_param
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    filters = soup.findAll("div", {"class": "divMarketFilter"})
    filtering = [
        f.text.replace("\n", "").replace(" - 9", "")
        for f in filters[0].findAll("tr")[0].findAll("td")
    ]

    for f in filtering:
        param = f"?type=A&value={f}"
        url = base_url + param
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        tables = soup.findAll("table", {"class": "marketWatch"})
        rows = tables[0].findAll("tr")

        for row in rows:
            columns = [
                r.text if r.text else r.img.get("src") for r in row.findAll("td")
            ]
            index.append(columns[0])
            company_name.append(row.findAll("h3")[1])
            stock_name.append(row.find("a").text.split("(")[0].strip())
            stock_code.append(row.find("a").get("href").split("=")[1])
            market_name.append(row.find("span").text)
            shariah.append("Yes" if "Yes" in columns[1] else "No")
            sector.append(columns[2])
            market_Cap.append(columns[3])
            last_price.append(columns[4])
            PE.append(columns[5])
            DY.append(columns[6])
            ROE.append(columns[7])

    data = {
        "Company full name": company_name,
        "Stock short name": stock_name,
        "Stock code": stock_code,
        "Market name": market_name,
        "Shariah": shariah,
        "Sector": sector,
        "Market Cap": market_Cap,
        "Last Price": last_price,
        "PE": PE,
        "DY": DY,
        "ROE": ROE,
    }
    df = pd.DataFrame(data)
    df.drop_duplicates(keep="last", inplace=True, ignore_index=True)

    config = ConfigParser()
    config.read("config/postgres.cfg")

    dbconnect = pg.connect(
        dbname=config.get("postgres", "DATABASE"),
        user=config.get("postgres", "USER"),
        password=config.get("postgres", "PASSWORD"),
        host=config.get("postgres", "HOST"),
    )

    df.to_sql("bursa_listed_companies", con=dbconnect, if_exists="replace", index=False)

    # cur = dbconnect.cursor()
    # cur.execute(sql, (vendor_name,))
    return


with DAG(
    "scrap_data",
    start_date=datetime(2022, 4, 17),
    max_active_runs=3,
    schedule_interval="@once",
    default_args=default_args,
    catchup=False,
) as dag:

    scraping = PythonOperator(
        task_id="scrap_data",
        python_callable=scrap_data,
        dag=dag,
    )

    scraping