import React, { useState } from 'react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('extract');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Drip Drop</h1>
        
        {/* Tab Navigation */}
        <div className="tab-navigation">
          <button 
            className={`tab-button ${activeTab === 'extract' ? 'active' : ''}`}
            onClick={() => setActiveTab('extract')}
          >
            Extract Clothing
          </button>
          <button 
            className={`tab-button ${activeTab === 'tryon' ? 'active' : ''}`}
            onClick={() => setActiveTab('tryon')}
          >
            Try On Clothes
          </button>
          <button 
            className={`tab-button ${activeTab === 'debug' ? 'active' : ''}`}
            onClick={() => setActiveTab('debug')}
          >
            Debug
          </button>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'extract' && <ExtractClothingTab />}
          {activeTab === 'tryon' && <TryOnTab />}
          {activeTab === 'debug' && <DebugTab />}
        </div>
      </header>
    </div>
  );
}

// Extract Clothing Tab Component
function ExtractClothingTab() {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setError('');
      setResult(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!image) {
      setError('Please select an image');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('image', image);

      const response = await fetch('http://localhost:8000/extract-clothing', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Failed to extract clothing');
      }
    } catch (err) {
      setError('Error connecting to server: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="tab-panel">
      <h2>Extract Clothing Item</h2>
      <p>Upload an image containing a clothing item to create a professional product photo</p>
      
      <form onSubmit={handleSubmit} className={`generator-form ${loading ? 'loading-overlay' : ''}`}>
        <div className="upload-section">
          <label htmlFor="extract-image" className="upload-label">
            Select Clothing Image:
          </label>
          <input
            type="file"
            id="extract-image"
            accept="image/*"
            onChange={handleImageUpload}
            disabled={loading}
          />
          {image && (
            <div className="image-preview">
              <img
                src={URL.createObjectURL(image)}
                alt="Clothing item"
                onLoad={(e) => URL.revokeObjectURL(e.target.src)}
              />
            </div>
          )}
        </div>

        <button type="submit" disabled={loading || !image} className="submit-btn">
          {loading && <span className="loading-spinner"></span>}
          {loading ? 'Extracting...' : 'Extract Clothing'}
        </button>
      </form>

      {loading && (
        <div className="loading-message">
          <span className="loading-spinner"></span>
          Processing your image - this may take a few moments...
          <div className="loading-progress">
            <div className="loading-progress-bar"></div>
          </div>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}

      {result && (
        <div className="result-section">
          <h3>Professional Product Photo:</h3>
          {result.generated_image_base64 && (
            <img
              src={`data:image/png;base64,${result.generated_image_base64}`}
              alt="Extracted clothing"
              className="generated-image"
            />
          )}
          {result.description && (
            <p className="result-description">{result.description}</p>
          )}
        </div>
      )}
    </div>
  );
}

// Try On Tab Component
function TryOnTab() {
  const [personImage, setPersonImage] = useState(null);
  const [clothingImages, setClothingImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handlePersonImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPersonImage(file);
      setError('');
      setResult(null);
    }
  };

  const handleClothingImageUpload = (e) => {
    const files = Array.from(e.target.files);
    if (files.length + clothingImages.length > 4) {
      setError('You can only upload up to 4 clothing items');
      return;
    }
    setClothingImages([...clothingImages, ...files]);
    setError('');
    setResult(null);
  };

  const removeClothingImage = (index) => {
    const newImages = clothingImages.filter((_, i) => i !== index);
    setClothingImages(newImages);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!personImage) {
      setError('Please select a person image');
      return;
    }

    if (clothingImages.length === 0) {
      setError('Please select at least one clothing item');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const formData = new FormData();
      
      // Add person image first
      formData.append('images', personImage);
      
      // Add clothing images
      clothingImages.forEach((image) => {
        formData.append('images', image);
      });

      const response = await fetch('http://localhost:8000/try-on-clothes', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Failed to generate try-on');
      }
    } catch (err) {
      setError('Error connecting to server: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="tab-panel">
      <h2>Try On Clothes</h2>
      <p>Upload a photo of a person and clothing items to see them wearing the clothes</p>
      
      <form onSubmit={handleSubmit} className={`generator-form ${loading ? 'loading-overlay' : ''}`}>
        <div className="upload-section">
          <label htmlFor="person-image" className="upload-label">
            Select Person Image:
          </label>
          <input
            type="file"
            id="person-image"
            accept="image/*"
            onChange={handlePersonImageUpload}
            disabled={loading}
          />
          {personImage && (
            <div className="image-preview">
              <img
                src={URL.createObjectURL(personImage)}
                alt="Person"
                onLoad={(e) => URL.revokeObjectURL(e.target.src)}
              />
            </div>
          )}
        </div>

        <div className="upload-section">
          <label htmlFor="clothing-images" className="upload-label">
            Select Clothing Items (up to 4):
          </label>
          <input
            type="file"
            id="clothing-images"
            accept="image/*"
            multiple
            onChange={handleClothingImageUpload}
            disabled={loading}
          />
          <div className="image-previews">
            {clothingImages.map((image, index) => (
              <div key={index} className="image-preview">
                <img
                  src={URL.createObjectURL(image)}
                  alt={`Clothing ${index + 1}`}
                  onLoad={(e) => URL.revokeObjectURL(e.target.src)}
                />
                <button
                  type="button"
                  onClick={() => removeClothingImage(index)}
                  className="remove-btn"
                  disabled={loading}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>

        <button type="submit" disabled={loading || !personImage || clothingImages.length === 0} className="submit-btn">
          {loading && <span className="loading-spinner"></span>}
          {loading ? 'Generating Try-On...' : 'Try On Clothes'}
        </button>
      </form>

      {loading && (
        <div className="loading-message">
          <span className="loading-spinner"></span>
          Generating your try-on - this may take a few moments...
          <div className="loading-progress">
            <div className="loading-progress-bar"></div>
          </div>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}

      {result && (
        <div className="result-section">
          <h3>Try-On Result:</h3>
          {result.generated_image_base64 && (
            <img
              src={`data:image/png;base64,${result.generated_image_base64}`}
              alt="Try-on result"
              className="generated-image"
            />
          )}
          {result.description && (
            <p className="result-description">{result.description}</p>
          )}
          <p className="result-info">Images processed: {result.images_processed}</p>
        </div>
      )}
    </div>
  );
}

// Debug Tab Component (using generate-image endpoint as is)
function DebugTab() {
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
    <div className="tab-panel">
      <h2>Debug - Image Generator</h2>
      <p>Original image generation functionality for debugging</p>
      
      <form onSubmit={handleSubmit} className={`generator-form ${loading ? 'loading-overlay' : ''}`}>
        <div className="upload-section">
          <label htmlFor="debug-images" className="upload-label">
            Upload Reference Images (up to 5):
          </label>
          <input
            type="file"
            id="debug-images"
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
          <label htmlFor="debug-prompt" className="prompt-label">
            Enter your image generation prompt:
          </label>
          <textarea
            id="debug-prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe the image you want to generate..."
            rows={4}
            disabled={loading}
          />
        </div>

        <button type="submit" disabled={loading} className="submit-btn">
          {loading && <span className="loading-spinner"></span>}
          {loading ? 'Generating...' : 'Generate Image'}
        </button>
      </form>

      {loading && (
        <div className="loading-message">
          <span className="loading-spinner"></span>
          Generating your image - this may take a few moments...
          <div className="loading-progress">
            <div className="loading-progress-bar"></div>
          </div>
        </div>
      )}

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
  );
}

export default App;