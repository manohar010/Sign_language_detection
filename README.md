# Sign_language_detection
✋ Real-Time Sign Language Recognition (YOLOv8)📖 About the ProjectThis application leverages the power of Computer Vision to bridge communication gaps. By using a custom-trained YOLOv8s model, the system identifies hand gestures in milliseconds and displays the translation on a sleek web interface.Why this project stands out:Optimized Performance: Trained on a specialized dataset with an image size of 416px for low-latency inference.Production Ready: Includes a Flask wrapper for easy deployment on local servers or cloud edge devices.Robust Metrics: Achieved near-perfect precision (~0.99 mAP) as recorded in the training logs.📊 System Architecture & Data FlowCode snippetgraph TD
    subgraph Input
    A[Webcam Feed] --> B[Frame Capture]
    end
    
    subgraph AI Engine
    B --> C[YOLOv8s Model]
    C --> D{Inference}
    D --> E[Class Labeling]
    D --> F[Bounding Box Generation]
    end
    
    subgraph Output
    E & F --> G[Flask Stream]
    G --> H[Web Dashboard]
    end

    style C fill:#f96,stroke:#333
    style H fill:#69f,stroke:#333
📈 Training & Validation PerformanceBased on the results.csv generated during the 100-epoch training phase:MetricValueStatusmAP500.995✅ ExcellentPrecision0.996✅ Highly AccurateRecall1.000✅ No Missed SignsImage Size416⚡ Optimized for Speed🛠️ Step-by-Step Installation1. Clone and NavigateBashgit clone https://github.com/manohar010/Sign_language_detection.git
cd Sign_language_detection
2. Initialize EnvironmentBashpython -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
3. Install Core DependenciesBashpip install ultralytics flask opencv-python pandas
4. Execute ApplicationBashpython app_web.py
📂 Directory Structure (Standardized)Plaintext.
├── app_web.py           # Flask Backend Engine
├── best.pt              # Optimized Model Weights
├── args.yaml            # Hyperparameter Config
├── results.csv          # Training Metrics Data
├── requirements.txt     # Dependency Manifest
└── templates/
    └── index.html       # Web Frontend UI
