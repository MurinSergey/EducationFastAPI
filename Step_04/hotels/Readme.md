## Создаем первые ручки FastAPI
* app.get
* app.delete
* app.post
* app.put
* app.patch

### app.get
Позволяет делать запросы к серверу с параметрами или без.
Данный метод используется для получения данных, т.е. для отправки запросов.

    id: int | None = Query(description="Номер отеля", default=None),
    title: str | None = Query(description="Название отеля", default=None)

Такой синтаксис позволяет определить параметры запроса GET как не обязательные.