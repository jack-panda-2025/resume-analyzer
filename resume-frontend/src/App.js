import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

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

  return (
    <div style={{ padding: "40px", maxWidth: "800px", margin: "0 auto" }}>
      <h1>Resume Analyzer</h1>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      <button onClick={handleAnalyze} disabled={!file || loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>
      {result && <pre style={{ marginTop: "20px" }}>{result}</pre>}
    </div>
  );
}

export default App;
