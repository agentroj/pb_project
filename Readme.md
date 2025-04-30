# Roj’s CSV-Backed Video API

## Quickstart

1. **Clone & env**  
   ```bash
   git clone … && cd myproject
   echo "DJANGO_SECRET_KEY=…\nDEBUG=1" > .env
   ```

## Build & Run

```bash
docker-compose up --build
```

## Open

- **API root:** `http://localhost:8000/videos/`
- **Swagger UI:** `http://localhost:8000/swagger/`
- **OpenAPI schema:** `http://localhost:8000/doc/`

## Sample CSV

Located at `videos.csv`—you can edit or replace with your own tab-delimited file.

## Endpoints

| Method | Path            | Description                                       |
| ------ | --------------- | ------------------------------------------------- |
| GET    | `/videos/`      | List all records (supports `?sort_by=…&order=…`)  |
| POST   | `/videos/`      | Add a new record                                  |
| PUT    | `/videos/{id}/` | Update a record by `source_post_id`               |
| DELETE | `/videos/{id}/` | Delete a record by `source_post_id`               |

## Fields

- `source_post_id` (string, pk)  
- `post_url` (URL)  
- `post_description` (string)  
- `post_created` (MM/DD/YY)  
- `likes_count`, `shares_count`, `views_count`, `comments_count` (integers)  

## Tests

```bash
pytest
```

