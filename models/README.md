# ML Model Files

This directory should contain the trained machine learning model files for seizure prediction.

## Required Files

- `best_mlp_model.joblib` - The trained MLP (Multi-Layer Perceptron) model
- `mlp_scaler.joblib` - The feature scaler used during training

## File Format

Both files should be saved using joblib format:
```python
import joblib

# Save model
joblib.dump(model, 'best_mlp_model.joblib')

# Save scaler  
joblib.dump(scaler, 'mlp_scaler.joblib')
```

## Model Requirements

- The model should accept 115 EEG features as input
- Output should be binary classification (0 = no seizure risk, 1 = seizure risk)
- The scaler should be compatible with the same 115 features

## Testing

You can test the model loading by running:
```python
import joblib
import numpy as np

# Load model and scaler
model = joblib.load('best_mlp_model.joblib')
scaler = joblib.load('mlp_scaler.joblib')

# Test with dummy data
features = np.random.random(115).reshape(1, -1)
scaled_features = scaler.transform(features)
prediction = model.predict(scaled_features)
print(f"Prediction: {prediction}")
``` 