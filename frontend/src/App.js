import axios from "axios";
import { useState } from "react";

function App() {
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  const [image1Name, setImage1Name] = useState("");
  const [image2Name, setImage2Name] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);

  const validateTifFile = (file) => {
    const fileName = file.name.toLowerCase();
    return fileName.endsWith('.tif') || fileName.endsWith('.tiff');
  };

  const handleImage1Change = (e) => {
    const file = e.target.files[0];
    setError(null);
    
    if (file) {
      if (!validateTifFile(file)) {
        setError("Invalid input given. Please upload a valid .TIF or .TIFF image.");
        setImage1(null);
        setImage1Name("");
        e.target.value = null;
        return;
      }
      
      // Check if same file is already uploaded as image2
      if (image2 && file.name === image2Name) {
        setError(`"${file.name}" is already uploaded as the second image. Please choose a different file.`);
        e.target.value = null;
        return;
      }
      
      setImage1(file);
      setImage1Name(file.name);
      setResults(null); 
    }
  };

  const handleImage2Change = (e) => {
    const file = e.target.files[0];
    setError(null);
    
    if (file) {
      if (!validateTifFile(file)) {
        setError("Invalid input given. Please upload a valid .TIF or .TIFF image.");
        setImage2(null);
        setImage2Name("");
        e.target.value = null;
        return;
      }
      
      // Check if same file is already uploaded as image1
      if (image1 && file.name === image1Name) {
        setError(`"${file.name}" is already uploaded as the first image. Please choose a different file.`);
        e.target.value = null;
        return;
      }
      
      setImage2(file);
      setImage2Name(file.name);
      setResults(null);
    }
  };

  const analyze = async () => {
    if (!image1 || !image2) {
      setError("Please select both images");
      return;
    }

    setLoading(true);
    setProgress(0);
    setError(null);
    setResults(null);

    const formData = new FormData();
    formData.append("image1", image1);
    formData.append("image2", image2);

    let progressInterval = null;

    try {
      // Simulate progress updates
      progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) {
            return 90;
          }
          return prev + 10;
        });
      }, 500);

      const response = await axios.post(
        "https://landcoverclassification.onrender.com/analyze",
        formData,
        { 
          timeout: 300000,
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setProgress(Math.min(percentCompleted, 30));
          }
        }
      );

      if (progressInterval) clearInterval(progressInterval);
      setProgress(100);
      
      // Store results with filenames
      const resultsWithFiles = {
        ...response.data.results,
        file1Name: image1Name,
        file2Name: image2Name
      };
      
      setResults(resultsWithFiles);
      
      // Store output paths
      if (response.data.outputs) {
        setResults(prev => ({
          ...prev,
          outputs: response.data.outputs
        }));
      }
    } catch (err) {
      console.error("FRONTEND ERROR:", err);
      if (progressInterval) clearInterval(progressInterval);
      
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Analysis failed. Please check that both images are valid multispectral TIF files and try again.");
      }
    } finally {
      setLoading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  };

  const downloadFile = async (url, filename) => {
    try {
      const response = await fetch(`https://landcoverclassification.onrender.com${url}`);
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      console.error('Download error:', error);
      alert('Failed to download file. Please try again.');
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h2>LULC Change Detection Analysis</h2>
      <p style={{ textAlign: "center", color: "#666", marginBottom: "30px" }}>
        Upload two multispectral images (.TIF format) to detect land use and land cover changes
      </p>

      {error && (
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          {error}
        </div>
      )}

      <div className="file-input-wrapper">
        <input 
          type="file" 
          id="file1" 
          onChange={handleImage1Change}
          accept=".tif,.tiff"
        />
        <label 
          htmlFor="file1" 
          className={`file-input-label ${image1 ? 'has-file' : ''}`}
        >
          {image1 ? `Selected: ${image1Name}` : 'Choose First Image (.TIF)'}
        </label>
        {image1 && (
          <div className="file-info">
            <span className="file-size">
              {(image1.size / (1024 * 1024)).toFixed(2)} MB
            </span>
          </div>
        )}
      </div>

      <div className="file-input-wrapper">
        <input 
          type="file" 
          id="file2" 
          onChange={handleImage2Change}
          accept=".tif,.tiff"
        />
        <label 
          htmlFor="file2" 
          className={`file-input-label ${image2 ? 'has-file' : ''}`}
        >
          {image2 ? `Selected: ${image2Name}` : 'Choose Second Image (.TIF)'}
        </label>
        {image2 && (
          <div className="file-info">
            <span className="file-size">
              {(image2.size / (1024 * 1024)).toFixed(2)} MB
            </span>
          </div>
        )}
      </div>

      <button onClick={analyze} disabled={loading || !image1 || !image2 || results}>
        {loading ? "Processing..." : "Run Analysis"}
      </button>

      {loading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <div className="progress-bar-container">
            <div 
              className="progress-bar" 
              style={{ width: `${progress}%` }}
            >
              {progress > 0 && `${progress}%`}
            </div>
          </div>
          <div className="progress-text">
            {progress < 30 && "Uploading images..."}
            {progress >= 30 && progress < 60 && "Processing spectral indices (NDVI, NDWI, NDBI)..."}
            {progress >= 60 && progress < 90 && "Generating change detection map..."}
            {progress >= 90 && "Finalizing results..."}
          </div>
        </div>
      )}

      {results && results.outputs && (
        <div className="results-section">
          {/* Image Previews */}
          <h3>Image Previews</h3>
          <p style={{ textAlign: "center", color: "#666", fontSize: "14px", marginBottom: "20px" }}>
            RGB composite generated from multispectral bands
          </p>
          <div className="preview-grid">
            <div className="preview-item">
              <img
                src={`https://landcoverclassification.onrender.com${results.outputs.preview_image1}?t=${Date.now()}`}
                alt="First satellite preview"
                className="preview-image"
                onError={(e) => {
                  console.error("Error loading preview 1");
                  e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='500' height='500'%3E%3Crect fill='%23f0f0f0' width='500' height='500'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='16' fill='%23999'%3EPreview not available%3C/text%3E%3C/svg%3E";
                }}
              />
              <p className="preview-label">{results.file1Name || "Image 1"}</p>
            </div>
            <div className="preview-item">
              <img
                src={`https://landcoverclassification.onrender.com${results.outputs.preview_image2}?t=${Date.now()}`}
                alt="Second satellite preview"
                className="preview-image"
                onError={(e) => {
                  console.error("Error loading preview 2");
                  e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='500' height='500'%3E%3Crect fill='%23f0f0f0' width='500' height='500'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='16' fill='%23999'%3EPreview not available%3C/text%3E%3C/svg%3E";
                }}
              />
              <p className="preview-label">{results.file2Name || "Image 2"}</p>
            </div>
          </div>

          {/* Land Cover Percentages Table */}
          <h3>Land Cover Percentages</h3>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Category</th>
                  <th>{results.file1Name || "Image 1"} (%)</th>
                  <th>{results.file2Name || "Image 2"} (%)</th>
                  <th>Change (%)</th>
                </tr>
              </thead>
              <tbody>
                {Object.keys(results.image1).map(key => (
                  <tr key={key}>
                    <td><strong>{key}</strong></td>
                    <td>{results.image1[key].toFixed(2)}</td>
                    <td>{results.image2[key].toFixed(2)}</td>
                    <td className={results.change[key] > 0 ? 'positive-change' : results.change[key] < 0 ? 'negative-change' : ''}>
                      {results.change[key] > 0 ? '+' : ''}{results.change[key].toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Download Change Matrix - Right after the table */}
          <div className="download-section">
            <button 
              className="download-btn-csv"
              onClick={() => downloadFile(results.outputs.change_matrix, 'change_matrix.csv')}
            >
              📊 Download Change Matrix (CSV)
            </button>
          </div>

          {/* Total Change Statistics */}
          <div className="change-stats">
            <h3>Change Detection Statistics</h3>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-label">Total Changed Area</div>
                <div className="stat-value">{results.total_change_area.toFixed(2)}%</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Unchanged Area</div>
                <div className="stat-value">{(100 - results.total_change_area).toFixed(2)}%</div>
              </div>
            </div>
          </div>

          {/* Change Map */}
          <h3>Binary Change Detection Map</h3>
          <div className="output-item">
            <img
              src={`https://landcoverclassification.onrender.com${results.outputs.change_map}?t=${Date.now()}`}
              alt="Change Map"
              className="output-image"
              onError={(e) => console.error("Error loading change map")}
            />
            <button 
              className="download-btn"
              onClick={() => downloadFile(results.outputs.change_map, 'change_map.png')}
            >
              📥 Download Change Map
            </button>
          </div>

          {/* Comparison Graph */}
          <h3>Land Cover Comparison Graph</h3>
          <div className="output-item">
            <img
              src={`https://landcoverclassification.onrender.com${results.outputs.comparison_graph}?t=${Date.now()}`}
              alt="Comparison Graph"
              className="output-image"
              onError={(e) => console.error("Error loading comparison graph")}
            />
            <button 
              className="download-btn"
              onClick={() => downloadFile(results.outputs.comparison_graph, 'comparison_graph.png')}
            >
              📥 Download Comparison Graph
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;