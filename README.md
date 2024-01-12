# FASTAPI_TASK_MANAGER_RENDER

Example of CRUD for a task manager using :
- `FastAPI`
- `SQL ALchemy` for database
- `logger` 
- `ratelimit`

The `RateLimit` is using `slowapi` package that allows to set a number of request for each end point.
Example:

```commandline
@router.get("/")
@limiter.limit("10/minute")
async def read_all_items(request: Request, db: Session = Depends(get_db)) -> list[Item]:
    try:
        db_items = read_db_items(db)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
    return [Item(**db_item.__dict__) for db_item in db_items]
```

# References
- `youtube`: https://www.youtube.com/watch?v=XlnmN4BfCxw
- `github`: https://github.com/ArjanCodes/examples/tree/main/2023/fastapi-router
