# Model Training Notebooks

This directory contains Jupyter notebooks for training and developing machine learning models.

## Purpose
- Store `.ipynb` files for model training and experimentation
- Keep training code separate from deployment code
- Maintain version control of model development process

## Structure
```
notebooks/
├── README.md
├── model_training.ipynb (your training notebook)
├── data_exploration.ipynb
├── feature_engineering.ipynb
└── model_evaluation.ipynb
```

## Guidelines
- Place all training notebooks in this directory
- Use descriptive names for notebook files
- Include clear documentation in notebooks
- Export trained models to the `models/` directory
- Keep this directory separate from deployment files

## Model Deployment
After training, export your models to:
- `models/best_mlp_model.joblib` (for the MLP classifier)
- `models/mlp_scaler.joblib` (for the StandardScaler)

This ensures the deployment application can access the trained models without interference from training code.
