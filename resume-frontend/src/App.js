import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [jd, setJd] = useState("");

  const handleFileChange = (e) => {
    // 获取用户选择的文件
    setFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    setLoading(true);
    // 你来实现：
    // 1. 把file放进FormData
    const formData = new FormData();
    formData.append("file", file);
    // 2. 用fetch调用 http://localhost:8000/analyze
    const response = await fetch("http://localhost:8000/analyze", {
      method: "post",
      body: formData,
    });
    // 3. 把结果存到result
    const data = await response.json();
    setResult(data.result);
    // 4. loading状态管理
    setLoading(false);
  };

  const handleMatch = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(
      `http://localhost:8000/match?jd=${encodeURIComponent(jd)}`,
      {
        method: "post",
        body: formData,
      },
    );
    const data = await response.json();
    setResult(data.result);
    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", maxWidth: "800px", margin: "0 auto" }}>
      <h1>Resume Analyzer</h1>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      <button onClick={handleAnalyze} disabled={!file || loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>
      <textarea
        placeholder="paste jb description here..."
        value={jd}
        onChange={(e) => setJd(e.target.value)}
        style={{ width: "100%", height: "150px", marginTop: "20px" }}
      />
      <button onClick={handleMatch} disabled={!file || !jd || loading}>
        {loading ? "Matching..." : "Match with JD"}
      </button>
      {result && <pre style={{ marginTop: "20px" }}>{result}</pre>}
    </div>
  );
}

export default App;
