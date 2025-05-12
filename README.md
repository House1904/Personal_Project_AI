# **🔢 8-Puzzle Solver using AI Search Algorithms**

![Demo Giao Diện](assets/Game_GUI.png)

---

## **Mô tả về dự án**

Dự án này triển khai giải pháp cho bài toán 8-Puzzle cổ điển bằng nhiều thuật toán tìm kiếm AI khác nhau. 8-Puzzle là trò chơi giải đố trượt, trong đó mục tiêu là sắp xếp lại các ô để tạo thành một chuỗi đã sắp xếp. Trò chơi được biểu diễn dưới dạng lưới 3x3, thiếu một ô (được biểu diễn bằng một khoảng trống).

Người giải sẽ lấy cấu hình ban đầu của câu đố và cố gắng đạt đến trạng thái mục tiêu (thường là: `1 2 3 4 5 6 7 8 0`, trong đó `0` là ô trống) bằng cách áp dụng nhiều chiến lược tìm kiếm khác nhau. Dự án bao gồm giao diện đồ họa để trực quan hóa từng bước của quá trình giải và bảng kết quả để so sánh hiệu suất của các thuật toán.

---

## **Mục tiêu**

Mục tiêu của dự án là xây dựng một hệ thống giải bài toán 8-Puzzle bằng các thuật toán Tìm kiếm trong Trí tuệ nhân tạo (AI Search Algorithms). Hệ thống cho phép:

- Tìm lời giải hợp lệ từ trạng thái ban đầu đến trạng thái mục tiêu.

- So sánh hiệu quả của nhiều thuật toán dựa trên các tiêu chí như:

  - Thời gian chạy (Runtime)

  - Số lượng node được mở rộng (Nodes Expanded)

  - Độ sâu lời giải (Search Depth)

  - Số bước trong lời giải (Steps)

---

## **Nội dung**

Dự án mô phỏng trò chơi 8-Puzzle – một bài toán sắp xếp trên lưới 3x3 với một ô trống (0). Mục tiêu là đưa các số từ 1 đến 8 về đúng thứ tự (mặc định là [[1, 2, 3], [4, 5, 6], [7, 8, 0]]) bằng cách di chuyển ô trống.

Dự án bao gồm:

- Giao diện đồ họa bằng Pygame: trực quan hóa trạng thái bắt đầu, trạng thái đích, và quá trình giải theo từng bước.

- Lựa chọn nhiều thuật toán khác nhau từ Uninformed Search, Informed Search, Local Search, Genetic, And-Or Graph Searc, Belief-based Search và cuối cùng là CSP Search.

- Cơ chế điều khiển và hiển thị kết quả chi tiết sau mỗi lần giải.

- Hỗ trợ nhập trạng thái ban đầu (start state) trực tiếp từ giao diện.

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

- **IDA\* Search**: Tìm kiếm sâu dần và có chi phí tương tự A\*.

### **Local Search Algorithms:**

- **Simple Hill Climbing**: Tìm kiếm bằng cách di chuyển đến vị trí tốt hơn.

- **Steepest Ascent Hill Climbing**: Tìm kiếm bằng cách di chuyển đến vị trí tốt nhất.

- **Stochastic Hill Climbing**: Tìm kiếm bằng cách di chuyển đến vị trí tốt hơn với xác suất.

- **Simulated Annealing**: Tìm kiếm bằng cách di chuyển đến vị trí tốt hơn với xác suất giảm dần.

- **Genetic Algorithm**: Tìm kiếm bằng cách di chuyển đến vị trí tốt hơn thông qua quá trình chọn lọc và lai ghép.

- **Beam Local Search**: Tìm kiếm bằng cách chọn các giải pháp tốt nhất trong một số lượng giới hạn.

### **And-Or Graph Search Algorithm**

Thuật toán được dùng trong môi trường có cấu trúc phân nhánh kiểu "AND" và "OR". Mỗi nút OR đại diện cho lựa chọn giữa các hành động, còn nút AND đại diện cho các hành động bắt buộc thực hiện đồng thời. Thuật toán này phù hợp với các bài toán có mục tiêu phụ thuộc nhiều điều kiện, ví dụ như trong môi trường phân rã nhiệm vụ (task decomposition) hoặc điều khiển hệ thống trong môi trường không chắc chắn.

### **Belief Propagation Algorithms:**

- **Belief-BFS**: Tìm kiếm theo chiều rộng trong môi trường niềm tin.

- **Belief-A\***: Tìm kiếm theo chiều sâu trong môi trường niềm tin.

- **Belief-Greedy**: Tìm kiếm dựa trên heuristics trong môi trường niềm tin.

### **CSP Algorithms:**

- **Backtracking Algorithm**: Giải bài toán bằng cách thử từng giá trị cho biến theo thứ tự, kiểm tra ràng buộc sau mỗi bước. Nếu phát hiện xung đột, thuật toán quay lui (backtrack) để thử giá trị khác.

- **Forward Checking Algorithm**: Mở rộng thuật toán backtracking bằng cách, sau mỗi lần gán biến, loại bỏ các giá trị không hợp lệ khỏi miền giá trị của các biến còn lại. Điều này giúp phát hiện sớm mâu thuẫn và giảm đáng kể không gian tìm kiếm.

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

- Nhập trạng thái bắt đầu (Đã có sẵn hoặc bạn có thể nhập tuỳ theo input của mình)

![Input](assets/Input_Start_state.png)

Chú ý nhập đúng định dạng:

- 0: Trống

- Còn lại : Số thứ tự của ô (từ 1 đến 8)

Ví dụ: 410263758

Nhập xong thì nhấn Enter để áp dụng Input mới của bạn.

- Chọn thuật toán mong muốn (BFS, DFS, A\*, v.v.)

- Quan sát quá trình giải và so sánh bằng bảng kết quả.

Ngoài ra, ma trận chi tiết từng bước sẽ in ra console để bạn dễ dàng theo dõi (không in ra giao diện vì quá nhiều).

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

## Các nguồn tham khảo

[8-Puzzle Solver Web App - by AbdElRahman Osama](https://8-puzzle.streamlit.app/)

[eight-puzzle-solver - by Elzawawy](https://github.com/Elzawawy/eight-puzzle-solver)

[8-Puzzle-Solver - by yousefkotp](https://github.com/yousefkotp/8-Puzzle-Solver)

[8-puzzle-solver - by dgurkaynak](https://github.com/dgurkaynak/8-puzzle-solver?tab=readme-ov-file)

## [pynpuzzle - by mahdavipanah](https://github.com/mahdavipanah/pynpuzzle)

## **Tác giả**

- Lê Vũ Hào

- MSSV: 23133020

- Trường: Đai học Sư phạm Kỹ thuật Thành phố Hồ Chí Minh

- Môn học: Trí tuệ nhân tạo (Artificial Intelligence)
