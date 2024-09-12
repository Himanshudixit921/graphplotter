import React, { useState } from "react";
import axios from "axios";

function App() {
  const [equation, setEquation] = useState("");
  const [imageUrl, setImageUrl] = useState("");

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Send POST request to Flask backend
      const response = await axios.post(
        "http://localhost:5000/plot",
        {
          equation: equation,
        },
        { responseType: "blob" }
      );

      // Convert the response into an image URL
      const url = URL.createObjectURL(new Blob([response.data]));
      setImageUrl(url);
    } catch (error) {
      console.error("Error plotting graph", error);
    }
  };

  return (
    <div className="App">
      <h1>Graph Plotter</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter an equation (e.g., x**2 + 3*x + 2)"
          value={equation}
          onChange={(e) => setEquation(e.target.value)}
          required
        />
        <button type="submit">Plot Graph</button>
      </form>

      {imageUrl && (
        <div>
          <h2>Graph Output:</h2>
          <img src={imageUrl} alt="Graph" />
        </div>
      )}
    </div>
  );
}

export default App;
