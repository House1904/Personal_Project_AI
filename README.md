# **🔢 8-Puzzle Solver using AI Search Algorithms**

![Demo Giao Diện](assets/Game_GUI.png)

---

## **Mô tả về dự án**

Dự án này triển khai giải pháp cho bài toán 8-Puzzle cổ điển bằng nhiều thuật toán tìm kiếm AI khác nhau. 8-Puzzle là trò chơi giải đố trượt, trong đó mục tiêu là sắp xếp lại các ô để tạo thành một chuỗi đã sắp xếp. Trò chơi được biểu diễn dưới dạng lưới 3x3, thiếu một ô (được biểu diễn bằng một khoảng trống).

Người giải sẽ lấy cấu hình ban đầu của câu đố và cố gắng đạt đến trạng thái mục tiêu (thường là: `1 2 3 4 5 6 7 8 0`, trong đó `0` là ô trống) bằng cách áp dụng nhiều chiến lược tìm kiếm khác nhau. Dự án bao gồm giao diện đồ họa để trực quan hóa từng bước của quá trình giải và bảng kết quả để so sánh hiệu suất của các thuật toán.

---

## **Các thuật toán tìm kiếm AI được triển khai**

### **Uninformed Search Algorithms:**

- **BFS (Breadth-First Search)**: Tìm kiếm theo chiều rộng,

- **DFS (Depth-First Search)**: Tìm kiếm theo chiều sâu,

- **UCS (Uniform Cost Search)**: Tìm kiếm có chi phí,

- **IDS (Iterative Deepening Search)**: Tìm kiếm sâu dần.

### **Informed Search Algorithms:**

- **Greedy Best-First Search**: Tìm kiếm dựa trên heuristics,

- **A\* Search**: Tìm kiếm có chi phí và heuristics.

- **IDA\* Search**: Tìm kiếm sâu dần và có chi phí.

### **Local Search Algorithms:**

- **Simple Hill Climbing**: Tìm kiếm bằng cách di chuyển đến vị trí tốt hơn.

- **Steepest Ascent Hill Climbing**: Tìm kiếm bằng cách di chuyển đến vị trí tốt nhất.

- **Stochastic Hill Climbing**: Tìm kiếm bằng cách di chuyển đến vị trí tốt hơn với xác suất.

- **Simulated Annealing**: Tìm kiếm bằng cách di chuyển đến vị trí tốt hơn với xác suất giảm dần.

- **Genetic Algorithm**: Tìm kiếm bằng cách di chuyển đến vị trí tốt hơn thông qua quá trình chọn lọc và lai ghép.

- **Beam Local Search**: Tìm kiếm bằng cách chọn các giải pháp tốt nhất trong một số lượng giới hạn.

### **And-Or Graph Search Algorithm**

### **Belief Propagation Algorithms:**

- **Belief-BFS**: Tìm kiếm theo chiều rộng trong môi trường niềm tin.

- **Belief-DFS**: Tìm kiếm theo chiều sâu trong môi trường niềm tin.

- **Belief-Greedy**: Tìm kiếm dựa trên heuristics trong môi trường niềm tin.

### **Backtracking Algorithm**

---

## **Demo chương trình**

![Demo](assets/Demo.gif)

---

## **Yêu cầu**

Để chạy được chương trình 8-Puzzle Solver, bạn cần chuẩn bị các yêu cầu sau:

- **Python 3.x**: Cài đặt Python 3.x trên máy tính của bạn.

- **Pygame**: Cài đặt Pygame để chạy chương trình.

---

## **Cách sử dụng**

**1. Tải mã nguồn:** Clone dự án từ GitHub về máy.

```
git clone https://github.com/House1904/Personal_Project_AI.git
cd Personal_Project_AI
```

**2. Cài đặt thư viện cần thiết**

**3. Chạy chương trình**

```
python main.py
```

**4. Tùy chọn thuật toán**

Sử dụng giao diện để:

- Nhập trạng thái ban đầu và trạng thái mục tiêu trong main.py (Đã có sẵn, bạn có thể sửa đổi tuỳ theo input của mình)

```
start_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]] # Trạng thái ban đầu
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]] # Trạng thái mục tiêu
```

- Chọn thuật toán mong muốn (BFS, DFS, A\*, v.v.)

- Quan sát quá trình giải và so sánh kết quả (thời gian, bước đi, số node mở rộng)

**5. Quan sát kết quả và chọn tiếp thuật toán khác**

- Animation sẽ được hiển thị trên màn hình sau khi chọn thuật toán.

- Ma trận từng bước giải sẽ được in ra console.

- Bảng Details hiển thị thời gian, bước đi, số node mở rộng cho từng thuật toán.

- Trong lúc Animation đang chạy, bạn có thể dừng, chạy tiếp hoặc xem bước trước và bước sau bằng các nút tương ứng. Sau khi Animation kết thúc, bạn Reset lại chương trình để chạy lại thuật toán khác.

---

## **Giấy phép và Bản quyền**

Dự án này được cấp phép theo giấy phép [MIT License](LICENSE).

Bạn có thể sử dụng, sửa đổi và phân phối phần mềm này cho bất kỳ mục đích cá nhân hoặc thương mại nào, miễn là bạn giữ nguyên thông tin bản quyền và điều khoản giấy phép gốc.

---

## **Tác giả**

- Lê Vũ Hào

- MSSV: 23133020

- Trường: Đai học Sư phạm Kỹ thuật Thành phố Hồ Chí Minh

- Môn học: Trí tuệ nhân tạo (Artificial Intelligence)
