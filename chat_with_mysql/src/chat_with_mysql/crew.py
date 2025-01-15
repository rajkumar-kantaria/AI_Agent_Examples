from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from tools.mysql_tool import SQLQueryTool

@CrewBase
class ChatWithMysql():
	"""ChatWithMysql crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def prepare_sql_query(self) -> Agent:
		llm = LLM(model="groq/llama-3.3-70b-versatile")

		return Agent(
			config=self.agents_config['prepare_sql_query'],
			llm=llm,
			verbose=True
		)

	@task
	def prepare_sql_query_task(self) -> Task:
		return Task(
			config=self.tasks_config['prepare_sql_query_task'],
		)
	
	@task
	def execute_sql_query_task(self) -> Task:
		mysql_tool = SQLQueryTool()
		return Task(
			config=self.tasks_config['execute_sql_query_task'],
			tools=[mysql_tool],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ChatWithMysql crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
