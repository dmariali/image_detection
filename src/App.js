import React, { useState } from "react";
import "./App.css";

const App = () => {
  const [annotatedImage, setAnnotatedImage] = useState(null);

  const detect = async (image) => {
    const fetch_url = "http://127.0.0.1:8000/";
    const response = await fetch(fetch_url, {
      method: "GET",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
      },
      // body: `{
      //   "url": URL.createObjectURL(image),
      //   "name": image.name,
      //   }`,
    });

    response.json().then((data) => {
      console.log(data);
    });
  };

  return (
    <div className="App">
      <h1>Upload image</h1>
      <input
        type="file"
        name="myImage"
        onChange={(event) => {
          detect(event.target.files[0]);
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
