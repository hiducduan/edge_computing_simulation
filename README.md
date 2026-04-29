# Edge Computing Simulation

Dự án mô phỏng môi trường tính toán biên (Edge Computing), tập trung vào việc tối ưu hóa việc đẩy tác vụ (task offloading) từ các thiết bị đầu cuối lên các nút cạnh.

## 📌 Tính năng chính
* Mô phỏng thực thi tác vụ trên các thực thể (Entities) khác nhau.
* Triển khai thuật toán offloading.
* Trực quan hóa kết quả thông qua biểu đồ (Matplotlib).
* Tùy chỉnh cấu hình hệ thống dễ dàng qua file `config.py`.

## 📂 Cấu trúc thư mục
* `main.py`: File chạy chính của chương trình.
* `simulator.py`: Bộ điều phối và quản lý vòng đời mô phỏng.
* `entities.py`: Định nghĩa các thành phần như Edge Node, End Device.
* `offloading.py`: Logic xử lý việc đẩy tác vụ.
* `task_generator.py`: Tạo các tác vụ ngẫu nhiên dựa trên cấu hình.
* `greedy_policy.py`: Thuật toán chọn nút cạnh tối ưu.
