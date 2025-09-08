import React, { useState } from "react";
import { predictText, predictImage } from "../api";


export default function UploadForm() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleTextSubmit = async () => {
    const res = await predictText(text);
    setResult(res);
  };

  const handleImageSubmit = async () => {
    if (!file) return;
    const res = await predictImage(file);
    setResult(res);
  };

  return (
    <div>
      <h2>Text Prediction</h2>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type something..."
      />
      <button onClick={handleTextSubmit}>Predict Text</button>

      <h2>Image Prediction</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleImageSubmit}>Predict Image</button>

      {result && (
        <div>
          <h3>Prediction Result:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
