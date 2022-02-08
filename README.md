# Quiz BE

This application is a backend for a simple quiz application, where users (creators) can create their own quiz and invite other people (participants) via email to participate in the quiz. It is possible to creators set a limit of time per question and/or a datetime limit for the whole quiz.It is written in python and using the django framework.

## How to run

You can run the application with docker or with the traditional django way. But before that, you have to create a ```.env``` file with some environment variables. You can check the template example on the ```.env_template```file.

### Docker
1. With docker, you just need to run the following command:

```bash
docker-compose up --build
```

### Django
1. With the traditional django way, first you need to install the requirements:

```bash
pip install -r requirements.txt
```

2. After that, make sure you have [Redis](https://redis.io/) installed, up and running.
3. Run migrations:

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
4. Run Celery:
```bash
celery -A quiz worker -l info
```
5. Finally, run the application:
```bash
python manage.py runserver
```

## Endpoints

### Login
**You send:**  Your login credentials.
**You get:** An `API-Token` with wich you can make further actions.

**Request:**
```json
POST api/login

{
    "email": "admin@email.com",
    "password": "password" 
}
```
**Successful Response:**
```json
Status: 200 OK
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZGQ4ZDI4ODgtODFlMS00YmVlLWJjM2QtYzdiYzRkN2IzM2ZkIiwidXNlcm5hbWUiOiJwYXJ0aWNpcGFudEBlbWFpbC5jb20iLCJleHAiOjE2NDQ2MDg1MzAsImVtYWlsIjoicGFydGljaXBhbnRAZW1haWwuY29tIn0.-WSioHECQEqkm9D2aISDG4RvZvZFiYzNFcY22MWCAxc",
    "user": {
        "id": "dd8d2888-81e1-4bee-bc3d-c7bc4d7b33fd",
        "email": "admin@email.com",
        "first_name": "Admin",
        "last_name": "Admin",
        "is_admin": true,
        "date_joined": "2022-02-07T15:41:49.798584"
    }
}
```
**Failed Response:**
```json
Status: 400 Bad Request
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}
``` 

### Register
This endpoint is to create a new account, so the user can create quizzes and invite participants.

**Request:**
```json
POST api/register

{
    "email": "creator@email.com",
    "first_name": "Creator",
    "last_name": "One"
}
```
**Successful Response:**
```json
Status: 201 Created
{
    "id": "1e87af34-5ffc-49f2-a75a-8986060a1a47",
    "email": "creator@email.com",
    "first_name": "Creator",
    "last_name": "One"
    "date_joined": "2022-02-03T15:41:11.972231Z"
}
```
**Failed Response:**
```json
Status: 400 Bad Request
{
    "email": [
        "This field is required."
    ],
    "first_name": [
        "This field is required."
    ],
    "last_name": [
        "This field is required."
    ]
}
``` 

### User confirmation
This endpoint is to confirm the created account on **Register** endpoint and define the password. You can get the ```token_confirmation``` in the user email

**Request:**
```json
PUT api/users/confirmation?token_confirmation=X

{
    "password": "password"
}
```
**Successful Response:**
```json
Status: 201 Created
{
    "id": "1e87af34-5ffc-49f2-a75a-8986060a1a47",
    "email": "creator@email.com",
    "first_name": "Creator",
    "last_name": "One"
    "date_joined": "2022-02-03T15:41:11.972231Z"
}
```
**Failed Response:**
```json
Status: 400 Bad Request
{
    "password": [
        "This field is required."
    ]
}
``` 
The next endpoints need a ```Authorization: Bearer X``` header.

### Quizzes
The following endpoints are the CRUD for the quizzes. Only the creator (and the admin) can use this endpoints to its own quizzes.

### List Quizzes
On list quizzes you can also add the parameters ```name``` and ```id``` to filter the results and ```page``` and ```limit``` for pagination.

**Request:**
```json
GET api/quizzes
```
**Successful Response:**
```json
Status: 200 OK
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "aefd7296-3b49-49c1-8ab1-523453cea7b0",
            "name": "quiz one",
            "description": "a description related to the quiz",
            "question_time_limit": null,
            "datetime_limit": null
        }
    ]
}
```
**Failed Response:**
```json
Status: 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```

### Create Quizzes
This endpoint is for creating a quiz. The body parameters ```question_time_limit``` and ```datetime_limit``` are optional. The first one is the time that a participant have to answer each question and the second one is the datetime limit to answer the quiz.

**Request:**
```json
POST api/quizzes

{
    "name": "quiz 2",
    "description": "example of a description!",
    "question_time_limit": 50
}
```
**Successful Response:**
```json
Status: 201 Created
{
    "id": "aefd7296-3b49-49c1-8ab1-523453cea7b0",
    "name": "quiz 2",
    "description": "example of a description!",
    "question_time_limit": 50,
    "datetime_limit": null
}
```
**Failed Response:**
```json
Status: 400 Bad Request
{
    "name": [
        "This field is required."
    ],
    "description": [
        "This field is required."
    ]
}
``` 

### Retrieve Quizzes
This endpoint is to retrieve a quiz

**Request:**
```json
GET api/quizzes/:id

```
**Successful Response:**
```json
Status: 200 OK
{
    "id": "aefd7296-3b49-49c1-8ab1-523453cea7b0",
    "name": "quiz 2",
    "description": "example of a description!",
    "question_time_limit": 50,
    "datetime_limit": null
}
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "detail": "Not found."
}
``` 

### Update Quizzes
This endpoint is to update a quiz (```PUT``` to update all the fields and ```PATCH``` to update the selected fields).

**Request:**
```json
PUT/PATCH api/quizzes/:id

```
**Successful Response:**
```json
Status: 200 OK
{
    "id": "aefd7296-3b49-49c1-8ab1-523453cea7b0",
    "name": "quiz 2",
    "description": "example of a description!",
    "question_time_limit": 50,
    "datetime_limit": null
}
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "detail": "Not found."
}
``` 

### Delete Quizzes
This endpoint is to delete a quiz.

**Request:**
```json
DELETE api/quizzes/:id

```
**Successful Response:**
```json
Status: 204 No Content
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "detail": "Not found."
}
```

### Questions
The following endpoints are the CRUD for the quizzes' questions. Only the creator (and the admin) can use this endpoints to its own quizzes' questions.

### List Questions
On list questions you can also add the parameters ```question``` to filter the results and ```page``` and ```limit``` for pagination.

**Request:**
```json
GET api/quizzes/:id/questions
```
**Successful Response:**
```json
Status: 200 OK
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "75e11b8c-95df-466a-b340-a8ac1c5dfe1c",
            "question": "question one",
            "created_at": "2022-02-08T11:32:53.077897",
            "answers": [
                {
                    "id": "4d8a5d3f-0fed-4b50-8ede-1c33bd722706",
                    "answer": "answer 1",
                    "is_correct": true
                },
                {
                    "id": "f06891a4-afc2-4da4-9347-59a332b6ea1c",
                    "answer": "answer 1",
                    "is_correct": false
                }
            ]
        }
    ]
}
```
**Failed Response:**
```json
Status: 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```

### Create Questions
This endpoint is to create new questions for the given quiz.

**Request:**
```json
POST api/quizzes/:id/questions
{
    "question": "Question 2"
}
```
**Successful Response:**
```json
Status: 201 Created
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "75e11b8c-95df-466a-b340-a8ac1c5dfe1c",
            "question": "question one",
            "created_at": "2022-02-08T11:32:53.077897",
            "answers": []
        }
    ]
}
```
**Failed Response:**
```json
Status: 400 Bad Request
{
    "question": [
        "This field is required."
    ]
}
```

### Retrieve Questions
This endpoint is to retrieve a question from a given quiz.

**Request:**
```json
GET api/quizzes/:quiz_id/questions/:question_id
```
**Successful Response:**
```json
Status: 200 OK
{
    "id": "75e11b8c-95df-466a-b340-a8ac1c5dfe1c",
    "question": "question one",
    "created_at": "2022-02-08T11:32:53.077897",
    "answers": []
}
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "detail": "Not found."
}
```

### Update Questions
This endpoint is to update a question from a given quiz.

**Request:**
```json
PUT/PATCH api/quizzes/:quiz_id/questions/:question_id
{
    "question": "question one",
}
```
**Successful Response:**
```json
Status: 200 OK
{
    "id": "75e11b8c-95df-466a-b340-a8ac1c5dfe1c",
    "question": "question oneee",
    "created_at": "2022-02-08T11:32:53.077897",
    "answers": []
}
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "detail": "Not found."
}
```

### Delete Questions
This endpoint is to delete a question from a given quiz.

**Request:**
```json
DELETE api/quizzes/:quiz_id/questions/:question_id
```
**Successful Response:**
```json
Status: 204 No Content
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "detail": "Not found."
}
```

### Answers
The following endpoints are the CRUD for the questions' answers. Only the creator (and the admin) can use this endpoints to its own questions' answers.

### List Answers
On list questions you can also add the parameters ```answer``` to filter the results and ```page``` and ```limit``` for pagination.

**Request:**
```json
GET api/quizzes/:quiz_id/questions/:question_id/answers
```
**Successful Response:**
```json
Status: 200 OK
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "4d8a5d3f-0fed-4b50-8ede-1c33bd722706",
            "answer": "answer 1",
            "is_correct": true
        },
        {
            "id": "f06891a4-afc2-4da4-9347-59a332b6ea1c",
            "answer": "answer 1",
            "is_correct": false
        }
    ]
}
```
**Failed Response:**
```json
Status: 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```

### Create Answers
This endpoint is to create new answers for the given question.

**Request:**
```json
POST api/quizzes/:quiz_id/questions/:question_id/answers
{
    "answer": "Answer 3",
    "is_correct": false
}
```
**Successful Response:**
```json
Status: 201 Created
{
    "id": "07478a50-66d1-430c-919a-54b009dfe6cc",
    "answer": "Answer 3",
    "is_correct": false
}
```
**Failed Response:**
```json
Status: 400 Bad Request
{
    "answer": [
        "This field is required."
    ]
}
```

### Retrieve Answers
This endpoint is to retrieve an answer from a given question.

**Request:**
```json
GET api/quizzes/:quiz_id/questions/:question_id/answers/:answer_id
```
**Successful Response:**
```json
Status: 200 OK
{
    "id": "07478a50-66d1-430c-919a-54b009dfe6cc",
    "answer": "Answer 3",
    "is_correct": false
}
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "detail": "Not found."
}
```

### Update Questions
This endpoint is to update an answer from a given question.

**Request:**
```json
PUT/PATCH api/quizzes/:quiz_id/questions/:question_id
{
    "answer": "Answer 4",
    "is_correct": false
}
```
**Successful Response:**
```json
Status: 200 OK
{
    "id": "07478a50-66d1-430c-919a-54b009dfe6cc",
    "answer": "Answer 4",
    "is_correct": false
}
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "detail": "Not found."
}
```

### Delete Answer
This endpoint is to delete an answer from a given question.

**Request:**
```json
DELETE api/quizzes/:quiz_id/questions/:question_id/answers/:answer_id
```
**Successful Response:**
```json
Status: 204 No Content
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "detail": "Not found."
}
```

### Participants
The following endpoints are for list, create and remove participants from a given quiz. Only the creator (and the admin) can use this endpoints to its own quizzes.

### List Participants
On list questions you can also add the parameters ```id```, ```user__email```, ```user__first_name``` and ```user__last_name``` to filter the results and ```page``` and ```limit``` for pagination.

**Request:**
```json
GET api/quizzes/:quiz_id/participants
```
**Successful Response:**
```json
Status: 200 OK
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "ce87313e-0733-4afa-a335-2011ca824870",
            "user": {
                "id": "7c20d456-a277-485f-afe8-3693f56c9703",
                "email": "participant@email.com",
                "first_name": "Participant",
                "last_name": "one"
            }
        }
    ]
}
```
**Failed Response:**
```json
Status: 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```

### Create Participant
This endpoint is to add a new participant to the given quiz. If the user invited has not an account yet, an invite will be sent via email to confirm the user password along with the invitation for the quiz.

**Request:**
```json
POST api/quizzes/:quiz_id/participants
{
    "email": "participant2@email.com",
    "first_name": "Participant",
    "last_name": "Two"
}
```
**Successful Response:**
```json
Status: 201 Created
{
    "id": "126fafa3-2870-4e8d-b2e2-9c85ea6409a3",
    "user": {
        "id": "6cd157c3-cee6-4bd0-b0a6-57120a247e19",
        "email": "participant2@email.com",
        "first_name": "Participant",
        "last_name": "Two"
    }
}
```
**Failed Response:**
```json
Status: 400 Bad Request
{
    "email": [
        "This field is required."
    ]
}
```

### Delete Participants
This endpoint is to delete a participant from a given quiz.

**Request:**
```json
DELETE api/quizzes/:quiz_id/participants/:participant_id
```
**Successful Response:**
```json
Status: 204 No Content
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "detail": "Not found."
}
```

### Quiz Status
This endpoint provides some information about the progress of the quiz. Only the creator (and the admin) can use this endpoint to its own quizzes.

**Request:**
```json
GET api/quizzes/:quiz_id/status
```
**Successful Response:**
```json
Status: 200 OK
{
    "datetime_limit": 2022-02-10 10:02:14,
    "time_left": 2320,
    "progress_total_questions_answered": 0.0
}
```
**Failed Response:**
```json
Status: 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```

### Quiz Results
This endpoint provides the result, in percentage, of the participants of the given quiz. Only the creator (and the admin) can use this endpoint to its own quizzes.

**Request:**
```json
GET api/quizzes/:quiz_id/results
```
**Successful Response:**
```json
Status: 200 OK
{
    "participants": [
        {
            "id": "7c20d456-a277-485f-afe8-3693f56c9703",
            "email": "participant@email.com",
            "first_name": "Participant",
            "last_name": "one",
            "result": 60.0
        }
    ]
}
```
**Failed Response:**
```json
Status: 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```

### Notify Quiz Results
This endpoint notifies the participants of the quiz, via email, the results, in percentage. Only the creator (and the admin) can use this endpoint to its own quizzes.

**Request:**
```json
GET api/quizzes/:quiz_id/results/notify
```
**Successful Response:**
```json
Status: 200 OK
{
    "results": "results were sent successfully via email"
}
```
**Failed Response:**
```json
Status: 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```

### Participant Quizzes
This endpoint lists the quizzes that the user can answer. Only the participant can use this endpoint to the quizzes that was invited to.

**Request:**
```json
GET api/participant/quizzes
```
**Successful Response:**
```json
Status: 200 OK
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "aefd7296-3b49-49c1-8ab1-523453cea7b0",
            "name": "quiz 2",
            "description": "example of description!",
            "question_time_limit": 50,
            "datetime_limit": null
        }
    ]
}
```
**Failed Response:**
```json
Status: 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```

### Retrieve Participant Quizzes
This endpoint retrieve the quizzes that the user can answer. It retrieves information about the quiz and also the id's of the questions, so the user can answer them. Only the participant can use this endpoint to the quizzes that was invited to.

**Request:**
```json
GET api/participant/quizzes/:id
```
**Successful Response:**
```json
Status: 200 OK
{
    "id": "aefd7296-3b49-49c1-8ab1-523453cea7b0",
    "name": "quiz 2",
    "description": "example of description!",
    "question_time_limit": 50,
    "datetime_limit": null,
    "questions": [
        "75e11b8c-95df-466a-b340-a8ac1c5dfe1c",
        "daeffd66-ef0b-4d9c-8144-a6ddba61a729"
    ]
}
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "errors": [
        "quiz not found"
    ]
}
```

### Retrieve Participant Quizzes Questions
This endpoint retrieve the quizzes that the user can answer. It retrieves information about the quiz and also the id's of the questions, so the user can answer them. Only the participant can use this endpoint to the quizzes that was invited to.

**Request:**
```json
GET api/participant/quizzes/:quiz_id/questions/:question_id
```
**Successful Response:**
```json
Status: 200 OK
{
    "id": "75e11b8c-95df-466a-b340-a8ac1c5dfe1c",
    "question": "question one",
    "answers": [
        {
            "id": "4d8a5d3f-0fed-4b50-8ede-1c33bd722706",
            "answer": "answer 1"
        },
        {
            "id": "f06891a4-afc2-4da4-9347-59a332b6ea1c",
            "answer": "answer 2"
        }
    ]
}
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "detail": "Not found."
}
```

### Create Participant Quizzes Answer
This endpoint is for the participant to answer a question of a given quiz. Only the participant can use this endpoint to the quizzes that was invited to.

**Request:**
```json
POST api/participant/quizzes/:quiz_id/questions/:question_id/answers
```
**Successful Response:**
```json
Status: 201 Created
{
    "answer": "answer sent successfully"
}
```
**Failed Response:**
```json
Status: 400 Bad Request
{
    "answer_id": [
        "This field is required."
    ]
}
```

### Participant Quizzes Status
This endpoint retrieves some information about the status of a given quiz. Only the participant can use this endpoint to the quizzes that was invited to.

**Request:**
```json
GET api/participant/quizzes/:quiz_id/status
```
**Successful Response:**
```json
Status: 200 OK
{
    "datetime_limit": null,
    "time_left": null,
    "questions_answered": 1,
    "questions_left": 1
}
```
**Failed Response:**
```json
Status: 404 Not Found
{
    "errors": [
        "quiz not found"
    ]
}
```

### Admin Quizzes Reports
This endpoint retrieves a report with some information about the results of the quizzes created on the current day. Only the admin can use this endpoint.

**Request:**
```json
GET api/admin/reports
```
**Successful Response:**
```json
Status: 200 OK
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "aefd7296-3b49-49c1-8ab1-523453cea7b0",
            "name": "quiz 2",
            "description": "example of description!",
            "participants": [
                {
                    "id": "7c20d456-a277-485f-afe8-3693f56c9703",
                    "email": "participant@email.com",
                    "first_name": "Participant",
                    "last_name": "one",
                    "result": 50.0
                }
            ]
        }
    ]
}
```
**Failed Response:**
```json
Status: 403 Forbidden
{
    "errors": [
        "Only admin users have access to this endpoint"
    ]
}
```

### Admin Quizzes Reports (CSV)
This endpoint retrieves a report, in csv format, with some information about the results of the quizzes created on the current day. Only the admin can use this endpoint.

**Request:**
```json
GET api/admin/reports
```
**Successful Response:**
```json
Status: 200 OK
id,name,description,participant_email,participant_first_name,participant_last_name,participant_result
b62db041-3ae7-4fcd-be61-c74badf90d02,quiz 2,example of description!,,,,
aefd7296-3b49-49c1-8ab1-523453cea7b0,quiz 2,example of description!,participant@email.com,Participant,one,50.0
```
**Failed Response:**
```json
Status: 403 Forbidden
{
    "errors": [
        "Only admin users have access to this endpoint"
    ]
}
```
