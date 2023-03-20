from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def hello():
	return {'Hello': "World"}


@app.post('/')
def hello_post():
	return {'Success': "You posted"}


@app.get('/something')
def something():
	return {'Data': "something"}

