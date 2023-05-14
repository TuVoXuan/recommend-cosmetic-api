import uvicorn

if __name__ == "__main__":
    try:
        uvicorn.run(
            reload=False,
            app="main:app",
            host='0.0.0.0',
            port=8000,
        )
    except:
        print('Loi khong chay file main')
