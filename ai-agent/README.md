# Chat GPT Agent

## Prerequisites

- Python 3.9 installed.

## Getting Started

### Downloading Dataset Files

1. **Destinations Dataset:**
   - Download the `Bali Popular Destination for Tourist 2022` dataset from [Kaggle](https://www.kaggle.com/datasets/fuarresvij/bali-popular-destination-for-tourist-2022).
   - Save the downloaded file as `Destinations.csv` in the `data` folder of this project.

2. **Reviews Dataset:**
   - Download the `Amazon Fine Food Reviews` dataset from [Kaggle](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews).
   - Save the downloaded file as `Reviews.csv` in the `data` folder of this project.

### Project Setup

3. **Setting Up Environment (Optional)**

   If you are using Docker, follow these steps to build and run the project:

   ```bash
   # Clone the repository
   git clone https://github.com/khanhbdang-kms/agent.git
   cd your-project

   # Build Docker image
   docker build -t project-name .

   # Run Docker container
   docker run -p 8501:8501 project-name
