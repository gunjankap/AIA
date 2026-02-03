🌾 Dr. Crops
Dr. Crops is an AI-powered plant disease detection system designed to help farmers, agricultural experts, and researchers easily identify tomato crop diseases using a combination of machine learning models and real-time environmental insights.

With image-based CNN models and real-time weather-aware predictions, Dr. Crops helps diagnose issues faster, reduce crop losses, and promote healthier yields — all from a simple, intuitive interface.

🚀 Tech Stack
Frontend

Framework: React + TypeScript

Styling: Tailwind CSS

UI Interactions: React Hooks

Backend

Runtime: Node.js

Model Integration: TensorFlow (.h5) and classifier .pkl files

Weather API Integration: AgMarket API

Model Serving: FastAPI

📁 Project Structure

dr-crop/
├── gui/                       # Frontend (React + TypeScript)
│   ├── components/            # UI Components
│   ├── pages/                 # Routes and pages
│   ├── styles/                # Tailwind CSS styling
│   └── utils/                 # Utility functions and constants
│
├── backend/                   # Node.js backend
│   ├── main.py                # API entry point
│   ├── city_module.py         # Weather logic integration
│   ├── tomato_model_finetuned.h5 # CNN model
│   ├── classifier_model.pkl   # Environmental/classifier model
│
└── README.md                  # Project documentation
🧠 Key Features
✅ Tomato Leaf Disease Detection using CNN
🌦️ Weather-Aware Risk Prediction using AgMarket API
📷 Real-Time Image Upload and Analysis
🧪 Finetuned Keras Model and Classifier .pkl Files
💡 Multi-Modal Prediction Capability (Image + Weather)
🖥️ Clean, Responsive UI Built with TypeScript + Tailwind
📦 No External Database Required – Pure API & Model-Driven

🎥 Demo Video Walkthrough
📺 Project Video Presentation:
👉 Watch the Demo on YouTube

👨‍💻 Built By
Kartikeya Singh & Team

🎓 Guided under the academic project framework
🌟 Passionate about AgriTech innovation through AI

📄 License
This project is licensed under the MIT License.

⚠️ Note: Ensure sensitive API keys are stored securely in .env files before production deployment.
