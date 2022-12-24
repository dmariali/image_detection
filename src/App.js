import React, { useState } from "react";
import "./App.css";

const App = () => {
  const [annotatedImage, setAnnotatedImage] = useState(null);

  const detect = async (image) => {
    console.log('URL is ', URL.createObjectURL(image), 'and name is ', image.name)

    // const response = await fetch("https://reqbin.com/echo/post/json", {
    //   method: 'POST',
    //   headers: {
    //     'Accept': 'application/json',
    //     'Content-Type': 'application/json'
    //   },
    //   body: `{
    //     "Id": 78912,
    //     "Customer": "Jason Sweet",
    //     "Quantity": 1,
    //     "Price": 18.00
    //     }`,
    //   });
  
    //   response.json().then(data => {
    //     console.log(data);
    //   });
  }

  return (
    <div className='App'>
      <h1>Upload image</h1>
      <input
        type="file"
        name="myImage"
        onChange={(event) => {
          detect(event.target.files[0])
        }}
      />

      {annotatedImage && (
        <div>
        {/* <img alt="not found" width={"250px"} src={URL.createObjectURL(annotatedImage)} /> */}
        <br />
        <button onClick={()=>setAnnotatedImage(null)}>Remove</button>
        </div>
      )}
    </div>
  );
};

export default App;


