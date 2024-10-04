# 要运行 API 服务器，可以使用以下命令：python api/main.py


from fastapi import FastAPI, HTTPException
from modules import inventory_management, financial_management, project_management, user_management

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Laboratory Management System API"}

@app.get("/inventory")
async def get_inventory():
    return inventory_management.get_all_items()

@app.get("/financial-summary")
async def get_financial_summary():
    return financial_management.get_financial_summary()

@app.get("/projects")
async def get_projects():
    return project_management.get_all_projects()

@app.get("/user-activity")
async def get_user_activity():
    return user_management.get_user_activity()

# 可以根据需要添加更多的 API 端点

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
