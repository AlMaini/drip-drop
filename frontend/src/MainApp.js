import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import { supabase } from './supabaseClient';
import './App.css';

// Helper function to download base64 image
const downloadImage = (base64String, filename) => {
  try {
    // Convert base64 to blob
    const byteCharacters = atob(base64String);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'image/png' });
    
    // Create download link
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    
    // Cleanup
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error downloading image:', error);
    alert('Error downloading image. Please try again.');
  }
};


// Helper function to upload base64 image to Supabase storage
const uploadBase64ToSupabase = async (base64String, filename) => {
  try {
    // Convert base64 to blob
    const byteCharacters = atob(base64String);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'image/png' });

    const { data, error } = await supabase.storage
      .from('clothing-items')
      .upload(`${Date.now()}-${filename}`, blob, {
        cacheControl: '3600',
        upsert: false
      });

    if (error) throw error;

    // Get public URL
    const { data: { publicUrl } } = supabase.storage
      .from('clothing-items')
      .getPublicUrl(data.path);

    return publicUrl;
  } catch (error) {
    console.error('Error uploading base64 image:', error);
    throw error;
  }
};

// Helper function to save clothing item to database
const saveClothingItem = async (itemData) => {
  try {
    const response = await fetch('http://localhost:8000/supabase/clothes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${(await supabase.auth.getSession()).data.session?.access_token}`
      },
      body: JSON.stringify(itemData)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error saving clothing item:', error);
    throw error;
  }
};

function MainApp() {
  const [activeTab, setActiveTab] = useState('extract');
  const { signOut, user } = useAuth();

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-top">
          <h1>Drip Drop</h1>
          <div className="user-info">
            <span>Welcome, {user?.email}</span>
            <button onClick={signOut} className="logout-button">Logout</button>
          </div>
        </div>
        
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
          <button 
            className={`tab-button ${activeTab === 'quality' ? 'active' : ''}`}
            onClick={() => setActiveTab('quality')}
          >
            Check Photo Quality
          </button>
          <button 
            className={`tab-button ${activeTab === 'itemize' ? 'active' : ''}`}
            onClick={() => setActiveTab('itemize')}
          >
            Itemize Clothing
          </button>
          <button 
            className={`tab-button ${activeTab === 'wardrobe' ? 'active' : ''}`}
            onClick={() => setActiveTab('wardrobe')}
          >
            Add Fit to Wardrobe
          </button>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'extract' && <ExtractClothingTab />}
          {activeTab === 'tryon' && <TryOnTab />}
          {activeTab === 'debug' && <DebugTab />}
          {activeTab === 'quality' && <CheckQualityTab />}
          {activeTab === 'itemize' && <ItemizeClothingTab />}
          {activeTab === 'wardrobe' && <AddFitToWardrobeTab />}
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

      const session = await supabase.auth.getSession();
      const response = await fetch('http://localhost:8000/api/extract-clothing', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${session.data.session?.access_token}`
        },
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        setResult(data);
        
        // Save to database after successful extraction
        try {
          // Upload the generated image to Supabase storage
          const imageUrl = await uploadBase64ToSupabase(
            data.generated_image_base64, 
            `extracted-${Date.now()}.png`
          );
          
          // Save clothing item to database
          const clothingItem = {
            name: data.description || 'Extracted Clothing Item',
            category: 'extracted',
            color: null,
            size: null,
            image_url: imageUrl
          };
          
          await saveClothingItem(clothingItem);
          console.log('Clothing item saved successfully!');
        } catch (saveError) {
          console.error('Error saving to database:', saveError);
          // Don't show error to user as extraction succeeded
        }
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
            <div className="image-container">
              <img
                src={`data:image/png;base64,${result.generated_image_base64}`}
                alt="Extracted clothing"
                className="generated-image"
              />
              <button 
                className="download-btn"
                onClick={() => downloadImage(result.generated_image_base64, 'extracted-clothing.png')}
                title="Download image"
              >
                ⬇ Download
              </button>
            </div>
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
  const [wardrobeItems, setWardrobeItems] = useState({});
  const [wardrobeLoading, setWardrobeLoading] = useState(false);
  const [selectedWardrobeItems, setSelectedWardrobeItems] = useState([]);
  const [activeCategory, setActiveCategory] = useState('all');

  // Fetch wardrobe items when component loads
  React.useEffect(() => {
    fetchWardrobeItems();
  }, []);

  const fetchWardrobeItems = async () => {
    setWardrobeLoading(true);
    try {
      const session = await supabase.auth.getSession();
      const response = await fetch('http://localhost:8000/supabase/clothes/categorized', {
        headers: {
          'Authorization': `Bearer ${session.data.session?.access_token}`
        }
      });

      const data = await response.json();
      if (data.success) {
        setWardrobeItems(data.categories);
      } else {
        console.error('Failed to fetch wardrobe items:', data);
      }
    } catch (err) {
      console.error('Error fetching wardrobe items:', err);
    } finally {
      setWardrobeLoading(false);
    }
  };

  const handleWardrobeItemSelect = async (item) => {
    // Check if item is already selected
    if (selectedWardrobeItems.find(selected => selected.id === item.id)) {
      return;
    }

    // Add to selected wardrobe items
    setSelectedWardrobeItems([...selectedWardrobeItems, item]);

    // If the item has a valid image URL, fetch it and add to clothing images
    if (item.image_url && !item.image_url.startsWith('temp://')) {
      try {
        const response = await fetch(item.image_url);
        const blob = await response.blob();
        
        // Create a File object from the blob with the item name
        const file = new File([blob], `${item.name.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.png`, {
          type: 'image/png',
          lastModified: Date.now()
        });

        // Add a custom property to identify this as a wardrobe item
        file.wardrobeItem = item;
        file.isFromWardrobe = true;

        // Add to clothing images array
        setClothingImages(prev => [...prev, file]);
      } catch (error) {
        console.error(`Failed to fetch wardrobe item image for ${item.name}:`, error);
      }
    }
  };

  const removeWardrobeItem = (itemId) => {
    setSelectedWardrobeItems(selectedWardrobeItems.filter(item => item.id !== itemId));
    
    // Also remove from clothing images if it was added from wardrobe
    setClothingImages(prev => 
      prev.filter(file => !file.isFromWardrobe || file.wardrobeItem?.id !== itemId)
    );
  };

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
    const imageToRemove = clothingImages[index];
    
    // If this was a wardrobe item, also remove it from selected wardrobe items
    if (imageToRemove.isFromWardrobe && imageToRemove.wardrobeItem) {
      setSelectedWardrobeItems(prev => 
        prev.filter(item => item.id !== imageToRemove.wardrobeItem.id)
      );
    }
    
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
      
      // Add all clothing images (both uploaded and from wardrobe)
      clothingImages.forEach((image) => {
        formData.append('images', image);
      });

      const response = await fetch('http://localhost:8000/api/try-on-clothes', {
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
      <p>Upload a photo of a person and select clothing items to see them wearing the clothes</p>
      
      <div className="tryon-container">
        {/* Wardrobe Side Menu */}
        <div className="wardrobe-sidebar">
          <h3>Your Wardrobe</h3>
          {wardrobeLoading ? (
            <div className="loading-message">Loading wardrobe...</div>
          ) : (
            <div className="wardrobe-content">
              {/* Category Tabs */}
              <div className="category-tabs">
                <button 
                  className={`category-tab ${activeCategory === 'all' ? 'active' : ''}`}
                  onClick={() => setActiveCategory('all')}
                >
                  All
                </button>
                {Object.keys(wardrobeItems).map(category => (
                  <button 
                    key={category}
                    className={`category-tab ${activeCategory === category ? 'active' : ''}`}
                    onClick={() => setActiveCategory(category)}
                  >
                    {category.charAt(0).toUpperCase() + category.slice(1)} ({wardrobeItems[category]?.length || 0})
                  </button>
                ))}
              </div>

              {/* Selected Items */}
              {selectedWardrobeItems.length > 0 && (
                <div className="selected-items">
                  <h4>Selected Items ({selectedWardrobeItems.length})</h4>
                  <div className="selected-items-list">
                    {selectedWardrobeItems.map(item => (
                      <div key={item.id} className="selected-item">
                        {item.image_url && !item.image_url.startsWith('temp://') && (
                          <img src={item.image_url} alt={item.name} className="selected-item-image" />
                        )}
                        <span className="selected-item-name">{item.name}</span>
                        <button 
                          className="remove-selected-btn"
                          onClick={() => removeWardrobeItem(item.id)}
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Wardrobe Items */}
              <div className="wardrobe-items">
                {activeCategory === 'all' ? (
                  Object.entries(wardrobeItems).map(([category, items]) => (
                    items.length > 0 && (
                      <div key={category} className="category-section">
                        <h4>{category.charAt(0).toUpperCase() + category.slice(1)}</h4>
                        <div className="wardrobe-items-grid">
                          {items.map(item => (
                            <div 
                              key={item.id} 
                              className={`wardrobe-item-card ${selectedWardrobeItems.find(s => s.id === item.id) ? 'selected' : ''}`}
                              onClick={() => handleWardrobeItemSelect(item)}
                            >
                              {item.image_url && !item.image_url.startsWith('temp://') && (
                                <img src={item.image_url} alt={item.name} className="wardrobe-item-thumbnail" />
                              )}
                              <div className="wardrobe-item-info">
                                <span className="wardrobe-item-name">{item.name}</span>
                                {item.primary_color && (
                                  <span className="wardrobe-item-color">{item.primary_color}</span>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )
                  ))
                ) : (
                  <div className="wardrobe-items-grid">
                    {(wardrobeItems[activeCategory] || []).map(item => (
                      <div 
                        key={item.id} 
                        className={`wardrobe-item-card ${selectedWardrobeItems.find(s => s.id === item.id) ? 'selected' : ''}`}
                        onClick={() => handleWardrobeItemSelect(item)}
                      >
                        {item.image_url && !item.image_url.startsWith('temp://') && (
                          <img src={item.image_url} alt={item.name} className="wardrobe-item-thumbnail" />
                        )}
                        <div className="wardrobe-item-info">
                          <span className="wardrobe-item-name">{item.name}</span>
                          {item.primary_color && (
                            <span className="wardrobe-item-color">{item.primary_color}</span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Main Try On Form */}
        <div className="tryon-main">
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
              <div key={index} className={`image-preview ${image.isFromWardrobe ? 'from-wardrobe' : ''}`}>
                <img
                  src={URL.createObjectURL(image)}
                  alt={image.isFromWardrobe ? image.wardrobeItem?.name : `Clothing ${index + 1}`}
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
                {image.isFromWardrobe && (
                  <div className="wardrobe-badge">
                    <span>👕 {image.wardrobeItem?.name}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        <button type="submit" disabled={loading || !personImage || clothingImages.length === 0} className="submit-btn">
          {loading && <span className="loading-spinner"></span>}
          {loading ? 'Generating Try-On...' : 'Try On Clothes'}
        </button>
      </form>
      </div>
      </div>

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
          {result.final_image_base64 && (
            <div className="image-container">
              <img
                src={`data:image/png;base64,${result.final_image_base64}`}
                alt="Try-on result"
                className="generated-image"
              />
              <button 
                className="download-btn"
                onClick={() => downloadImage(result.final_image_base64, 'try-on-result.png')}
                title="Download final result"
              >
                ⬇ Download
              </button>
            </div>
          )}
          {result.description && (
            <p className="result-description">{result.description}</p>
          )}
          <div className="result-stats">
            <p className="result-info">Images processed: {result.images_processed}</p>
            <p className="result-info">Total iterations: {result.total_iterations}</p>
            <p className="result-info">Successful iterations: {result.successful_iterations}</p>
            <p className="result-info">Clothing items: {result.total_clothing_items}</p>
          </div>
          
          {result.iteration_results && result.iteration_results.length > 0 && (
            <div className="iteration-details">
              <h4>Iteration Details:</h4>
              <div className="iterations-grid">
                {result.iteration_results.map((iteration, index) => (
                  <div key={index} className={`iteration-item ${iteration.success ? 'success' : 'error'}`}>
                    <div className="iteration-header">
                      <span className="iteration-number">Iteration {iteration.iteration}</span>
                      <span className={`status-badge ${iteration.success ? 'success' : 'error'}`}>
                        {iteration.success ? '✓' : '✗'}
                      </span>
                    </div>
                    <p className="iteration-info">{iteration.items_added} item(s) applied</p>
                    {iteration.description && (
                      <p className="iteration-description">{iteration.description}</p>
                    )}
                    {iteration.error && (
                      <p className="iteration-error">{iteration.error}</p>
                    )}
                    {iteration.success && iteration.generated_image_base64 && (
                      <div className="image-container">
                        <img
                          src={`data:image/png;base64,${iteration.generated_image_base64}`}
                          alt={`Iteration ${iteration.iteration} result`}
                          className="iteration-image"
                        />
                        <button 
                          className="download-btn small"
                          onClick={() => downloadImage(iteration.generated_image_base64, `try-on-iteration-${iteration.iteration}.png`)}
                          title={`Download iteration ${iteration.iteration} result`}
                        >
                          ⬇
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
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

      const response = await fetch('http://localhost:8000/api/generate-image', {
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
            <div className="image-container">
              <img
                src={`data:image/png;base64,${result.generated_image_base64}`}
                alt="Generated"
                className="generated-image"
              />
              <button 
                className="download-btn"
                onClick={() => downloadImage(result.generated_image_base64, 'generated-image.png')}
                title="Download generated image"
              >
                ⬇ Download
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// Check Quality Tab Component
function CheckQualityTab() {
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

      const response = await fetch('http://localhost:8000/api/check-clothing-quality', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      // Log the entire JSON response to console
      console.log('Check Photo Quality API Response:', JSON.stringify(data, null, 2));

      if (data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Failed to check image quality');
      }
    } catch (err) {
      setError('Error connecting to server: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const getQualityIndicator = (quality) => {
    const qualityMap = {
      'excellent': { class: 'quality-excellent', label: 'Excellent' },
      'good': { class: 'quality-good', label: 'Good' },
      'poor': { class: 'quality-poor', label: 'Poor' }
    };
    return qualityMap[quality] || { class: 'quality-unknown', label: 'Unknown' };
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'confidence-high';
    if (confidence >= 0.6) return 'confidence-medium';
    return 'confidence-low';
  };

  return (
    <div className="tab-panel">
      <h2>Check Photo Quality</h2>
      <p>Upload an image to check if it's a professional studio quality photo of a single clothing item</p>
      
      <form onSubmit={handleSubmit} className={`generator-form ${loading ? 'loading-overlay' : ''}`}>
        <div className="upload-section">
          <label htmlFor="quality-image" className="upload-label">
            Select Image to Check:
          </label>
          <input
            type="file"
            id="quality-image"
            accept="image/*"
            onChange={handleImageUpload}
            disabled={loading}
          />
          {image && (
            <div className="image-preview">
              <img
                src={URL.createObjectURL(image)}
                alt="Image to check"
                onLoad={(e) => URL.revokeObjectURL(e.target.src)}
              />
            </div>
          )}
        </div>

        <button type="submit" disabled={loading || !image} className="submit-btn">
          {loading && <span className="loading-spinner"></span>}
          {loading ? 'Analyzing...' : 'Check Quality'}
        </button>
      </form>

      {loading && (
        <div className="loading-message">
          <span className="loading-spinner"></span>
          Analyzing image quality - this may take a few moments...
        </div>
      )}

      {error && <div className="error-message">{error}</div>}

      {result && result.analysis && (
        <div className="result-section quality-analysis">
          <h3>Quality Analysis Results:</h3>
          <div className="analysis-grid">
            <div className="analysis-item">
              <span className="label">Professional Quality:</span>
              <span className={`value ${result.analysis.is_professional ? 'positive' : 'negative'}`}>
                {result.analysis.is_professional ? '✓ Yes' : '✗ No'}
              </span>
            </div>
            
            <div className="analysis-item">
              <span className="label">Single Item:</span>
              <span className={`value ${result.analysis.is_single_item ? 'positive' : 'negative'}`}>
                {result.analysis.is_single_item ? '✓ Yes' : '✗ No'}
              </span>
            </div>
            
            {result.analysis.item_type && (
              <div className="analysis-item">
                <span className="label">Item Type:</span>
                <span className="value">{result.analysis.item_type}</span>
              </div>
            )}
            
            {result.analysis.background_quality && (
              <div className="analysis-item">
                <span className="label">Background Quality:</span>
                <span className={`value quality-badge ${getQualityIndicator(result.analysis.background_quality).class}`}>
                  {getQualityIndicator(result.analysis.background_quality).label}
                </span>
              </div>
            )}
            
            {result.analysis.lighting_quality && (
              <div className="analysis-item">
                <span className="label">Lighting Quality:</span>
                <span className={`value quality-badge ${getQualityIndicator(result.analysis.lighting_quality).class}`}>
                  {getQualityIndicator(result.analysis.lighting_quality).label}
                </span>
              </div>
            )}
            
            {result.analysis.overall_confidence !== undefined && (
              <div className="analysis-item">
                <span className="label">Confidence:</span>
                <span className={`value confidence-badge ${getConfidenceColor(result.analysis.overall_confidence)}`}>
                  {Math.round(result.analysis.overall_confidence * 100)}%
                </span>
              </div>
            )}
          </div>
          
          {result.analysis.reasoning && (
            <div className="analysis-reasoning">
              <h4>Analysis Reasoning:</h4>
              <p>{result.analysis.reasoning}</p>
            </div>
          )}
          
          {result.analysis.issues && result.analysis.issues.length > 0 && (
            <div className="analysis-issues">
              <h4>Issues Found:</h4>
              <ul>
                {result.analysis.issues.map((issue, index) => (
                  <li key={index}>{issue}</li>
                ))}
              </ul>
            </div>
          )}
          
          {result.filename && (
            <div className="analysis-meta">
              <small>File: {result.filename}</small>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// Itemize Clothing Tab Component
function ItemizeClothingTab() {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [extracting, setExtracting] = useState(false);
  const [extractedResults, setExtractedResults] = useState(null);
  const [batchStatus, setBatchStatus] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setError('');
      setResult(null);
      setExtractedResults(null);
      setBatchStatus(null);
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

      const session = await supabase.auth.getSession();
      const response = await fetch('http://localhost:8000/api/itemize-clothing', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${session.data.session?.access_token}`
        },
        body: formData,
      });

      const data = await response.json();

      // Log the entire JSON response to console
      console.log('Itemize Clothing API Response:', JSON.stringify(data, null, 2));

      if (data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Failed to itemize clothing');
      }
    } catch (err) {
      setError('Error connecting to server: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExtractSpecific = async () => {
    if (!image || !result) {
      setError('No items to extract');
      return;
    }

    // Check if we have any items to extract
    const hasClothing = result.clothing_items && result.clothing_items.length > 0;
    const hasAccessories = result.accessories && result.accessories.length > 0;
    
    if (!hasClothing && !hasAccessories) {
      setError('No clothing items or accessories to extract');
      return;
    }

    setExtracting(true);
    setError('');
    setExtractedResults(null);
    setBatchStatus('Processing concurrent extraction...');

    try {
      const formData = new FormData();
      formData.append('image', image);
      
      // Extract just the names for the extraction API (it expects strings, not objects)
      const clothingNames = (result.clothing_items || []).map(item => 
        typeof item === 'string' ? item : item.name
      );
      const accessoryNames = (result.accessories || []).map(item => 
        typeof item === 'string' ? item : item.name
      );
      const allItemNames = [...clothingNames, ...accessoryNames];
      formData.append('clothing_items', JSON.stringify(allItemNames));

      // Submit concurrent extraction request
      const session = await supabase.auth.getSession();
      const response = await fetch('http://localhost:8000/api/extract-clothes-concurrent', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${session.data.session?.access_token}`
        },
        body: formData,
      });

      const data = await response.json();

      // Log the entire JSON response to console
      console.log('Extract Clothes Concurrent API Response:', JSON.stringify(data, null, 2));

      if (data.success) {
        // The concurrent endpoint processes all items in parallel and returns results immediately
        setExtractedResults(data);
        setExtracting(false);
        setBatchStatus(`Extraction completed! (${data.processing_time}s using ${data.processing_method})`);
        
        // Save extracted items to database
        try {
          if (data.extracted_items && data.extracted_items.length > 0) {
            for (const extractedItem of data.extracted_items) {
              try {
                // Upload the extracted image to Supabase storage
                const imageUrl = await uploadBase64ToSupabase(
                  extractedItem.extracted_image_base64, 
                  `itemized-${extractedItem.description.replace(/\s+/g, '-').toLowerCase()}-${Date.now()}.png`
                );
                
                // Save clothing item to database
                const clothingItem = {
                  name: extractedItem.description,
                  category: extractedItem.category || 'itemized',
                  color: extractedItem.color || null,
                  size: extractedItem.size || null,
                  image_url: imageUrl
                };
                
                await saveClothingItem(clothingItem);
                console.log(`Saved ${extractedItem.description} to database`);
              } catch (itemError) {
                console.error(`Error saving ${extractedItem.description}:`, itemError);
              }
            }
            console.log(`Successfully saved ${data.extracted_items.length} items to database!`);
          }
        } catch (saveError) {
          console.error('Error saving items to database:', saveError);
          // Don't show error to user as extraction succeeded
        }
      } else {
        setError(data.error || 'Failed to extract clothing items');
        setExtracting(false);
        setBatchStatus(null);
      }
    } catch (err) {
      setError('Error connecting to server: ' + err.message);
      setExtracting(false);
      setBatchStatus(null);
    }
  };


  return (
    <div className="tab-panel">
      <h2>Itemize Clothing</h2>
      <p>Upload an image to get a detailed list of all clothing items and accessories visible in the photo</p>
      
      <form onSubmit={handleSubmit} className={`generator-form ${loading ? 'loading-overlay' : ''}`}>
        <div className="upload-section">
          <label htmlFor="itemize-image" className="upload-label">
            Select Image to Analyze:
          </label>
          <input
            type="file"
            id="itemize-image"
            accept="image/*"
            onChange={handleImageUpload}
            disabled={loading}
          />
          {image && (
            <div className="image-preview">
              <img
                src={URL.createObjectURL(image)}
                alt="Image to analyze"
                onLoad={(e) => URL.revokeObjectURL(e.target.src)}
              />
            </div>
          )}
        </div>

        <button type="submit" disabled={loading || !image} className="submit-btn">
          {loading && <span className="loading-spinner"></span>}
          {loading ? 'Analyzing...' : 'Itemize Clothing'}
        </button>
      </form>

      {loading && (
        <div className="loading-message">
          <span className="loading-spinner"></span>
          Analyzing clothing items and accessories - this may take a few moments...
        </div>
      )}

      {error && <div className="error-message">{error}</div>}

      {result && (
        <div className="result-section clothing-itemization">
          <h3>Items Found:</h3>
          <div className="itemization-summary">
            <span className="item-count">{result.item_count} item{result.item_count !== 1 ? 's' : ''} detected</span>
            {result.saved_items_count !== undefined && (
              <span className="saved-count"> ({result.saved_items_count} saved to wardrobe)</span>
            )}
            {result.filename && <span className="filename">in {result.filename}</span>}
          </div>
          
          {/* Clothing Items Section */}
          {result.clothing_items && result.clothing_items.length > 0 && (
            <div className="items-section">
              <h4 className="section-title">Clothing Items ({result.clothing_items.length})</h4>
              <div className="clothing-items-list">
                {result.clothing_items.map((item, index) => (
                  <div key={`clothing-${index}`} className="clothing-item enhanced">
                    <div className="item-header">
                      <span className="item-number">{index + 1}</span>
                      <span className="item-name">{typeof item === 'string' ? item : item.name}</span>
                      {typeof item === 'object' && item?.saved_item_id && (
                        <span className="saved-badge">✓ Saved</span>
                      )}
                      {typeof item === 'object' && item?.save_error && (
                        <span className="error-badge">⚠ Save Error</span>
                      )}
                    </div>
                    {typeof item === 'object' && item !== null && (
                      <div className="item-details">
                        {item.type && <span className="item-detail">Type: {item.type}</span>}
                        {item.primary_color && <span className="item-detail">Primary Color: {item.primary_color}</span>}
                        {item.secondary_color && item.secondary_color !== item.primary_color && (
                          <span className="item-detail">Secondary Color: {item.secondary_color}</span>
                        )}
                        {item.features && typeof item.features === 'object' && Object.keys(item.features).length > 0 && (
                          <div className="item-features">
                            <span className="features-label">Features:</span>
                            {Object.entries(item.features).map(([key, value]) => (
                              <span key={key} className="feature-tag">{key}: {String(value)}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Accessories Section */}
          {result.accessories && result.accessories.length > 0 && (
            <div className="items-section">
              <h4 className="section-title">Accessories ({result.accessories.length})</h4>
              <div className="clothing-items-list">
                {result.accessories.map((item, index) => (
                  <div key={`accessory-${index}`} className="clothing-item enhanced">
                    <div className="item-header">
                      <span className="item-number">{index + 1}</span>
                      <span className="item-name">{typeof item === 'string' ? item : item.name}</span>
                      {typeof item === 'object' && item?.saved_item_id && (
                        <span className="saved-badge">✓ Saved</span>
                      )}
                      {typeof item === 'object' && item?.save_error && (
                        <span className="error-badge">⚠ Save Error</span>
                      )}
                    </div>
                    {typeof item === 'object' && item !== null && (
                      <div className="item-details">
                        {item.type && <span className="item-detail">Type: {item.type}</span>}
                        {item.primary_color && <span className="item-detail">Primary Color: {item.primary_color}</span>}
                        {item.secondary_color && item.secondary_color !== item.primary_color && (
                          <span className="item-detail">Secondary Color: {item.secondary_color}</span>
                        )}
                        {item.features && typeof item.features === 'object' && Object.keys(item.features).length > 0 && (
                          <div className="item-features">
                            <span className="features-label">Features:</span>
                            {Object.entries(item.features).map(([key, value]) => (
                              <span key={key} className="feature-tag">{key}: {String(value)}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* No items found */}
          {(!result.clothing_items || result.clothing_items.length === 0) && 
           (!result.accessories || result.accessories.length === 0) && (
            <div className="no-items">
              <p>No clothing items or accessories were detected in this image.</p>
            </div>
          )}
          
          {/* Extract button - show if we have any items */}
          {((result.clothing_items && result.clothing_items.length > 0) || 
            (result.accessories && result.accessories.length > 0)) && (
            <div className="extract-actions">
              <button 
                onClick={handleExtractSpecific} 
                disabled={extracting || !image}
                className="extract-btn"
              >
                {extracting && <span className="loading-spinner"></span>}
                {extracting ? 'Extracting Items...' : 'Extract Individual Items'}
              </button>
              <p className="extract-description">
                Create professional product photos for each detected item
              </p>
            </div>
          )}
        </div>
      )}

      {extracting && (
        <div className="loading-message">
          <span className="loading-spinner"></span>
          <div className="batch-status-info">
            <p>Extracting individual clothing items and accessories using concurrent processing...</p>
            {batchStatus && <p className="batch-status">{batchStatus}</p>}
          </div>
        </div>
      )}

      {extractedResults && (
        <div className="result-section extracted-items">
          <h3>Extracted Items:</h3>
          <div className="extraction-summary">
            <span className="extraction-count">
              {extractedResults.successful_extractions} of {extractedResults.total_items} items extracted successfully
            </span>
          </div>
          
          <div className="extracted-images-grid">
            {extractedResults.extracted_images.map((extraction, index) => (
              <div key={index} className={`extracted-item ${extraction.success ? 'success' : 'error'}`}>
                <div className="extraction-header">
                  <h4 className="item-title">{extraction.item}</h4>
                  {extraction.success ? (
                    <span className="status-badge success">✓ Success</span>
                  ) : (
                    <span className="status-badge error">✗ Failed</span>
                  )}
                </div>
                
                {extraction.success && extraction.generated_image_base64 ? (
                  <div className="extracted-image-container">
                    <div className="image-container">
                      <img
                        src={`data:image/png;base64,${extraction.generated_image_base64}`}
                        alt={extraction.item}
                        className="extracted-image"
                      />
                      <button 
                        className="download-btn small"
                        onClick={() => downloadImage(extraction.generated_image_base64, `extracted-${extraction.item.replace(/[^a-zA-Z0-9]/g, '-')}.png`)}
                        title={`Download ${extraction.item}`}
                      >
                        ⬇
                      </button>
                    </div>
                    {extraction.description && (
                      <p className="extraction-description">{extraction.description}</p>
                    )}
                  </div>
                ) : (
                  <div className="extraction-error">
                    <p>{extraction.error || 'Failed to extract this item'}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Add Fit to Wardrobe Tab Component
function AddFitToWardrobeTab() {
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

      const session = await supabase.auth.getSession();
      const response = await fetch('http://localhost:8000/api/add-fit-to-wardrobe', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${session.data.session?.access_token}`
        },
        body: formData,
      });

      const data = await response.json();

      // Log the entire JSON response to console
      console.log('Add Fit to Wardrobe API Response:', JSON.stringify(data, null, 2));

      if (data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Failed to add fit to wardrobe');
      }
    } catch (err) {
      setError('Error connecting to server: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="tab-panel">
      <h2>Add Fit to Wardrobe</h2>
      <p>Upload an outfit image to automatically identify, extract, and save all clothing items to your wardrobe with professional photos</p>
      
      <form onSubmit={handleSubmit} className={`generator-form ${loading ? 'loading-overlay' : ''}`}>
        <div className="upload-section">
          <label htmlFor="wardrobe-image" className="upload-label">
            Select Outfit Image:
          </label>
          <input
            type="file"
            id="wardrobe-image"
            accept="image/*"
            onChange={handleImageUpload}
            disabled={loading}
          />
          {image && (
            <div className="image-preview">
              <img
                src={URL.createObjectURL(image)}
                alt="Outfit to add"
                onLoad={(e) => URL.revokeObjectURL(e.target.src)}
              />
            </div>
          )}
        </div>

        <button type="submit" disabled={loading || !image} className="submit-btn wardrobe-btn">
          {loading && <span className="loading-spinner"></span>}
          {loading ? 'Processing Outfit...' : 'Add to Wardrobe'}
        </button>
      </form>

      {loading && (
        <div className="loading-message">
          <span className="loading-spinner"></span>
          <div className="processing-steps">
            <p>Processing your outfit - this may take a few moments...</p>
            <div className="step-indicator">
              <div className="step">1. Analyzing clothing items</div>
              <div className="step">2. Extracting individual items</div>
              <div className="step">3. Uploading to storage</div>
              <div className="step">4. Saving to your wardrobe</div>
            </div>
          </div>
          <div className="loading-progress">
            <div className="loading-progress-bar"></div>
          </div>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}

      {result && (
        <div className="result-section wardrobe-results">
          <h3>Successfully Added to Wardrobe!</h3>
          <div className="wardrobe-summary">
            <div className="summary-stats">
              <div className="stat-item">
                <span className="stat-number">{result.total_items_found}</span>
                <span className="stat-label">Items Found</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">{result.items_saved}</span>
                <span className="stat-label">Items Saved</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">{result.items_with_images}</span>
                <span className="stat-label">With Photos</span>
              </div>
            </div>
            {result.message && <p className="success-message">{result.message}</p>}
          </div>
          
          {/* Saved Items Display */}
          {result.saved_items && result.saved_items.length > 0 && (
            <div className="saved-items-section">
              <h4>Your New Wardrobe Items:</h4>
              <div className="wardrobe-items-grid">
                {result.saved_items.map((item, index) => (
                  <div key={index} className={`wardrobe-item ${item.extraction_success ? 'with-image' : 'no-image'}`}>
                    <div className="item-header">
                      <h5 className="item-name">{item.name}</h5>
                      <div className="item-badges">
                        <span className="category-badge">{item.category}</span>
                        {item.extraction_success ? (
                          <span className="success-badge">✓ Photo</span>
                        ) : (
                          <span className="warning-badge">⚠ No Photo</span>
                        )}
                      </div>
                    </div>
                    
                    <div className="item-details">
                      {item.primary_color && (
                        <span className="detail-item">
                          <strong>Color:</strong> {item.primary_color}
                          {item.secondary_color && item.secondary_color !== item.primary_color && 
                            `, ${item.secondary_color}`}
                        </span>
                      )}
                    </div>
                    
                    {item.extraction_success && item.image_url && !item.image_url.startsWith('temp://') && (
                      <div className="item-image-preview">
                        <img 
                          src={item.image_url} 
                          alt={item.name}
                          className="wardrobe-item-image"
                          onError={(e) => {
                            e.target.style.display = 'none';
                            e.target.nextSibling.style.display = 'block';
                          }}
                        />
                        <div className="image-placeholder" style={{display: 'none'}}>
                          No image available
                        </div>
                      </div>
                    )}
                    
                    {item.extraction_error && (
                      <div className="extraction-error">
                        <small>Photo extraction failed: {item.extraction_error}</small>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {result.filename && (
            <div className="processing-meta">
              <small>Processed: {result.filename}</small>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default MainApp;