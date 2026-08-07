@echo off
:: Kích hoạt môi trường ảo (thay 'venv' bằng tên thư mục ảo của bạn nếu khác)
call venv\Scripts\activate

:: Khởi chạy Uvicorn
uvicorn routers.main:app --reload

pause
