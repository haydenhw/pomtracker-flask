import json
from project.tasks.schemas import task_schema, task_list_schema

with open('project/tests/post_project_request_body.json') as f:
  project = json.load(f)

def test_load_tasks():
  tasks = project['tasks']
  tasks[0]['project_id'] = 1
  tasks[1]['project_id'] = 2
  tasks_json = json.dumps(tasks)
  result = task_list_schema.loads(tasks_json)
  assert len(result) == 2

def test_load_task():
  tasks = project['tasks']
  task = tasks[0]
  task['project_id'] = 1
  task_json = json.dumps(task)
  task_loaded = task_schema.loads(task_json)
  assert task_loaded['task_name'] == task['task_name']