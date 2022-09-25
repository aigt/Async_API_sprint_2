
### Пример запроса с сортировкой, фильтрацией и пагинацией

```
http://0.0.0.0:8000/api/v1/films/?filter[genre]=Fantasy&page[size]=5&page[number]=2&sort=-imdb_rating
```