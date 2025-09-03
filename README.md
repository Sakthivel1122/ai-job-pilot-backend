# JobPilot.AI – Backend

This is the **backend API** of JobPilot.AI, built using **FastAPI**.  
It powers job application management, resume analysis, authentication, and AI-driven insights using **LangChain**, **Groq**, and **LLMs**.

---

## 🚀 Features

- **Job Application API**
  - CRUD operations for applications
  - Status management (Applied, Interview Scheduled, Offer Received)
  - Job statistics endpoints for insights

- **Resume Analysis API**
  - Upload resumes and analyze using AI  
  - Get intelligent feedback and optimization suggestions  
  - Track feedback history and associate multiple resumes with applications  

- **Authentication API**
  - Secure login/signup with JWT tokens  
  - Protected routes for dashboard access  

- **AI Integration**
  - Orchestrated with **LangChain**  
  - Uses **Groq** and LLMs for fast, accurate responses  
  - Stores data in **MongoDB**

---

## 🛠️ Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)  
- **Database**: [MongoDB](https://www.mongodb.com/)  
- **AI Layer**: [LangChain](https://www.langchain.com/), [Groq](https://groq.com/), LLMs  
- **Authentication**: JWT tokens  
- **Environment Management**: Python `venv` or `pipenv`

---

## 📂 Related Repositories

- **Hub (Project Overview)**: [ai-job-pilot-hub ↗](https://github.com/Sakthivel1122/ai-job-pilot-hub)  
- **Frontend UI**: [ai-job-pilot-frontend ↗](https://github.com/Sakthivel1122/ai-job-pilot-frontend)  
