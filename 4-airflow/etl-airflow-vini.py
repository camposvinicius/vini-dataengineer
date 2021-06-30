from airflow.decorators import dag, task
from airflow.models import Variable
from datetime import datetime
import requests
import json
import boto3
from sqlalchemy import create_engine

default_args = {
    'owner': 'Vinicius Campos',
    "depends_on_past": False,
    "start_date": datetime(2021, 6, 29),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
}

@dag(dag_id = 'vini-teste-airflow', tags= ['teste','vini','airflow'], default_args=default_args, 
            schedule_interval = None, description = "ETL (IBGE) => Datalake and DW")
def etl():
    
    @task
    def extracao_mongo():
        import pymongo
        import pandas as pd 
        client = pymongo.MongoClient(
            "mongodb+srv://estudante_igti:SRwkJTDz2nA28ME9@unicluster.ixhvw.mongodb.net/ibge?retryWrites=true&w=majority")
        db = client.ibge
        pnad_collect = db.pnadc20203
        df = pd.DataFrame(list(pnad_collect.find()))
        df.to_csv('/tmp/pnadc20203.csv', index=False, encoding = 'utf-8', sep= ';')
        return '/tmp/pnadc20203.csv'

    @task
    def extracao_api():
        import pandas as pd
        res = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP/mesorregioes")
        resjson = json.loads(res.text)
        df = pd.DataFrame(resjson)[['id','nome']]
        df.to_csv('/tmp/dimensao_localidades_SP.csv', index=False, encoding = 'utf-8', sep= ';')
        return '/tmp/dimensao_localidades_SP.csv'

    @task
    def fazendo_upload_no_s3(file):
        print(f'Got filename: {file}')
        aws_access_key_id = Variable.get("aws_access_key_id")
        aws_secret_access_key = Variable.get("aws_secret_access_key")

        s3_client = boto3.client('s3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key )
        s3_client.upload_file(file,"vini-datalake-127012818163",file[5:])

    @task
    def dados_no_postgres(csv_file_path):
        import pandas as pd
        aws_postgres_password = Variable.get("aws_postgres_password")
        conn = create_engine(
            f'postgresql://postgres:{aws_postgres_password}@vini-database-teste-airflow.c3fuuzuq3h7j.us-east-1.rds.amazonaws.com:5432/viniairflowdb')
        df = pd.read_csv(csv_file_path, sep = ';')
        if csv_file_path == "/tmp/pnadc20203.csv":
            df = df.loc[(df.idade >= 20) & (df.idade <= 40) & (df.sexo == 'Mulher')]
        df['dt_inclusao_registro'] = datetime.today()
        df.to_sql(csv_file_path[5:-4], conn, index = False, if_exists = 'replace', 
                  method ='multi', chunksize = 1000)
        
    mongo = extracao_mongo()
    api = extracao_api()
    upload_mongo = fazendo_upload_no_s3(mongo)
    upload_api = fazendo_upload_no_s3 (api)
    dados_mongo = dados_no_postgres(mongo)
    dados_api = dados_no_postgres(api)

etl = etl()

        
        


    