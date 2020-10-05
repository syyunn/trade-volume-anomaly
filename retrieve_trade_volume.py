import psycopg2
import auth
import pandas as pd
from pathlib import Path

import json

with open('./partner.json', 'r') as f:
    decoded_hand = json.loads(f.read())

connection = psycopg2.connect(
    user=auth.user,
    password=auth.password,
    host=auth.host,
    port=auth.port,
    database=auth.database,
)  # please make sure to run ssh -L <local_port>:localhost:<remote_port> <user_at_remote>@<remote_address>

conn_status = connection.closed  # 0

years = [i for i in range(2010, 2021)]
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
periods = []
start = f'(period={201001}'

for year in years:
    for month in months:
        period = str(year) + str(month)
        periods.append(period)
        start += f' or period={period}'
        print(period)
start += ')'

commodity_code = '392062'
reporter = 'Peru'
partner = 'Brazil'

try:
    crsr = connection.cursor()
    crsr.execute(
        f"""
        select period, reporter, partner, trade_flow, trade_value_usd from raw___uncmtrd.monthly
        where {start} and aggregate_level  = 6 and commodity_code = '{commodity_code}' and partner = '{partner}' and reporter = '{reporter}' and trade_flow = 'Exports'
        """
    )
    df = pd.DataFrame(crsr.fetchall())
except psycopg2.OperationalError as e:
    print("error occurred", period, e)
    pass


if __name__ == "__main__":
    pass
