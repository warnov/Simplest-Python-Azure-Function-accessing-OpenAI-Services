import azure.functions as func
from openai import OpenAI
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="HelloOpenAI")
def HelloOpenAI(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    prompt = req.params.get('prompt')
    if not prompt:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            prompt = req_body.get('prompt')

    if prompt:
        client=OpenAI()
        completion=client.chat.completions.create(
            model="gpt-3.5-turbo",
             messages=[
                {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role":"user", "content":prompt}]
        )
        return func.HttpResponse(completion.choices[0].message.content)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a prompt in the query string or in the request body for a personalized response.",
             status_code=200
        )