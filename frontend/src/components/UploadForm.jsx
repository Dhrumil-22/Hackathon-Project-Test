import React, { useState } from "react";
import { moderateText, moderateImage } from "../api";


export default function UploadForm() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleTextSubmit = async () => {
  try {
    const res = await moderateText(text);
    setResult(res);
  } catch (err) {
    console.error(err);
  }
};

const handleImageSubmit = async () => {
  if (!file) return;
  try {
    const res = await moderateImage(file);
    setResult(res);
  } catch (err) {
    console.error(err);
  }
};

  return (
    <div>
      <h2>Moderate Text </h2>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type something..."
      />
      <button onClick={handleTextSubmit}>Predict Text</button>

      <h2>Moderate Image</h2>
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
