import React, { useState } from "react";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    sex: "F",
    age: 18,
    address: "U",
    guardian: "mother",

    Medu: 2,
    Fedu: 2,
    studytime: 2,
    failures: 0,
    absences: 5,

    famrel: 4,
    freetime: 3,
    health: 4,

    G1: 10,
    G2: 10
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData)
    });

    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="container">
      <h1>Student Performance Prediction System</h1>

      <form onSubmit={handleSubmit} className="form">

        {/* PERSONAL DETAILS */}
        <h3>Personal Details</h3>
        <div className="grid">
          <label>Gender</label>
          <select name="sex" value={formData.sex} onChange={handleChange}>
            <option value="F">Female</option>
            <option value="M">Male</option>
          </select>

          <label>Age</label>
          <input type="number" name="age" value={formData.age} onChange={handleChange} />

          <label>Address</label>
          <select name="address" value={formData.address} onChange={handleChange}>
            <option value="U">Urban</option>
            <option value="R">Rural</option>
          </select>

          <label>Guardian</label>
          <select name="guardian" value={formData.guardian} onChange={handleChange}>
            <option value="mother">Mother</option>
            <option value="father">Father</option>
            <option value="other">Other</option>
          </select>
        </div>

        {/* ACADEMIC DETAILS */}
        <h3>Academic Details</h3>
        <div className="grid">
          <label>Mother Education (0–4)</label>
          <input type="number" name="Medu" value={formData.Medu} onChange={handleChange} />

          <label>Father Education (0–4)</label>
          <input type="number" name="Fedu" value={formData.Fedu} onChange={handleChange} />

          <label>Study Time (1–4)</label>
          <input type="number" name="studytime" value={formData.studytime} onChange={handleChange} />

          <label>Past Failures</label>
          <input type="number" name="failures" value={formData.failures} onChange={handleChange} />

          <label>Absences</label>
          <input type="number" name="absences" value={formData.absences} onChange={handleChange} />
        </div>

        {/* LIFESTYLE */}
        <h3>Lifestyle</h3>
        <div className="grid">
          <label>Family Relationship (1–5)</label>
          <input type="number" name="famrel" value={formData.famrel} onChange={handleChange} />

          <label>Free Time (1–5)</label>
          <input type="number" name="freetime" value={formData.freetime} onChange={handleChange} />

          <label>Health (1–5)</label>
          <input type="number" name="health" value={formData.health} onChange={handleChange} />
        </div>

        {/* PREVIOUS MARKS */}
        <h3>Previous Exam Marks</h3>
        <div className="grid">
          <label>G1 (First Period)</label>
          <input type="number" name="G1" value={formData.G1} onChange={handleChange} />

          <label>G2 (Second Period)</label>
          <input type="number" name="G2" value={formData.G2} onChange={handleChange} />
        </div>

        <button type="submit">Predict Performance</button>
      </form>

      {result && (
        <div className="result">
          <h2>Prediction Result</h2>
          <p><strong>Predicted Grade:</strong> {result.predicted_grade}</p>
          <p><strong>Performance Level:</strong> {result.performance_level}</p>
        </div>
      )}
    </div>
  );
}

export default App;
