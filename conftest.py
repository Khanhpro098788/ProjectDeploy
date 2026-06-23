"""
conftest.py ở project root.

Mục đích:
- Đảm bảo pytest (và type checkers như Pyrefly) nhận ra thư mục gốc
  là import root, tức là `from src.main import app` hoạt động đúng.
- File này không cần nội dung thêm — sự hiện diện của nó đã đủ.
"""
