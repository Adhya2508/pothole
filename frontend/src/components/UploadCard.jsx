import { useRef, useState } from "react";
import api from "../services/api";
import Loader from "./Loader";
import ResultCard from "./ResultCard";
import "../styles/upload.css";

function UploadCard() {
  const fileInputRef = useRef();

  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    setImage({
      file,
      preview: URL.createObjectURL(file),
    });

    setResult(null);
  };

  const removeImage = () => {
    setImage(null);
    setResult(null);
    fileInputRef.current.value = "";
  };

  const analyzeImage = async () => {
    if (!image) {
      alert("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", image.file);

    try {
      setLoading(true);

      const response = await api.post("/predict", formData);

      setResult(response.data);

    } catch (err) {
      console.error(err);
      alert("Prediction failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="upload-card">

        <h2>Upload Road Image</h2>

        {!image ? (
          <div className="upload-box">

            <div className="upload-icon">📤</div>

            <p>Drag & Drop Image Here</p>

            <span>or</span>

            <button
              className="browse-btn"
              onClick={() => fileInputRef.current.click()}
            >
              Browse Files
            </button>

            <input
              type="file"
              hidden
              accept="image/*"
              ref={fileInputRef}
              onChange={handleFileChange}
            />

            <small>JPG • PNG • JPEG</small>

          </div>
        ) : (
          <div className="preview-box">

            <img src={image.preview} alt="preview" />

            <button
              className="remove-btn"
              onClick={removeImage}
            >
              Remove Image
            </button>

          </div>
        )}

        <button
          className="analyze-btn"
          onClick={analyzeImage}
        >
          Analyze Image
        </button>

      </div>

      {loading && <Loader />}

      {result && (
        <ResultCard
          result={result}
          original={image.preview}
        />
      )}
    </>
  );
}

export default UploadCard;