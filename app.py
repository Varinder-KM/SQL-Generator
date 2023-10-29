from flask import Flask, render_template, request, g
import os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType
import pymysql
import psycopg2
# Import ChatOpenAI if needed in the future
# from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = ''

app = Flask(__name__)

app.config['global_var'] = None

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect_db():
    db_type = request.form.get("db_type") 
    host = request.form['host']
    user = request.form['user']
    password = request.form['password']
    database = request.form['database']
    result = ''

    if db_type == "MySQL":
        # MySQL credentials
        credentials = f'mysql+pymysql://{user}:{password}@{host}/{database}'

        # Connect to the MySQL database
        db = SQLDatabase.from_uri(credentials)

        # Create a ChatOpenAI language model
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")

        # Create an SQLDatabaseToolkit instance
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        # Create an SQL agent
        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True
        )
        app.config['global_var'] = agent_executor


    elif db_type == 'PostgresSQL':
        credentials = f'postgresql+psycopg2://{user}:{password}@{host}/{database}'
        db = SQLDatabase.from_uri(credentials)

        llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True
        )

        app.config['global_var'] = agent_executor

    else:
        db = SQLDatabase.from_uri("sqlite:///static/database/northwind.db")
        toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))
        from langchain.chat_models import ChatOpenAI
        agent_executor = create_sql_agent(
            llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS
        )

        app.config['global_var'] = agent_executor


    
    
    return render_template('query.html', result=result)


@app.route('/query', methods=['GET', 'POST'])
def make_queries():
    result = ''
    if request.method == 'POST':
        query_input = request.form['query']
        if app.config['global_var']  is not None:
            agent_executor = app.config['global_var']
            output = agent_executor.run(query_input)
        
    return render_template('query.html', result=output)
