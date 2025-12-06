// frontend/src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [fileUploaded, setFileUploaded] = useState(false);
  const [fileInfo, setFileInfo] = useState(null);
  const [uploadingFile, setUploadingFile] = useState(false);
  const [wakingUp, setWakingUp] = useState(false);

  // API Base URL - Change this to your deployed backend URL
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploadingFile(true);
    setWakingUp(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/upload/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000, // 60 seconds timeout for cold starts
      });

      setFileUploaded(true);
      setFileInfo(response.data);
      setError('');
      setWakingUp(false);
    } catch (err) {
      if (err.code === 'ECONNABORTED') {
        setError('Server is waking up from sleep. Please try again in a moment.');
      } else {
        setError('Error uploading file. Please check the file format.');
      }
      console.error(err);
      setFileUploaded(false);
      setWakingUp(false);
    } finally {
      setUploadingFile(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!fileUploaded) {
      setError('Please upload a file first');
      return;
    }

    if (!query.trim()) {
      setError('Please enter a query');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/analyze/`, {
        query: query
      }, {
        timeout: 60000, // 60 seconds timeout for AI processing
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Error analyzing query. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const sampleQueries = [
    "Give me analysis of Wakad",
    "Analyze Aundh",
    "Show price trends for Baner"
  ];

  return (
    <div className="App">
      <div className="container py-5">
        <div className="text-center mb-4">
          <h1 className="display-4">📊 Universal Data Analyzer</h1>
          <p className="lead text-muted">Upload ANY data file and get AI-powered insights!</p>
          <small className="text-white-50">Supports: PDF, Excel, CSV, and more</small>
        </div>

        {/* File Upload Section */}
        <div className="row justify-content-center mb-4">
          <div className="col-md-8">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">📁 Step 1: Upload Your Data</h5>
                <p className="text-muted small">Supported: PDF, Excel (.xlsx, .xls), CSV, TSV - Any type of data!</p>
                
                <div className="mb-3">
                  <input
                    type="file"
                    className="form-control"
                    accept=".xlsx,.xls,.csv,.tsv,.pdf"
                    onChange={handleFileUpload}
                    disabled={uploadingFile}
                  />
                </div>

                {uploadingFile && (
                  <div className="alert alert-info">
                    <span className="spinner-border spinner-border-sm me-2"></span>
                    {wakingUp ? 'Waking up server (free tier - first load takes 30-60s)...' : 'Uploading file...'}
                  </div>
                )}

                {fileUploaded && fileInfo && (
                  <div className="alert alert-success">
                    ✅ File uploaded successfully!
                    <div className="small mt-2">
                      <strong>Rows:</strong> {fileInfo.rows} | 
                      <strong> Columns:</strong> {fileInfo.columns.join(', ')}
                    </div>
                    {fileInfo.sample_areas && fileInfo.sample_areas.length > 0 && (
                      <div className="small mt-1">
                        <strong>Sample Areas:</strong> {fileInfo.sample_areas.slice(0, 5).join(', ')}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Query Input */}
        {fileUploaded && (
          <div className="row justify-content-center mb-4">
            <div className="col-md-8">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">💬 Step 2: Ask Anything!</h5>
                  <p className="text-muted small">Ask questions about your data in natural language</p>
                  
                  <form onSubmit={handleSubmit}>
                    <div className="input-group input-group-lg">
                      <input
                        type="text"
                        className="form-control"
                        placeholder="e.g., What are the trends? Show me top performers. Analyze Q4 results."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        disabled={loading}
                      />
                      <button 
                        className="btn btn-primary" 
                        type="submit"
                        disabled={loading}
                      >
                        {loading ? (
                          <>
                            <span className="spinner-border spinner-border-sm me-2"></span>
                            Analyzing...
                          </>
                        ) : (
                          '🔍 Analyze'
                        )}
                      </button>
                    </div>
                  </form>

                  {/* Sample Queries */}
                  {fileInfo?.sample_areas && fileInfo.sample_areas.length > 0 && (
                    <div className="mt-3">
                      <small className="text-muted">Try these:</small>
                      <div className="d-flex gap-2 flex-wrap mt-2">
                        {fileInfo.sample_areas.slice(0, 3).map((area, idx) => (
                          <button
                            key={idx}
                            className="btn btn-sm btn-outline-secondary"
                            onClick={() => setQuery(`Analyze ${area}`)}
                            disabled={loading}
                          >
                            Analyze {area}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="row justify-content-center">
            <div className="col-md-8">
              <div className="alert alert-danger" role="alert">
                {error}
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="row justify-content-center">
            <div className="col-md-10">
              <div className="results">
                {/* Summary */}
                <div className="card mb-4">
                  <div className="card-header bg-primary text-white">
                    <h5 className="mb-0">🤖 AI Analysis</h5>
                  </div>
                  <div className="card-body">
                    <pre className="summary-text">{result.summary}</pre>
                  </div>
                </div>

                {/* Chart */}
                {result.chart_data && result.chart_data.length > 0 && (
                  <div className="card mb-4">
                    <div className="card-header bg-success text-white">
                      <h5 className="mb-0">📈 Price Trends Over Time</h5>
                    </div>
                    <div className="card-body">
                      <ResponsiveContainer width="100%" height={400}>
                        <LineChart data={result.chart_data}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="category" />
                          <YAxis />
                          <Tooltip />
                          <Legend />
                          <Line 
                            type="monotone" 
                            dataKey="value" 
                            stroke="#8884d8" 
                            strokeWidth={2}
                            name={result.chart_data[0]?.label || "Value"}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                )}

                {/* Table */}
                {result.table_data && result.table_data.length > 0 && (
                  <div className="card mb-4">
                    <div className="card-header bg-info text-white">
                      <h5 className="mb-0">📋 Detailed Data ({result.table_data.length} rows)</h5>
                    </div>
                    <div className="card-body">
                      <div className="table-responsive">
                        <table className="table table-striped table-hover">
                          <thead>
                            <tr>
                              {Object.keys(result.table_data[0]).map((key) => (
                                <th key={key}>{key}</th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {result.table_data.map((row, idx) => (
                              <tr key={idx}>
                                {Object.values(row).map((value, i) => (
                                  <td key={i}>
                                    {typeof value === 'number' && value > 1000
                                      ? `₹${value.toLocaleString()}`
                                      : value}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;