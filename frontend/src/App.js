import React, { useState } from 'react';
import './App.css';

function App() {
  const [images, setImages] = useState([]);
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files);
    if (files.length + images.length > 5) {
      setError('You can only upload up to 5 images');
      return;
    }
    setImages([...images, ...files]);
    setError('');
  };

  const removeImage = (index) => {
    const newImages = images.filter((_, i) => i !== index);
    setImages(newImages);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('prompt', prompt);
      formData.append('style', 'realistic');
      
      images.forEach((image) => {
        formData.append('context_images', image);
      });

      const response = await fetch('http://localhost:8000/generate-image', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Failed to generate image');
      }
    } catch (err) {
      setError('Error connecting to server: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Drip Drop Image Generator</h1>
        <div className="image-generator">
          <form onSubmit={handleSubmit} className="generator-form">
            <div className="upload-section">
              <label htmlFor="images" className="upload-label">
                Upload Reference Images (up to 5):
              </label>
              <input
                type="file"
                id="images"
                accept="image/*"
                multiple
                onChange={handleImageUpload}
                disabled={loading}
              />
              <div className="image-previews">
                {images.map((image, index) => (
                  <div key={index} className="image-preview">
                    <img
                      src={URL.createObjectURL(image)}
                      alt={`Preview ${index + 1}`}
                      onLoad={(e) => URL.revokeObjectURL(e.target.src)}
                    />
                    <button
                      type="button"
                      onClick={() => removeImage(index)}
                      className="remove-btn"
                      disabled={loading}
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <div className="prompt-section">
              <label htmlFor="prompt" className="prompt-label">
                Enter your image generation prompt:
              </label>
              <textarea
                id="prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe the image you want to generate..."
                rows={4}
                disabled={loading}
              />
            </div>

            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? 'Generating...' : 'Generate Image'}
            </button>
          </form>

          {error && <div className="error-message">{error}</div>}

          {result && (
            <div className="result-section">
              <h3>Generated Image:</h3>
              {result.generated_image_base64 && (
                <img
                  src={`data:image/png;base64,${result.generated_image_base64}`}
                  alt="Generated"
                  className="generated-image"
                />
              )}
            </div>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;