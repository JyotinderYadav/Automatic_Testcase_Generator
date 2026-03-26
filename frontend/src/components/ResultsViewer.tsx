import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/atom-one-dark.css';

interface TestResponse {
  test_cases_table: string;
  edge_cases: string;
  executable_code: string;
  bug_risk: string;
  success: boolean;
  error?: string;
}

interface Props {
  data: TestResponse;
}

const ResultsViewer: React.FC<Props> = ({ data }) => {
  const [activeTab, setActiveTab] = useState<'table' | 'code' | 'edge' | 'bugs'>('table');

  if (!data.success) {
    return (
      <div className="glass-panel" style={{ borderColor: 'var(--error-color)' }}>
        <h2>Generation Failed</h2>
        <p style={{ color: 'var(--error-color)' }}>{data.error || 'Unknown error occurred.'}</p>
      </div>
    );
  }

  const renderContent = () => {
    let content = '';
    switch (activeTab) {
      case 'table':
        content = data.test_cases_table;
        break;
      case 'code':
        content = `\`\`\`${data.executable_code.includes('import pytest') ? 'python' : data.executable_code.includes('import org.junit') ? 'java' : 'javascript'}\n${data.executable_code}\n\`\`\``;
        // The backend already returns a code block maybe? Let's check backend... The backend returns raw code! So we wrap it.
        break;
      case 'edge':
        content = data.edge_cases;
        break;
      case 'bugs':
        content = data.bug_risk;
        break;
      default:
        content = '';
    }

    return (
      <div className="markdown-body">
        <ReactMarkdown rehypePlugins={[rehypeHighlight]}>
          {content}
        </ReactMarkdown>
      </div>
    );
  };

  return (
    <div className="results-section glass-panel">
      <div className="tabs">
        <button 
          className={`tab-btn ${activeTab === 'table' ? 'active' : ''}`}
          onClick={() => setActiveTab('table')}
        >
          Test Cases
        </button>
        <button 
          className={`tab-btn ${activeTab === 'code' ? 'active' : ''}`}
          onClick={() => setActiveTab('code')}
        >
          Executable Code
        </button>
        <button 
          className={`tab-btn ${activeTab === 'edge' ? 'active' : ''}`}
          onClick={() => setActiveTab('edge')}
        >
          Edge Cases
        </button>
        <button 
          className={`tab-btn ${activeTab === 'bugs' ? 'active' : ''}`}
          onClick={() => setActiveTab('bugs')}
        >
          Bug Risks
        </button>
      </div>
      <div className="tab-content" style={{ minHeight: '300px' }}>
        {renderContent()}
      </div>
    </div>
  );
};

export default ResultsViewer;
