# 🦾 SEAL Hackathon Fall 2025 – Team ca_nhan_2 (TheWings)

## 🎯 Giới thiệu

**SEAL Hackathon Fall 2025** là cuộc thi học thuật dành cho sinh viên CNTT, với chủ đề:

> **AI Agents for Software Development Life Cycle (SDLC)**

Mục tiêu: Tạo ra ứng dụng AI hỗ trợ một hoặc nhiều giai đoạn trong vòng đời phát triển phần mềm, thúc đẩy năng lực sáng tạo và khả năng làm việc nhóm.

---

## 🧩 Thông tin đội

| Mục                   | Thông tin                                                               |
| --------------------- | ----------------------------------------------------------------------- |
| **Tên đội**           | ca_nhan_2 *(TheWings)*                                                  |
| **Thành viên**        | 3–5 sinh viên                                                           |
| **Track thi đấu**     | Track 2 – *Code Generation & Review App*                                |
| **Chủ đề**            | AI Reviewer – Multi-Agent System for Code Generation & Review           |
| **Công nghệ sử dụng** | Google ADK (Python), Gemini 2.5 Pro, Streamlit, FastAPI, GitHub Actions |

---

## 🧠 Cấu trúc sản phẩm

| Thành phần                 | Mô tả                                                                        |
| -------------------------- | ---------------------------------------------------------------------------- |
| **Backend (FastAPI)**      | Nhận webhook GitHub, xử lý dữ liệu Pull Request và gọi Gemini 2.5 Pro.       |
| **AI Agents**              | Reviewer, Generator, Tester phối hợp trong vòng lặp review & cải thiện code. |
| **Frontend (Streamlit)**   | Dashboard hiển thị quá trình review và kết quả.                              |
| **CI/CD (GitHub Actions)** | Tự động chạy review khi có PR mới.                                           |
| **Config (policy.yaml)**   | Bộ luật và tiêu chuẩn đánh giá code (style, security, readability...).       |

---

## 🗓️ Lịch trình chính

| Thời gian        | Nội dung                                                 |
| ---------------- | -------------------------------------------------------- |
| **1–19/10/2025** | Đăng ký đội thi                                          |
| **29/10/2025**   | Workshop: *Unleashing AI Agents in Software Engineering* |
| **01/11/2025**   | Khai mạc, chọn track, bốc thăm chủ đề                    |
| **02/11/2025**   | Coding, trình bày và chấm điểm                           |

---

## 👥 Thành viên đội (dự kiến)

| Tên          | Vai trò      | Nhiệm vụ                                      |
| ------------ | ------------ | --------------------------------------------- |
| Thành viên 1 | Team Leader  | Quản lý repo, CI/CD, phối hợp các module      |
| Thành viên 2 | AI Engineer  | Xây dựng multi-agent flow với Google ADK      |
| Thành viên 3 | Backend Dev  | Phát triển FastAPI webhook & xử lý dữ liệu PR |
| Thành viên 4 | Frontend Dev | Thiết kế và phát triển Streamlit Dashboard    |
| Thành viên 5 | Presenter    | Chuẩn bị slide và trình bày demo              |

---

## 🧮 Tiêu chí trọng tâm

* **Tính ứng dụng và khả thi**
* **Tích hợp AI và tự động hóa quy trình review**
* **Giao diện và trải nghiệm người dùng**
* **Mức độ sáng tạo & tính đột phá**

---

## 💡 Định hướng phát triển

* **Tối ưu workflow giữa các AI Agent (Reviewer → Generator → Tester).**
* **Tự động phản hồi Pull Request và tạo report trực quan.**
* **Hỗ trợ cấu hình chính sách review riêng cho từng repo (policy-based).**

---

## 📫 Ghi chú

* **Trường:** FPT University HCM
* **Cuộc thi:** SEAL Hackathon Fall 2025
