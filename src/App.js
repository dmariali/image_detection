import React, { useState } from "react";
import "./App.css";

const App = () => {
  const [originalImage, setOriginalImage] = useState(null)
  const [annotatedImage, setAnnotatedImage] = useState(null);

  const detect = async (event) => {
    const fetch_url = "http://127.0.0.1:8000/detectobjects";

    const files = Array.from(event.target.files);
    const formData = new FormData();
    formData.append("data", files[0]);

    await fetch(fetch_url, {
      method: "POST",
      body: formData,
    })
      .then((res) => res.blob())
      .then((data) => {
        console.log(data)
        setAnnotatedImage(data)
      });
  };

  return (
    <div className="App">
      <h1>Upload image</h1>
      <input
        type="file"
        name="myImage"
        onChange={(event) => {
          setOriginalImage(event.target.files[0])
          detect(event);
        }}
      />

      {originalImage && (
        <div>
          <h1> ORIGINAL IMAGE </h1>
          <img alt="not found" width={"500px"} src={URL.createObjectURL(originalImage)} />
          <br />
          <button onClick={() => setOriginalImage(null)}>Remove</button>
        </div>
      )}
      { annotatedImage && (
        <div>
          <h1> ANNOTATED IMAGE </h1>
          <img alt={`not found ${annotatedImage}`} width={"500px"} src={URL.createObjectURL(annotatedImage)} />
        </div>
      )}
    </div>
  );
};

export default App;
