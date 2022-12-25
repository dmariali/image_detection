import React, { useState } from "react";
import "./App.css";

const App = () => {
  const [annotatedImage, setAnnotatedImage] = useState(null);

  const detect = async (event) => {
    const fetch_url = "http://127.0.0.1:8000/uploadfile";

    const files = Array.from(event.target.files);
    const formData = new FormData();
    formData.append("data", files[0]);

    await fetch(fetch_url, {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => console.log(data));
  };

  return (
    <div className="App">
      <h1>Upload image</h1>
      <input
        type="file"
        name="myImage"
        onChange={(event) => {
          detect(event);
        }}
      />

      {annotatedImage && (
        <div>
          {/* <img alt="not found" width={"250px"} src={URL.createObjectURL(annotatedImage)} /> */}
          <br />
          <button onClick={() => setAnnotatedImage(null)}>Remove</button>
        </div>
      )}
    </div>
  );
};

export default App;
