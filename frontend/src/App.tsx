import React, { useState } from 'react';
import axios from 'axios';
import { Bot, TestTube2 } from 'lucide-react';
import ResultsViewer from './components/ResultsViewer';

interface TestResponse {
  test_cases_table: string;
  edge_cases: string;
  executable_code: string;
  bug_risk: string;
  success: boolean;
  error?: string;
}

function App() {
  const [inputType, setInputType] = useState('API');
  const [inputData, setInputData] = useState('POST /api/login\\nRequest: {"email": "string", "password": "string"}');
  const [framework, setFramework] = useState('pytest');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<TestResponse | null>(null);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setResults(null);

    try {
      const response = await axios.post<TestResponse>('http://localhost:8000/generate-tests', {
        input_type: inputType,
        input_data: inputData,
        test_framework: framework,
        mode: 'balanced'
      });
      setResults(response.data);
    } catch (error: any) {
      setResults({
        test_cases_table: '',
        edge_cases: '',
        executable_code: '',
        bug_risk: '',
        success: false,
        error: error.message || 'Failed to connect to backend'
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1 className="gradient-text">AI Testcase Generator</h1>
        <p className="subtitle">From requirement to robust executable tests in seconds.</p>
      </header>

      <main>
        <div className="glass-panel" style={{ maxWidth: '800px', margin: '0 auto' }}>
          <form onSubmit={handleGenerate}>
            <div className="form-group" style={{ display: 'flex', gap: '1rem' }}>
              <div style={{ flex: 1 }}>
                <label>Input Type</label>
                <select 
                  className="input-field" 
                  value={inputType} 
                  onChange={(e) => setInputType(e.target.value)}
                >
                  <option value="API">API Specification</option>
                  <option value="Code">Code Snippet</option>
                  <option value="User Story">User Story</option>
                </select>
              </div>
              <div style={{ flex: 1 }}>
                <label>Test Framework</label>
                <select 
                  className="input-field" 
                  value={framework} 
                  onChange={(e) => setFramework(e.target.value)}
                >
                  <option value="pytest">PyTest (Python)</option>
                  <option value="junit">JUnit (Java)</option>
                  <option value="jest">Jest (JavaScript)</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Provide Context Data</label>
              <textarea 
                className="input-field" 
                value={inputData}
                onChange={(e) => setInputData(e.target.value)}
                placeholder="Paste your code, text, or API spec here..."
              ></textarea>
            </div>

            <button type="submit" className="btn-primary" disabled={isLoading || !inputData.trim()}>
              {isLoading ? (
                <>
                  <Bot className="spinner" size={20} />
                  Generating Tests...
                </>
              ) : (
                <>
                  <TestTube2 size={20} />
                  Generate Robust Tests
                </>
              )}
            </button>
          </form>
        </div>

        {results && <ResultsViewer data={results} />}
      </main>
    </div>
  );
}

export default App;
