import uvicorn

if __name__ == "__main__":
    try:
        uvicorn.run(
            reload=False,
            app="main:app"
        )
    except:
        print('Loi khong chay file main')
