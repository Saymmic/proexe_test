# Proexe Dynamic Tables notes

Hello whomever you are :) \
There are two branches:\
`clean_architecture` I designed the solution using clean architecture and ports and adapters pattern with the exception that instead implement mappers for business entities I relay on Protocol abstractions of django models which then pass them directly ommiting the step of mapping. Anyways it relays on on abstraction so it not depends on anything django related so its clean.\
The advantages of this solution is that it is easy to switch database underneath or even the django framework itself.\

`the_django_way` The complete solution according to fat models ideology promoted by django docs and *Two scoops of django* book. **++Important note on updating model, due to limited time I had I decided to simplify the update table process by deleting the old model with all data and create a new one++**. I can implement the complete solution if you need me to do so or discuss it live further. \
The obvious disadvantage of this solution is that business logic is in models which tightly couple us with django and Postgres.

There is also quite popular and battle tested hacksoftware way [link](https://github.com/HackSoftware/Django-Styleguide). I also was implementing and using this approach. it separates more business logic from models not putting everything there or managers. I can reimplement solution if needed.


To run project just type:

```plain
docker compose -f local.yml build
docker compose -f local.yml up
docker compose -f local.yml run --rm django python manage.py migrate
docker compose -f local.yml run --rm django python manage.py createsuperuser
```

Then create token to use in the api.

Create table payload:

<http://localhost:8000/api/table/>

```json
{
    "name": "test_table",
    "fields": [
        {
            "name": "test_string",
            "type": "STRING"
        },
        {
            "name": "test_number",
            "type": "NUMBER"
        },
        {
            "name": "test_bool",
            "type": "BOOLEAN"
        }
    ],
    "description": "test_description"
}
```

Update table:

<http://localhost:8000/api/table/><uuid>/

```json
{
    "name": "another_test_table",
    "fields": [
        {
            "name": "another_test_string",
            "type": "STRING"
        },
        {
            "name": "another_test_number",
            "type": "NUMBER"
        },
        {
            "name": "another_test_bool",
            "type": "BOOLEAN"
        }
    ],
    "description": "test_description"
}
```

Create table data payload:

<http://localhost:8000/api/table/><uuid>/row/

```json
{
    "test_string": "test",
    "test_number": 1,
    "test_boolean": true
}
```

Retrive table data:

<http://localhost:8000/api/table/><uuid>/rows/


