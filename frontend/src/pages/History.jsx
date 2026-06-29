import { useEffect, useState } from "react";
import api from "../services/api";
import "../styles/history.css";

function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get("/history");
        setHistory(res.data);
      } catch (err) {
        console.log(err);
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="container history-page">
      <h1>Prediction History</h1>

      {history.length === 0 ? (
          <p style={{ textAlign: "center" }}>No predictions found.</p>
      ) : (
        <div className="history-grid">
          {history.map((item) => (
              <div
                className="history-card"
                key={item.prediction_id}
              >

              <img
                src={item.annotated_image_url}
                  alt="Prediction"
              />

                <div className="history-content">

                  <h3>{item.severity}</h3>

                  <p><strong>Potholes:</strong> {item.pothole_count}</p>

                  <p>
                    <strong>Confidence:</strong>{" "}
                    {(parseFloat(item.average_confidence) * 100).toFixed(1)}%
                  </p>

                  <p>
                    <strong>Covered Area:</strong>{" "}
                    {item.covered_area_percent}%
                  </p>

                  <p>
                    <strong>Timestamp:</strong><br />
                    {item.timestamp}
                  </p>

                </div>

            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default History;